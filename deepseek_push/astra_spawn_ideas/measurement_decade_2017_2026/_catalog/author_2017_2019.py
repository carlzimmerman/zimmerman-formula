"""Serialize original release-specific work orders; does not execute their science."""
import json
import re
from pathlib import Path
P=Path(__file__).parent
blocks={}
def add(y,s,txt):
 rows=[x.split('|') for x in txt.strip().splitlines() if x.strip()]
 assert len(rows)==25,(y,s,len(rows))
 assert all(len(r)==3 for r in rows),(y,s)
 blocks[y,s]=rows

add(2017,1,r'''
Dispersive phase curvature|K_disp(f)=d²[Psi_obs-Psi_src]/df²; remove constant phase and time directions before bounding K_disp|GW170104 calibrated phase and detector noise; source phase must be derived
Massive-dispersion interpretation audit|v_g²/c²=1-m_eff² c⁴/E² is a diagnostic ansatz; derive whether the action admits m_eff before translating its bound|GW170104 reported propagation constraint and waveform frequency support
Distance-weighted propagation integral|I_alpha(z)=integral_0^z (1+z')^(alpha-2)/H(z') dz'; deltaPsi=A_alpha I_alpha f^(alpha-1)|GW170104 luminosity-distance likelihood and redshift uncertainty, not a fixed inferred redshift
Spin-dispersion score separation|F_Achi=<partial_A h,partial_chi h>; F_AA.marg=F_AA-F_Achi²/F_chichi|GW170104 effective-spin and phase information
Parity-even propagation transfer|h_obs=T_even(f,z)h_src; constrain Re log T_even and Im log T_even jointly|GW170104 two-detector frequency-dependent amplitude and phase
Causal dispersive retarded kernel|K_ret(t)=Fourier^-1 T_even; quantify norm(K_ret on t<0) in preferred time|GW170104 sensitivity-weighted transfer band; outside-band completion explicit
Inspiral-merger dispersive closure|Delta_A=A_inspiral-A_merger with covariance from common strain realization|GW170104 inspiral and merger windows
Spin-precession leakage into phase|deltaPsi_prec projected orthogonally to f^(alpha-1); bound the remaining propagation score|GW170104 precession-sensitive waveform residuals
Amplitude-distance degeneracy|rank partial(log A_obs,Psi_obs)/partial(log dL,log G_rad,A_alpha)|GW170104 strain amplitude and phase; calibrated detector response
Wavefront coherence across detectors|C_HL(f)=h_H(f)h_L*(f) exp(2pi i f Delta_t_HL)|GW170104 Hanford-Livingston cross spectrum
Source-frame mass transport|M_source=M_detector/(1+z); derive Jacobian J=1/(1+z) for each independent mass coordinate|GW170104 mass-distance posterior with original prior recovered
Effective-spin sign robustness|P(chi_eff<0 given d) across waveform families sharing the same propagation law|GW170104 two-body spin posterior and prior support
Redshift dispersion monotonicity|dI_alpha/dz=(1+z)^(alpha-2)/H(z)>0 only for H>0; derive allowed parameter domain|GW170104 distance support and candidate expanding background
Vacuum-induced tensor refractive term|delta n_T(f)=partial_k omega_T/c-1 from the quadratic tensor action, then integrate phase along the event ray|GW170104 propagation residual and candidate vacuum background
Heat-filter tensor contamination|T_tensor(k,xi)=exp(-xi²k²/2) only if obtained from varied tensor equations; bound any induced attenuation|GW170104 observed high-frequency waveform support
Running kinetic normalization|dL_GW/dL_EM=sqrt(Q_T(0)/Q_T(z)) conditional on derived WKB transport|GW170104 amplitude-distance degeneracy and candidate Q_T history
Frequency-dependent arrival ordering|Delta_t(f1,f2)=(1/2pi)[partial_f deltaPsi(f1)-partial_f deltaPsi(f2)]|GW170104 phase slopes in nonoverlapping frequency bands
Dispersion likelihood prior-volume audit|p(A given d)/pi(A) proportional to likelihood only after marginalization assumptions are proved|GW170104 published propagation posterior and original nuisance priors
Near-source environmental delay|delta_t_env=integral_near_source (n_T-1)dl/c; separate it from cosmological propagation|GW170104 distance and source-environment uncertainty
Waveform truncation propagation bias|Delta_A=(F^-1)_Aj<partial_j h,delta h_trunc>|GW170104 residual waveform budget across inspiral-merger attachment
Positive tensor-energy flux|F_GW=Q_T <dot h_ij dot h_ij>/4; compare source energy loss with radiated strain|GW170104 amplitude evolution and source parameters conditional on distance
Detector calibration phase degeneracy|deltaPsi_cal=a+b f+c f²; profile c jointly with propagation curvature|GW170104 calibration phase uncertainty by interferometer
Merger time as a preferred-time observable|t_det=t_source+integral dl/v_g plus clock offsets; establish monotone time mapping|GW170104 detector clock and coalescence-time metadata
Dispersion exclusion without graviton particles|B_alpha={A_alpha: Delta log L within threshold}; report B_alpha rather than particle mass unless particle interpretation is derived|GW170104 propagation likelihood and calibrated strain
Cross-event incremental dispersion gain|F_new=F_104-F_104,shared F_shared^-1 F_shared,104; shared calibration retained|GW170104 data combined conditionally with earlier events, excluding duplicate GWTC-1 strain
''')
add(2017,2,r'''
Three-detector tensor response rank|rank F_T(n)=rank[(F_I^+,F_I^cross)] for I=H,L,V over the sky posterior|GW170814 detector antenna geometry and timing-localization likelihood
Tensor null-stream construction|n_I proportional to epsilon_IJK F_J^+ F_K^cross; N=sum_I n_I d_I|GW170814 synchronized three-detector strain
Scalar response falsifier|R_b=min_hb norm(d-F_b h_b)^2; compare to tensor residual with matched nuisance dimension|GW170814 coherent amplitudes and breathing-mode antenna pattern
Vector response falsifier|R_v=min_hx,hy norm(d-F_x h_x-F_y h_y)^2|GW170814 coherent network waveform and vector response templates as controls
Tensor ellipse reconstruction|epsilon(f)=h_cross(f)/h_plus(f) from noise-weighted inversion of F_T|GW170814 three-detector phase and amplitude ratios
Virgo leave-out prediction|p(d_V given d_H,d_L,T)=integral p(d_V given theta,T)p(theta given d_H,d_L,T)dtheta|GW170814 Virgo waveform withheld from tensor fit
Timing-annulus intersection|c Delta_t_IJ=(r_I-r_J) dot n; propagate timing covariance to sky area|GW170814 measured network arrival times
Calibration-null leakage|N_cal=sum_I n_I(deltaA_I+i deltaPhi_I)h_I|GW170814 detector-specific calibration envelopes
Polarization-sky degeneracy|F_pol.marg=F_pol,pol-F_pol,n F_nn^-1 F_n,pol|GW170814 polarization comparison and localization covariance
Common-clock null invariance|N(t+delta t) versus independently shifted detector times; only common shifts preserve coherence|GW170814 timing metadata and reconstructed null stream
Preferred-frame antenna transport|e_ab^A(n,u_pref) projected into detector tetrads; derive sidereal dependence|GW170814 known detector orientation and event time
Tensor-only curvature response|R_0i0j=-ddot h_ij/(2c²) in detector frame; project geodesic deviation into arm lengths|GW170814 strain and interferometer geometry
Polarization Bayes-factor prior audit|B_TV=int L_T pi_T/int L_V pi_V under equal sky-distance measures|GW170814 published polarization odds; original likelihood access required
Coherent versus incoherent energy|E_coh=d†P_T d; E_null=d†(I-P_T)d with colored-noise whitening|GW170814 network time-frequency pixels
Polarization bandwidth stability|Delta B=B_TV(f<f_cut)-B_TV(f>f_cut), covariance from a shared source|GW170814 frequency-resolved network likelihood
Detector-response frequency correction|F_I^A(f)=D_I^ab(f)e_ab^A; bound long-wavelength approximation residual|GW170814 arm-transfer functions and upper waveform frequencies
Handedness distinguishability|h_R,L=(h_plus plus_or_minus i h_cross)/sqrt(2); compute identifiable chirality score|GW170814 complex coherent amplitudes
Extra-mode identifiability ceiling|rank F_all<=3; characterize nullspace of six-polarization response before claiming mode counts|GW170814 three measured detector channels
Near-degenerate sky directions|s_min(F_T(n)) mapped over sky credible support|GW170814 localization and antenna matrix
Non-Gaussian null-stream tails|P(E_null>x) estimated from time-slid off-source data with the event weights fixed|GW170814 off-source network strain needed, availability to verify
Tensor wave speed from baseline|Delta_t_IJ=(baseline dot n)/c_T; infer joint c_T-sky degeneracy without electromagnetic timing|GW170814 network timing and sky localization
Source-inclination polarization map|h_plus/h_cross=(1+cos²inclination)/(2 i_unit cos(inclination)) for a specified Fourier phase convention only after quadrupole limit is derived|GW170814 inclination and polarization likelihood
Polarization memory projection|Delta h_mem projected into F_T and null stream with detector low-frequency response|GW170814 event strain baseline and memory-sensitive frequencies
Network distance consistency|dL_I inferred conditionally on common n,i,psi; test Delta log dL_IJ|GW170814 per-detector calibrated amplitudes
Two-DOF observation certificate boundary|observed tensor rank=2 does not imply Hamiltonian N_grav=2; enumerate invisible modes from F_all nullspace|GW170814 polarization measurement and pinned candidate constraint analysis
''')
add(2017,3,r'''
Multimessenger propagation delay|Delta t_obs=(1+z)Delta t_emit+integral dz (1/v_g-1/c)c/H(z)|GW170817 coalescence time, counterpart delay and host-distance information
Emission-lag partial identification|B_v=union_tau in physical lag set B_v(tau); preserve sign-asymmetric lag bounds|GW170817 gamma-ray association timing and explicit emission-lag model
Tensor light-cone matching|c_T²=F_T/Q_T; derive equality to photon characteristic speed on the traversed background|GW170817 arrival association and candidate tensor action
Differential Shapiro delay map|Delta t_g-gamma=-integral (Phi_g+Psi_g-Phi_gamma-Psi_gamma)dl/c³|GW170817 common sky direction and uncertain line-of-sight potentials
Host-distance versus standard-siren amplitude|dL_GW/dL_host inferred jointly with inclination; derive amplitude transport before fitting|GW170817 strain amplitude and independently authenticated host-distance data
Tidal phase observation map|deltaPsi_tidal proportional to Lambda_tilde v^5 at leading order; derive coefficient for the candidate star equations|GW170817 late-inspiral phase and neutron-star mass correlations
Tidal deformability normalization|Lambda_i=(2/3)k2_i(c²R_i/(G_N M_i))^5 with measured G_N distinguished from stellar G|GW170817 tidal likelihood and separately acquired stellar EOS inputs
Spin-tide degeneracy|F_Lambda,chi=<partial_Lambda h,partial_chi h>; find well-measured combinations|GW170817 low-spin and broad-spin prior analyses
Binary binding-energy flux test|dot f=-F_rad/(dE_b/df); derive tidal and MONO-matching corrections separately|GW170817 frequency evolution across inspiral
Luminosity-distance inclination manifold|A proportional to [(1+cos²i)^2 F_plus²+4cos²i F_cross²]^1/2/dL|GW170817 network amplitudes and polarization information
Prompt-emission clock transformation|Delta tau_source=Delta t_detector/(1+z) after detector and barycentric corrections|GW170817 detector timestamps and host redshift, with peculiar velocity treated separately
Neutron-star surface acceleration domain|y_surface=G_N M/(R² a0); identify whether high-y recovery controls tidal observables|GW170817 mass likelihood and explicitly external radius constraints
Heat-filter stellar matching|solve filtered source for finite stellar density and match exterior Phi, dPhi/dr at surface|GW170817 tidal phase sensitivity and baryonic stellar profile candidates
Finite-frequency tensor dispersion|DeltaPsi(f)=integral[k(f,z)-2pi f(1+z)/c]dl; constrain without assuming constant c_T|GW170817 broad inspiral frequency support
Prompt-counterpart association uncertainty|L_delay=p_assoc L_same+(1-p_assoc)L_accidental|GW170817 temporal and localization association evidence
Peculiar-velocity siren bias|cz=H0 d+v_pec; Delta H0=Delta v_pec/d in the low-z diagnostic limit|GW170817 host redshift and velocity-field information requiring independent authentication
Photon graviton metric consistency|compare principal symbols P_gamma(k)=g^munu k_mu k_nu and P_T(k)|GW170817 timing association under a single matter-photon metric
Tidal response causality|lambda(omega)=integral_0^infty K_tide(t)e^(i omega t)dt; bound negative-time support separately|GW170817 inspiral tidal response band and candidate preferred time
Merger cutoff censorship|L(f<f_cut) versus full L; isolate matter-disruption modeling dependence of propagation bound|GW170817 inspiral and merger-frequency data availability
Distance-free phase-delay combination|R=[partial_f Psi_g(f2)-partial_f Psi_g(f1)]/Delta t_gamma removes an adopted distance only under stated common path assumptions|GW170817 phase slopes and gamma-ray lag
Source-to-vacuum coupling transition|jump conditions [Q_T partial_n h]=0 across stellar-vacuum boundary from varied action|GW170817 amplitude and phase through matter-to-vacuum propagation
Binary center-of-mass equivalence test|a_CM=(m1 a1+m2 a2)/(m1+m2); derive cancellation of internal forces before interpreting timing|GW170817 phase coherence and source environmental acceleration bounds
Common-scale multimessenger compatibility|intersect B_cT(a0_canonical) and B_cT(a0_alternative) only as separately labelled models|GW170817 timing likelihood and both fixed acceleration normalizations
Tidal likelihood reweighting validity|w=pi_candidate(theta)/pi_GR(theta) valid only when waveform likelihood is unchanged|GW170817 released posterior assumptions; raw likelihood if observation map changes
Propagation bound to criterion-B scope|Delta t limits tensor speed; construct preferred-time characteristic ordering for non-tensor channels independently|GW170817 delay constraint and candidate mixed-system principal symbol
''')
add(2017,4,r'''
Low-mass chirp phase coefficient|Psi_N(f)=3( pi G_chirp M_c f/c³)^(-5/3)/128; derive G_chirp versus measured G_N|GW170608 inspiral phase and detector-frame chirp mass
Dipole-radiation null channel|deltaPsi_-1PN=beta_D v^-7; derive whether beta_D vanishes for two gravitational DOF|GW170608 long inspiral waveform
Low-frequency acceleration drift|deltaPsi_acc(f) from time-dependent Doppler factor 1+v_CM(t)/c; separate from chirp mass|GW170608 early-inspiral phase and source-environment prior
Radiation-to-conservative coupling ratio|R_G=G_rad/G_cons; infer only combinations surviving mass rescaling symmetry|GW170608 chirp evolution and amplitude
Post-Newtonian coefficient triangle|C_j=psi_j-psi_j(M_c,eta,chi); joint residual vector with off-diagonal covariance|GW170608 multiple inspiral phase coefficients
Adiabatic inspiral validity|epsilon_ad=abs(dot omega/omega²); locate measurement support where expansion error is controlled|GW170608 measured chirp trajectory
Eccentricity versus negative-PN phase|deltaPsi_e=e_ref² K_e(f); orthogonalize against v^-7|GW170608 low-frequency residuals and eccentricity nuisance
Spin-induced quadrupole response|Q_i=-kappa_i chi_i² G_N² m_i³/c⁴; derive candidate kappa_i before fitting|GW170608 inspiral spin-phase correlations
Inspiral horizon absorption|F_abs/F_inf as a derived frequency function; infer allowed coefficient after spin marginalization|GW170608 phase evolution before merger
Finite-size high-y correction|delta E/E=F(y_orb,xi/r); estimate separately from PN truncation|GW170608 orbital-frequency-inferred separation, conditional on source dynamics
Chirp mass calibration degeneracy|deltaPsi_cal projected on f^-5/3; bound apparent Delta M_c|GW170608 phase calibration and inspiral spectrum
Time-domain chirp reconstruction|M_c(t)=(c³/G_chirp)[5 dot f/(96 pi^(8/3) f^(11/3))]^(3/5)|GW170608 frequency ridge with noise derivative regularization
Frequency-domain energy balance|dE/df=-F_rad/dot f from reconstructed chirp, keeping distance normalization explicit|GW170608 amplitude spectrum and phase derivative
Inspiral-only remnant forecast|p(M_f,chi_f given d_insp) transported through candidate merger equations|GW170608 inspiral posterior and merger waveform held out
Ringdown residual envelope|h_RD=sum_n A_n exp(-t/tau_n)cos(omega_n t+phi_n); constrain only resolvable combinations|GW170608 post-peak strain and noise
Reduced-mass symmetry audit|eta=m1 m2/(m1+m2)²; verify likelihood invariance under label exchange|GW170608 component-mass likelihood and spin labels
Orbital-plane precession torque|dot L=Omega_prec cross L from candidate spin action; compare modulation residuals|GW170608 inclination and precession-sensitive strain
Amplitude PN harmonic content|h=sum_m A_m(f) exp(i m phi); bound nonquadrupole residual after detector response|GW170608 harmonic-sensitive frequency bands
Conservative MONO-to-PN matching|derive overlap expansion Phi=-G_N M/r+deltaPhi_MONO then compute periastron/inspiral corrections|GW170608 strong-field frequency window and baryonic source matching assumptions
Unmodeled low-frequency glitch bias|Delta theta=F^-1(partial h,glitch); require bounded bias at actual event noise|GW170608 off-source noise and event residuals
Detector-independent chirp consistency|Delta M_c=M_c,H-M_c,L with calibration and common waveform covariance|GW170608 separate Hanford/Livingston phase data
Source-redshift mass ambiguity|M_detector=(1+z)M_source; demonstrate which radiation coefficients remain dimensionless invariants|GW170608 distance likelihood with no electromagnetic redshift
Radiative memory energy consistency|Delta h_mem=(G_mem/(c⁴ dL))integral angular energy flux kernel dOmega|GW170608 radiated-energy posterior and low-frequency sensitivity
Low-mass versus GW170104 scaling|deltaPsi_608/deltaPsi_104 predicted from mass and distance scaling for one action coefficient|GW170608 and authenticated GW170104 data with shared calibration covariance
No-extra-particle radiation completion|derive all on-shell flux channels from reduced Hamiltonian and compare missing flux to chirp residual|GW170608 inspiral residual energy budget; no invented radiated species
''')
add(2017,5,r'''
Composition-dependent free-fall coefficient|eta_TiPt=2(a_Ti-a_Pt)/(a_Ti+a_Pt); derive eta from matter variation|MICROSCOPE Ti/Pt differential acceleration report
Common-mode leakage bound|a_diff=eta g+k_cm a_common; profile k_cm with calibration uncertainty|MICROSCOPE differential and common accelerometer channels if obtained
Thermal-line degeneracy|a_diff(f_EP)=eta g(f_EP)+k_T T(f_EP)|MICROSCOPE science-frequency acceleration and temperature telemetry
Tidal off-centering correction|delta a_i=Gamma_ij Delta x_j; propagate miscentering covariance into eta|MICROSCOPE gravity-gradient and test-mass alignment calibration
Spin-orbit modulation map|g_EP(t)=R_body(t)g_Earth(t); derive signal sidebands from attitude|MICROSCOPE orbit and spacecraft rotation metadata
Electrostatic actuation universality|F_act/m_inertial+grad Phi=0; distinguish force calibration from gravitational mass|MICROSCOPE force commands and mass calibration
Finite-size filtered force average|a_A=-(1/M_A)integral rho_A grad Phi d³x; compare Ti and Pt geometry|MICROSCOPE test-mass shapes and filtered Earth potential
Surface-patch force nuisance|a_patch=(1/m)integral sigma_E E_patch dA; bound EP-frequency projection|MICROSCOPE instrument systematic-error budget
Drag-free control transfer|a_meas(omega)=H_ctrl(omega)a_true(omega)+n; recover eta at EP frequency|MICROSCOPE closed-loop response metadata
Weak-equivalence Noether bridge|nabla_mu T_A^munu=0 implies metric geodesics for each composition under stated point-body limit|MICROSCOPE differential-acceleration upper range and candidate matter action
Binding-energy composition sensitivity|eta_AB=(s_A-s_B) q_env with s_A=partial log m_A/partial q|MICROSCOPE Ti/Pt composition and separately authenticated binding fractions
Earth acceleration high-y expansion|delta a/g=nu_mono(g_N/a0)-1 after finite-body filtering, not unfiltered substitution|MICROSCOPE orbital gravity and source geometry
Reference sensor null prediction|eta_same=0 plus geometric terms; test identical-composition reference without fitting eta_TiPt|MICROSCOPE reference-channel data availability must be established
Statistical systematic convolution|p(eta)=integral L(eta+b)pi_sys(b)db; compare Gaussian and bounded systematic priors|MICROSCOPE separately quoted statistical/systematic uncertainties
Orbit-eccentricity harmonic leverage|eta g(t) expanded in orbital harmonics; distinguish 1/r² from constant instrument offset|MICROSCOPE orbit ephemeris and acceleration harmonics
Preferred-direction free-fall signal|delta a_i=K_ij(u_pref)a_j; derive sidereal/orbital tensor projections|MICROSCOPE spacecraft attitude and laboratory frame velocity
Finite propagation across satellite|Delta t=L/v_channel; calculate phase shift at spin frequency under criterion B|MICROSCOPE test-mass separation and rotating field frequency
Self-gravity calibration contamination|Phi_self from spacecraft mass model; compute differential gradient and attitude dependence|MICROSCOPE spacecraft geometry and calibration report
Noise-color effective sample size|var eta=(g^T C^-1 g)^-1; compare to white-noise approximation|MICROSCOPE acceleration-noise spectrum and window function
Data-gap spectral leakage|tilde a_obs=W*tilde a; bound neighboring-line leakage into f_EP|MICROSCOPE session sampling mask if released
Vacuum-scale uncertainty transfer|partial eta/partial a0 times separate canonical/alternative a0 shifts, with no per-material fit|MICROSCOPE eta likelihood and candidate composition response
Inertial-gravitational G distinction|a=G_E M_E q_A/r²; determine measured combination compared with laboratory G_N|MICROSCOPE orbital acceleration and independent Earth GM
Mass-swap thought-experiment estimator|eta changes sign under composition exchange while fixed instrument bias need not; derive identifiable antisymmetric component|MICROSCOPE physical sensor-channel assignments and asymmetry calibration
Nonlinear actuator harmonic foldback|a_act=k1 V²+k2 V⁴; calculate mixing products at f_EP|MICROSCOPE actuation voltage spectrum and nonlinear calibration
EP bound to universal matter coupling|sup_A,B abs(q_A-q_B) cannot follow from Ti/Pt alone; characterize the measured composition subspace|MICROSCOPE Ti/Pt coefficient and candidate ordinary-matter species charges
''')
add(2017,6,r'''
Shear Weyl-potential kernel|C_l^ij=integral dchi W_i W_j P_(Phi+Psi)(l/chi,chi)/chi² with normalization derived from geodesic deviation|DES Y1 tomographic shape correlations and source distributions
Real-space spin-two projection|xi_plus/minus(theta)=integral l dl C_l J_0/4(l theta)/(2pi)|DES Y1 angular bins and finite-window integration
Finite-angle E/B ambiguity|xi restricted to [theta_min,theta_max] admits ambiguous modes; construct compensated T_plus/minus|DES Y1 angular scale cuts and covariance
Shear-calibration amplitude modes|C_obs^ij=(1+m_i)(1+m_j)C_true^ij; identify rank of m_i-growth degeneracy|DES Y1 independent shape catalogs and response calibrations
Source-redshift functional response|delta C_l^ij=int dz [delta C_l^ij/dn_i(z)]delta n_i(z)|DES Y1 redshift-calibration alternatives
Intrinsic-alignment separation|C_obs=C_GG+C_GI+C_IG+C_II; derive tidal-response source of each term|DES Y1 source colors and tomographic correlations
MONO filter scale projection|partial C_l/partial xi computed through S(k)=exp(-xi²k²/2), including growth and lensing variations|DES Y1 angular support and fixed candidate filter
Nonlinear response beyond halo import|P_Weyl=P_Weyl,linear+Delta P_candidate; derive Delta P without inserting a CDM halo prescription|DES Y1 small-angle shear residuals
Baryonic feedback tangent space|J_baryon=partial xi_pm/partial q_gas; project gravity score off J_baryon|DES Y1 scale-dependent correlations and independent gas priors
Tomographic ratio geometry test|R_l=C_l^ij/C_l^ik with common lens kernel approximations quantified|DES Y1 three source-bin combinations
Shape-noise contraction|N_l^ij=delta_ij sigma_e²/n_eff under uncorrelated shapes; derive corrections for weights|DES Y1 effective source weights and ellipticity variance
Survey-window mode coupling|C_tilde_l=sum_lprime M_llprime C_lprime|DES Y1 mask and two-point estimator window
Super-sample response covariance|Cov_SSC=partial C/partial delta_b times sigma_b² times partial C/partial delta_b|DES Y1 footprint and candidate separate-universe response
Parameter-dependent covariance|Delta log L includes log det C(theta); quantify effect of candidate-dependent covariance|DES Y1 shear data vector and covariance assumptions
Posterior S8 portability test|S8=sigma8(Omega_m/0.3)^0.5 is not sufficient when candidate transfer shape changes|DES Y1 parameter posterior versus underlying correlations
High-redshift tail sensitivity|Delta C_l from delta n(z>z_tail), constrained by normalization and calibration|DES Y1 uncertain source-distribution tails
Photo-z shear joint score|F_m,delta_z=(partial_m xi)^T C^-1 partial_delta_z xi|DES Y1 shear response and photometric-redshift offsets
Reduced-shear correction|g=gamma/(1-kappa); derive leading <gamma gamma kappa> contribution|DES Y1 smallest retained angular bins
Magnification selection correction|n_obs=n_true[1+(5s-2)kappa]; derive induced shear weighting bias|DES Y1 flux selection and number-count slopes
Cosmic shear vacuum-scale response|partial xi_pm/partial rho_L=(partial xi_pm/partial a0)a0/(2rho_L)+background terms|DES Y1 correlations with fixed scale relation and two separate normalizations
Cross-pipeline residual eigenmodes|Delta xi=xi_pipeline1-xi_pipeline2; whiten with covariance including shared shapes|DES Y1 paired analysis pipelines
Low-ell beyond-Limber correction|C_l=4pi int dk P_R(k)Delta_l^i Delta_l^j/k; compare exact projection to Limber|DES Y1 largest angles and source kernels
Shear-selected source clustering|<n_s gamma n_s gamma>/<n_s n_s> differs from <gamma gamma>; derive connected corrections|DES Y1 source positions and ellipticities
Growth-lensing slip identifiability|Sigma=(mu/2)(1+eta); determine measured Sigma-times-growth combinations|DES Y1 shear alone without assuming Phi=Psi
Shear parameter-cell compatibility|B_shear={candidate cells fitting xi_pm}; intersect fixed-action admissibility before any gate claim|DES Y1 vector, scale cuts and both acceleration footings
''')
add(2017,7,r'''
Galaxy-shear observation map|gamma_t(R)=DeltaSigma_Weyl(R)/Sigma_crit only after deriving projected metric potential|DES Y1 lens-source cross-correlations
Clustering bias cancellation|E_l=(C_gk)^2/C_gg; derive stochastic-bias residual r_gm²|DES Y1 galaxy clustering and galaxy-shear spectra
Joint covariance shared-shape block|C_joint=[[C_gg,C_gg,gk],[C_gk,gg,C_gk]] with common mask contractions|DES Y1 clustering and galaxy-shear estimators
Three-probe conditional likelihood|L(gk,gg given shear)=Gaussian with Schur-complement covariance when justified|DES Y1 3x2 vector excluding independent reuse of cosmic-shear likelihood
Lens redshift calibration response|delta gamma_t=int dz_l delta n_l(z_l)K_lens(z_l)|DES Y1 luminous-red-galaxy redshift distributions
Source-lens overlap dilution|gamma_obs=(1-f_assoc)gamma_background+gamma_IA,associated|DES Y1 close lens-source redshift pairs
Galaxy-bias scale dependence|b(k)=b1+b_grad k² plus derived stochastic term; determine safe expansion domain|DES Y1 angular clustering scale range
Halo-free lens mass reconstruction|DeltaSigma_Weyl=bar Sigma_Weyl-Sigma_Weyl; invert with finite-radius boundary term|DES Y1 tangential shear profiles and lens light
Metric slip from joint observables|C_g(Phi+Psi)/C_gdelta derived with candidate continuity and Euler equations|DES Y1 clustering-lensing amplitudes and external velocity dependency
Lens magnification contamination|delta_g,obs=b delta+(5s_l-2)kappa_l; propagate into C_gg and C_gk|DES Y1 lens selection slope and angular correlations
Stochastic galaxy-matter coefficient|r_gm=C_gm/sqrt(C_gg C_mm); infer admissible r_gm without setting it to one|DES Y1 three-probe correlations
Nonlocal source-gate imprint|delta rho_active(k)=G_gate(k,environment)delta rho_b; derive correlated effect in gg and gk|DES Y1 joint scale dependence and candidate carrier gate
Small-scale point-mass marginalization|gamma_t(theta)=A_PM/theta²+gamma_extended(theta); marginalize A_PM coherently|DES Y1 lens-source angular measurements
Redshift-bin cross-clustering leak|C_gg^ij from nonoverlapping true n_i,n_j should isolate magnification and catastrophic-z tails|DES Y1 lens-bin cross-correlations if archived
Three-probe consistency triangle|R=(C_gk)^2/(C_gg C_kk) bounded by positive-semidefinite field covariance after noise removal|DES Y1 matched-window three-probe spectra
Fixed-scale galaxy occupation degeneracy|rank partial(w,gamma_t)/partial(xi,a0,b1,occupation) at one common action|DES Y1 lens selection and galaxy-shear data
Uncertainty from nonlinear galaxy response|Delta b2 contribution from bispectrum contractions, with candidate density evolution|DES Y1 retained clustering scales
Observed-angle to physical-radius transport|R=D_A(z_l)theta; derivative includes geometry and changed field evaluated at changed R|DES Y1 angular lensing bins and redshifts
Galaxy conservation bias evolution|b(z)=1+[b(z_i)-1]D(z_i)/D(z) only for conserved comoving tracers|DES Y1 multi-bin clustering and explicitly tested selection evolution
Jackknife super-survey blind spot|Cov_JK lacks modes larger than region; compute missing response matrix from survey window|DES Y1 covariance validation products
Joint nuisance prior leverage|Delta theta=F^-1 J_nuis^T C^-1 Delta d with shared calibration prior blocks|DES Y1 photo-z and shape-calibration priors
Weyl-source linear response rank|K_ab=partial O_a/partial source_b; singular vectors distinguish gate occupancy from lensing slip|DES Y1 full 3x2 data vector
Two-shape-catalog conditional replication|L(shape2 given shape1,lenses) includes shared galaxy noise and separate response errors|DES Y1 independently calibrated shape catalogs
Joint-data compression certificate|t=J^T C^-1 d preserves local score only if J includes candidate directions|DES Y1 compressed cosmological constraints versus original joint vector
Clustering increment beyond shear|I_new=I(gg,gk;theta given kk); estimate without counting kk twice|DES Y1 joint report compared with same-year shear report
''')
add(2017,8,r'''
Isotropic BAO ruler map|D_V=[cz D_M²/H]^(1/3); derive conversion from observed pair coordinates|DR14 quasar monopole acoustic feature
Sound-horizon calibration freedom|alpha=(D_V/r_d)/(D_V/r_d)_fid; infer D_V/r_d without importing Planck r_d|DR14 quasar dilation likelihood
Fourier configuration agreement|xi_0(s)=int k²dk P_0(k)j0(ks)/(2pi²) with shared window|DR14 measured monopoles in both representations
Broadband acoustic separation|xi(s)=B xi_wiggle(alpha s)+sum_j a_j s^j; project nuisance span before estimating alpha|DR14 quasar correlation bins
Redshift-error acoustic damping|P_obs=P_true exp[-k² mu² sigma_r²]; infer anisotropic leakage into monopole|DR14 quasar redshift uncertainty
Radial selection integral constraint|delta_obs=delta-W weighted mean(delta); derive BAO estimator offset|DR14 angular and radial selection functions
Shot-noise non-Poisson correction|P_shot=1/n_eff+Delta P_nonPoisson; quantify its acoustic-scale projection|DR14 weighted quasar number density
Window convolution dilation bias|P_tilde(k)=int W(k,kprime)P(alpha kprime)dkprime|DR14 survey mask and measured P0
Cosmology-dependent pair weights|w_FKP=1/[1+n(z)P_ref]; derivative of effective redshift with changed P_ref|DR14 quasar positions and weights
Acoustic peak displacement from damping|xi_w=int P_w exp(-k²Sigma²/2)j0 k²dk/(2pi²); derive peak shift not merely width|DR14 BAO shape and nonlinear nuisance
Mock-covariance precision bias|E[C_hat^-1] differs from C^-1; derive finite-mock likelihood correction|DR14 mock count and covariance dimension to extract
Isotropic anisotropy leakage|P0=int dmu P(k,mu)/2; quantify alpha_perp-alpha_parallel combinations lost|DR14 monopole analysis and selection window
Quasar bias acoustic-phase invariance|b(k) smooth cannot arbitrarily move acoustic phase; bound phase bias from finite smoothness|DR14 broadband clustering and BAO oscillations
Redshift-effective distance approximation|D_eff=integral w(z)D_V(z)dz versus D_V(z_eff); calculate curvature remainder|DR14 broad redshift distribution
BAO from candidate acoustic propagation|r_d=int_zd^infty c_s/H dz; derive candidate H and photon-baryon c_s first|DR14 measured ruler ratio and independently verified baryon inputs
Vacuum density from late distance shape|D_V(z;rho_L,G_cosmo) with a0²=G_N c²rho_L/4; retain coupling ratio|DR14 distance likelihood and common candidate cosmology
Curvature-ruler degeneracy|D_M=S_K(chi); solve rank of partial alpha/partial(K,r_d,H0)|DR14 single-redshift isotropic distance information
North-south cap discrepancy|Delta alpha=alpha_N-alpha_S with cross-covariance from shared calibration|DR14 separate survey-cap data vectors
Fiber-collision pair correction|xi_hat=sum_DD w_pair/RR-2DR/RR+1; quantify nonlocal pair-weight effect|DR14 collision flags and random catalog
Redshift failure environment bias|p_success(delta,z) enters observed bias; estimate correction to BAO phase|DR14 redshift-success metadata
Selection-mock consistency|int W_data P W_data versus W_mock; derive Delta C from mismatched selection|DR14 catalog and mock survey windows
Acoustic detection significance calibration|Delta chi²=chi²_nowiggle-chi²_wiggle; calibrate null with nuisance refitting|DR14 actual acoustic likelihood, not Gaussian significance conversion alone
Distance-ladder incremental combination|L_joint=L_DR14 L_old only after cross-survey overlapping pairs are excluded or covaried|DR14 BAO with prior independent surveys authenticated separately
Broadband growth extraction boundary|P0=b²D²P_initial plus RSD terms; show why alpha does not fix f sigma8|DR14 isotropic acoustic measurement
Isotropic-to-2018 weighted comparison|Delta alpha between weighted anisotropic reconstruction and original monopole with same quasar covariance|DR14 2017 report, reserving 2018 weighted report as dependent comparison
''')
add(2017,9,r'''
Uncalibrated supernova distance map|m_Bcorr=M_B+5log10[d_L(z)/10pc]; derive d_L from candidate null geodesics|Pantheon standardized magnitudes and redshifts
Absolute-magnitude H0 symmetry|M_B -> M_B+5log10 lambda and H0 -> lambda H0 leaves low-z m unchanged|Pantheon unanchored Hubble diagram
Redshift-dependent standardization drift|M_B(z)=M0+epsilon z; profile epsilon against candidate background curvature|Pantheon survey-by-survey standardized residuals
Color-law cosmology covariance|m_corr=m_B+alpha x1-beta c+Delta_host; retain covariance of beta with distances|Pantheon light-curve color/stretch fits
Host-mass step uncertainty|Delta_host=gamma H(log M_host-M_cut); propagate uncertain host masses|Pantheon host classifications and distance residuals
Survey-zero-point covariance|delta m_i=sum_s A_is delta Z_s; C_Z=A Cov(Z)A^T|Pantheon cross-survey calibration systematics
Peculiar-velocity correlated errors|C_mu,ij=(5/ln10)² Cov(v_i,v_j)/(cz_i cz_j) at low z|Pantheon low-redshift positions and velocity model
Lensing magnification skew|mu_obs=mu_true-2.5log10 magnification; derive non-Gaussian distance likelihood|Pantheon high-redshift residual distribution
Selection truncation normalization|L_i=p(m_i given z_i,theta)S(m_i,z_i)/integral p(m given z_i,theta)S dm|Pantheon detection and spectroscopic-selection functions
Flux versus magnitude averaging|E[log F] differs from log E[F]; derive bias with measurement and lensing scatter|Pantheon photometry and binning choices
Distance duality conditional test|eta_D=d_L/[(1+z)²D_A]; require external independent angular distances|Pantheon luminosity distances and separately authenticated BAO geometry
Expansion deceleration reconstruction|q(z)=(1+z)Hprime/H-1 inferred through regularized d_L derivatives|Pantheon relative distance-redshift curve
Curvature-free acceleration witness|derive integrated distance inequality for q>=0 with explicit curvature assumptions|Pantheon Hubble diagram and calibrated uncertainty
Vacuum scale versus dark-energy evolution|a0(z)²/a0(0)²=rho_DE(z)/rho_DE(0) only under adopted fixed kappa,G_N|Pantheon relative expansion constraints under candidate dynamics
Canonical-alternative distance footprints|Delta mu(z)=5log10[dL_alt(z)/dL_can(z)] with densities changed consistently|Pantheon redshift coverage and full residual covariance
Supernova gravity dependence|M_Ch proportional to G_star^-3/2 is a conditional scaling; derive luminosity response before ladder use|Pantheon standard-candle residuals and stellar-physics dependency
Spectroscopic redshift convention audit|1+z_total=(1+z_cos)(1+z_pec)(1+z_grav); propagate correction order|Pantheon heliocentric/CMB-frame redshift fields
Outlier mixture and gravity-tail robustness|L=(1-f_out)N(mu,C)+f_out t_nu; infer candidate shift under mixture alternatives|Pantheon extreme residuals and quality flags
Intrinsic-scatter model transport|C_int(theta_scatter) enters light-curve bias correction and cosmology jointly|Pantheon scatter-model alternatives
PS1 incremental information|I_PS1_given_old=I(full)-I(old) with overlapping supernova IDs removed|Pantheon PS1 addition to historical samples
Redshift-binned zero-point null modes|find v with A_cal^T C^-1 v=0 and maximize v^T partial_theta mu|Pantheon calibration matrix and redshift bins
Observer acceleration dipole|delta mu(n,z)=D(z) a_obs dot n; separate from peculiar velocity and survey anisotropy|Pantheon sky coordinates and distance residuals
FLRW consistency residual|R(z)=H(z)d[D_M]/dz-c sqrt(1-KD_M²); compare only after external H authentication|Pantheon D_M inferred conditionally from distances
Posterior compression loss|compare likelihood of candidate mu(z) in full covariance with compressed w0-wa representation|Pantheon released distance vector versus published dark-energy contours
Supernova-to-vacuum bridge limit|rho_L inferred only from candidate Friedmann equation; prove which combinations remain unidentified by relative magnitudes|Pantheon absolute-scale degeneracy and both G_N/G_cosmo symbols
''')
add(2017,10,r'''
Angular acoustic ruler projection|theta_BAO=r_d/D_M(z) only for narrow bins; integrate actual n(z) kernel|DES Y1 photometric BAO galaxy distribution
Photometric smearing operator|w(theta)=int dz1 dz2 n(z1)n(z2)xi[r(theta,z1,z2)]|DES Y1 photo-z distributions and angular pair counts
Angular versus harmonic dilation|C_l=2pi int dcos(theta)w(theta)P_l(cos theta); preserve common mask|DES Y1 angular and spherical-harmonic BAO estimators
Transverse separation conversion|s_perp=D_M,fid(z)theta; derive alpha mapping with broad photo-z bins|DES Y1 comoving-transverse BAO estimator
Template versus machine-learning photo-z|Delta alpha=alpha_template-alpha_ML with shared-object covariance|DES Y1 two redshift-estimation pipelines
Mean photo-z acoustic shift|delta alpha=(partial alpha/partial delta z)delta z; derive derivative from projected acoustic kernel|DES Y1 calibrated mean-redshift errors
Photo-z width degeneracy|d w/dsigma_z versus d w/dalpha; compute nuisance-orthogonal acoustic score|DES Y1 uncertainty-width calibration
Catastrophic-redshift alias peaks|n(z)=(1-f)n_main+f n_alias; derive cross-term acoustic features|DES Y1 redshift-distribution tails
Projected broadband marginalization|w(theta)=B w_acoustic(alpha theta)+A0+A1/theta+A2/theta² with basis validity tested|DES Y1 angular BAO bins and range
Survey-mask acoustic mode loss|C_tilde_l=M_llprime C_lprime; characterize singular modes near acoustic oscillations|DES Y1 angular footprint
Color-magnitude selection gravity bias|S(color,m,z) induces b_eff(z); propagate selection into acoustic weighting|DES Y1 BAO-optimized galaxy sample
Angular integral constraint|w_meas=w_true-C_window; compute C_window with acoustic template|DES Y1 random catalog and mask
Finite-mock angular covariance|derive posterior for covariance from mocks rather than fixing inverse sample covariance|DES Y1 mock ensembles and estimator dimension
Correlated redshift-slice combination|alpha_joint from block covariance C_ij; compare to falsely independent slice weights|DES Y1 neighboring photometric bins
Distance ratio mass-density bridge|D_A/r_d from candidate H(z;rho_L,G_cosmo), while a0 fixes G_N rho_L|DES Y1 measured angular distance-ruler ratio
Curvature contribution at effective redshift|D_A=S_K(chi)/(1+z); derive second-order K expansion over source support|DES Y1 photometric-redshift kernel
Redshift evolution compression remainder|R=w_integrated-w_at_zeff; bound R projection onto acoustic dilation|DES Y1 broad redshift support
Magnification-induced angular acoustic distortion|delta_g=b delta+(5s-2)kappa; evaluate density-lensing acoustic cross term|DES Y1 count slopes and angular clustering
BAO-shear shared-footprint covariance|Cov(w_BAO,xi_shear) from common density modes and source overlap|DES Y1 BAO and shear reports; covariance extraction needed
BAO-clustering sample-overlap audit|Cov(w_BAO,w_redMaGiC) computed with shared objects and sky modes|DES Y1 BAO versus 3x2 lens sample IDs
Angular-radial anisotropy information ceiling|rank partial w/partial(alpha_perp,alpha_parallel) under photo-z smoothing|DES Y1 projected clustering only
Acoustic phase versus gravity growth|P_w(k,z)=D²(k,z)P_w,initial(k); identify scale-dependent growth shifting projected extrema|DES Y1 measured angular acoustic shape
Estimator-consensus without triple counting|combine three estimator summaries with singular shared-data covariance, or select one|DES Y1 angular/transverse/harmonic results
Release-specific acoustic null ensemble|generate no-wiggle projected fields with same n(z),mask,selection and refit nuisance|DES Y1 measured acoustic-significance procedure
Photometric-spectroscopic BAO bridge|R=[D_M/r_d]_DES/[D_V/r_d]_QSO with distinct z kernels and common ruler cancellation|DES Y1 angular BAO and 2017 DR14 quasar report
''')
add(2018,1,r'''
Temperature acoustic transfer|C_l^TT=4pi int dlnk P_R(k)abs(Delta_l^T)^2; derive Delta_l from candidate perturbations|Planck 2018 temperature spectra and foreground model
Polarization acoustic transfer|C_l^EE=4pi int dlnk P_R(k)abs(Delta_l^E)^2|Planck E-mode spectra, beams and polarization calibration
Temperature-polarization phase|C_l^TE=4pi int dlnk P_R Delta_l^T Delta_l^E; test peak-zero alignment|Planck TE spectrum and full TT/TE/EE covariance
Baryon-loading odd-even contrast|R_b=3rho_b/(4rho_gamma); derive odd/even peak response without a dark-particle addition|Planck acoustic peak amplitudes and verified baryon inputs
Early integrated Sachs-Wolfe response|Delta_T,ISW=int (Phi_prime+Psi_prime)j_l[k(eta0-eta)]deta|Planck first acoustic peaks and candidate potential evolution
Diffusion-scale consistency|r_D²=int d eta/[6 dot tau] times baryon-loading factor derived from transport|Planck damping tail and recombination inputs
Acoustic-scale geometry|theta_star=r_s(zstar)/D_M(zstar); separate background and sound-speed changes|Planck angular acoustic scale and candidate recombination epoch
Optical-depth amplitude degeneracy|high-l TT proportional to A_s exp(-2tau); use low-l EE for independent tau direction|Planck low-E and high-l spectra
Reionization-shape freedom|tau=int c sigma_T n_e dt; vary x_e(z) within physical bounds|Planck large-angle polarization
Effective lensing smoothing anomaly|C_l,lensed=L[C_unlensed,C_phi]; infer smoothing response distinct from four-point lensing|Planck peak smoothing and separately anchored lensing report
Primordial-tilt gravity degeneracy|partial C_l/partial n_s versus partial C_l/partial candidate response; compute score angle|Planck broad multipole spectra
Isocurvature transfer diagnostic|C_l=sum_ab P_ab Delta_l^a Delta_l^b; permit only fields present in pinned action|Planck acoustic phase/coherence and explicit initial-condition space
Newton-cosmological G distinction|H² contains G_cosmo while a0²=G_N c²rho_L/4; derive C_l response to ratio|Planck spectral likelihood, not quoted GR density parameters
Vacuum-density posterior transport|p(rho_L given spectra,candidate) must be refit; p_GR(Omega_L,H0) is not universal|Planck likelihood dependencies and published parameter chains
Homogeneous versus finite-mode closure|solve k=0 background separately from lim_k->0 perturbation equations|Planck distance and low-l support with candidate action
Neutrino-sector fixed-content audit|rho_nu and anisotropic stress only from declared ordinary species; no silent extra relics|Planck damping and phase-shift information
Recombination clock rescaling|zstar determined by rate/H competition; propagate modified H into visibility g(eta)|Planck acoustic peaks and atomic reaction inputs
Foreground spectral separation|d_nu=CMB+sum_c A_c f_c(nu); derive gravity-score projection after nuisance marginalization|Planck multifrequency spectral products if obtained
Beam eigenmode covariance|delta C_l=sum_a b_a E_al C_l; retain correlated beam uncertainty|Planck beam-calibration products
Temperature-polarization calibration ratio|C_TE scales g_T g_E and C_EE scales g_E²; estimate identifiable ratio|Planck cross-frequency TT/TE/EE spectra
Curvature-geometric degeneracy|keep theta_star fixed while varying K,H0,rho_L; identify residual lensing response|Planck spectra with separate reconstruction likelihood
Matter transfer without CDM shortcut|derive T_b(k,eta) from candidate coupled baryon-carrier equations and compare C_l|Planck measured acoustic spectrum and candidate carrier revision
Late-time potential decay|Delta C_l^TT from low-z ISW kernel; distinguish cosmic variance from model mismatch|Planck large-angle temperature spectrum
Canonical-alternative CMB consistency|compare likelihoods at two fixed rho_L values implied by separate a0 normalizations|Planck spectra with all remaining candidate parameters shared
Planck posterior compression sufficiency|test whether (theta_star,omega_b,As,tau) preserves candidate likelihood tangent directions|Planck full spectral likelihood versus compressed summaries
''')
add(2018,2,r'''
Quadratic-estimator candidate response|phi_hat_L=A_L int d²l g(l,L-l)T_l T_(L-l); rederive normalization for candidate C_l|Planck lensing reconstruction and fiducial response
Disconnected bias transport|N0_candidate-N0_fid from changed two-point spectra; retain realization dependence|Planck lensing noise-bias products
Connected lensing bias|N1_L depends on C_L^phiphi; iterate candidate spectrum instead of fixed subtraction|Planck four-point spectrum and bias templates
Lensing Weyl line integral|phi(n)=-int dchi (chi_star-chi)/(chi_star chi)(Phi+Psi)/c²|Planck reconstructed lensing-potential modes
Low-L reconstruction boundary|window-convolved C_L^phiphi at L near lower cut; derive leakage from excluded modes|Planck retained lensing multipoles
Polarization-only lensing check|C_phi,EB compared conditionally with C_phi,TT using shared sky covariance|Planck separate temperature/polarization estimators
Minimum-variance combination weights|w=N^-1 1/(1^T N^-1 1); update off-diagonal estimator noise|Planck lensing estimator covariance
Curl-mode null|Omega_hat from parity-odd deflections; derive expected zero for scalar Born lensing|Planck curl reconstruction availability
Mask mean-field contamination|phi_hat=phi+MF_mask+noise; estimate residual MF dependence on candidate sky|Planck mask and reconstruction simulations
Point-source trispectrum bias|Delta C_L from connected source four-point function; project onto gravity response|Planck foreground masks and source nuisance templates
CIB cross-lensing transfer|C_phi,I=int W_phi W_I P_Weyl,emissivity; separate biased emissivity from gravity|Planck lensing-CIB combination described in report
Delensing response consistency|C_l,delensed=L[C_unlensed,(1-r_L²)C_phi] with residual-noise corrections|Planck measured delensing effect
Reconstruction versus peak-smoothing covariance|Cov(C_phi,C_TT) from shared modes and lensing response|Planck lensing and parameter reports without double counting
Matter-Weyl coupling test|k²(Phi+Psi)=-8pi G_N a²Sigma rho delta; derive Sigma from candidate|Planck lensing-potential spectrum and source evolution
Lensing kernel redshift localization|R(z)=delta C_L^phiphi/d log P_Weyl(k,z); calculate redshift sensitivity eigenmodes|Planck multipole bins and distance kernel
Born-approximation remainder|Delta phi_postBorn from iterated geodesic deflection; bound at measured L support|Planck lensing power and candidate potentials
Observer-source boundary term|derive potential/velocity endpoint contributions to lensing map and monopole removal|Planck reconstruction convention
Filter-scale CMB-lensing imprint|partial C_L^phiphi/partial xi including response of growth and ray kernel|Planck lensing spectrum and pinned heat filter
Carrier anisotropic-stress signature|Phi-Psi from varied stress; evaluate resulting C_phi at fixed density growth|Planck lensing versus temperature-derived growth
Lensing amplitude shape separation|C_L=A_phi C_ref,L exp(sum q_a e_a(L)); infer shape modes orthogonal to amplitude|Planck binned lensing spectrum covariance
Nongravitational foreground hardening|phi_BH=phi_hat-R_phi,s R_s,s^-1 s_hat; derive response and variance|Planck foreground-sensitive reconstruction channels
Lensing-only distance degeneracy|det partial C_phi/partial(H0,As,rho_L) after marginalizing shape; identify null directions|Planck lensing-only inference and stated weak priors
Galaxy-lensing shared-mode combination|Cov(C_phi,DES shear) from overlapping sky and common Weyl modes|Planck lensing report and DES Y1 overlap mask
Vacuum normalization independent of spectra fit|hold a0 fixed per footing, infer remaining lensing response without floating rho_L independently|Planck lensing likelihood and scale identity
2015-to-2018 reconstruction increment|Delta C_phi corrected for shared sky/noise; isolate new polarization information|Planck 2018 report and separately authenticated earlier release
''')
add(2018,3,r'''
Parallax-to-distance likelihood|p(varpi given r)=N(1/r+zeta,C_varpi); integrate distances rather than invert noisy parallaxes|Gaia DR2 parallaxes and covariance
Proper-motion acceleration map|v_t=4.74047 mu d in compatible units; propagate parallax-motion covariance|Gaia DR2 astrometric vectors
Wide-binary relative-speed statistic|vtilde=v_rel/sqrt(G_N M/r_proj); derive projection distribution from orbital phase|Gaia DR2 paired astrometry and photometric masses
Wide-binary chance-alignment mixture|L=(1-f)L_bound+f L_field in position-velocity space|Gaia DR2 local phase-space density
Astrometric binary contamination|mu_fit=mu_CM+Delta x_photocenter/Delta t; bound unresolved orbital bias|Gaia DR2 fit quality and astrometric baseline
Parallax spatial-covariance floor|Var(mean varpi)=sum_ij w_i w_j C_varpi(theta_ij)|Gaia DR2 cluster/member astrometry
Vertical Jeans force inversion|K_z=-(1/nu)partial_z(nu sigma_z²)-(1/Rnu)partial_R(Rnu sigma_Rz)|Gaia DR2 stellar velocities and selection-corrected density
Radial Jeans circular-speed map|v_c²=mean v_phi²-sigma_R²-partial_logR(nu sigma_R²)/nu with tilt term retained|Gaia DR2 disc phase-space sample
Non-equilibrium vertical phase spiral|phase(theta_z,J_z,t)=theta_z0+Omega_z(J_z)t; infer potential only with perturbation clock|Gaia DR2 z-vz distribution
Escape-speed truncation|p(v given r) proportional to [v_esc(r)-v]^k times selection, convolved with errors|Gaia DR2 high-velocity stars
Stellar-stream track acceleration|d²x/dt²=-grad Phi only for orbit track; quantify stream-orbit offset|Gaia DR2 stream proper motions
Globular-cluster bulk motion|v_CM from membership mixture with internal rotation and perspective expansion|Gaia DR2 cluster astrometry and radial velocities
Perspective acceleration nuisance|dot mu=-2v_r mu/d under rectilinear motion; separate from gravitational curvature|Gaia DR2 proper motions and radial velocities
Solar-reflex dipole removal|v_obs=v_Gal-v_sun; infer correlated uncertainty across stellar force estimates|Gaia DR2 sky-wide kinematics
Radial-velocity selection bias|p(v_r given selected)=p(v_r)S(m,color,sky)/normalization|Gaia DR2 radial-velocity sample selection
Photometric mass-to-light gravity ambiguity|M_star=Upsilon(color,age) L(d); propagate common distance scaling into g_N|Gaia DR2 binary/cluster photometry
External-field wide-binary response|solve filtered MONO with boundary grad u=g_ext; project force anisotropy onto binary orientations|Gaia DR2 wide-binary sky geometry
Heat-filter binary finite-source limit|S rho_star versus point-source limit; bound xi-dependent force at measured separations|Gaia DR2 separation distribution and stellar radii dependency
Cluster virial surface pressure|2K+W=3P_s V+time derivative of inertia; determine measurable remainder|Gaia DR2 cluster dispersions and member radii
Galactic rotation disequilibrium|radial Euler/Jeans includes partial_t(nu mean v_R); bound bias from streaming patterns|Gaia DR2 radial streaming map
Action-space potential consistency|J_i=(1/2pi)oint p_i dq_i; compare clump compactness across fixed candidate potentials|Gaia DR2 phase-space substructure
Asteroid geodesic residual map|delta theta(t)=projection delta x(t)/distance with observer ephemeris uncertainty|Gaia DR2 solar-system epoch astrometry
Reference-frame spin coupling|mu_obs=mu_true+omega_frame cross n; propagate into Galactic rotation and binary tests|Gaia DR2 quasar frame calibration
DR1-to-DR2 acceleration fallacy|Delta mu/Delta t includes shared-baseline solution and calibration terms, not direct acceleration alone|Gaia DR2 versus authenticated DR1 source matches
Kinematic vacuum-scale identifiability|rank partial phase-space likelihood/partial(a0,xi,Upsilon,distance_zero_point)|Gaia DR2 gravity samples under both fixed a0 footings
''')
add(2018,4,r'''
S2 combined redshift observable|1+z=(u_mu k^mu)_emit/(u_mu k^mu)_obs; expand through v²/c² and Phi/c²|GRAVITY S2 astrometry and spectroscopy
Gravitational versus transverse-Doppler separation|z_rel=v²/(2c²)-Phi/c²; characterize covariance of the two contributions|S2 pericentre velocity and position time series
Pericentre redshift time asymmetry|A_z(t)=z(t_p+t)-z(t_p-t); separate orbital geometry and instrumental drift|S2 spectroscopy around May 2018
Astrometric angular-to-mass scaling|theta=a_phys/R0 and P²=4pi²a_phys³/(G_orb M); derive degeneracy|S2 sky orbit and radial velocities
Light-travel-time orbit correction|t_obs=t_emit+R_parallel(t_emit)/c+Delta_Shapiro; solve implicit time map|S2 rapid pericentre motion
Extended-mass redshift perturbation|deltaPhi(r)=-int_r^infty G_N M_ext(s)/s² ds; include finite boundary|S2 orbital radius support and stellar-cusp constraints
MONO high-acceleration orbit correction|delta a(r) from filtered spherical solution; integrate variational equations along S2 orbit|S2 pericentre and apocentre astrometry
Filter versus central point-source model|compute S delta³(x) and resulting finite-xi force; establish valid central-source limit|S2 minimum orbital radius and candidate heat scale
Spectrograph zero-point hierarchy|v_meas=v_orbit+Z_instrument+drift_instrument(t)|S2 multi-instrument radial velocities
Astrometric reference-frame acceleration|theta_obs=theta_orbit+theta0+mu0 t+(1/2)a_frame t²|S2 long-baseline astrometry
Relativistic-redshift coefficient portability|z=z_Newton+f z_rel,GR is valid only if candidate correction has same temporal shape|S2 reported f posterior and raw trajectory if obtained
Post-Newtonian pericentre forecast|Delta omega=6pi GM/[a(1-e²)c²] only in GR limit; derive candidate correction|S2 orbit posterior; later precession data excluded from 2018 fit
Photon versus massive-star metric|derive star geodesic from matter action and photon ray independently, then compare z(t)|S2 astrometry/spectroscopy from one physical metric
Relativistic beaming line bias|observed line centroid weighted by surface intensity and Doppler beaming; bound stellar-systematic shift|S2 spectra and stellar-atmosphere dependency
Binary-star redshift mimic|v_S2=v_CM+K_bin[cos(n_bin t+phi)+e cos omega]; constrain unobserved companion|S2 spectral residuals and cadence
R0 versus redshift coefficient degeneracy|F_f,R0 from joint angular and radial data; report nuisance-orthogonal f score|S2 astrometric/spectroscopic covariance
Finite observer-potential correction|z_endpoint=(Phi_obs-Phi_emit)/c² with common constant absorbed into spectral zero point|S2 observer and barycentric correction conventions
Preferred-frame orbital torque|dot L=r cross delta a_pref; predict nodal and redshift signatures jointly|S2 orbital orientation and candidate preferred foliation
Stellar tidal line-shift boundary|Delta z_tide from intensity-weighted surface velocities; compare with gravitational template|S2 pericentre spectra and stellar structure
Calibration-versus-physical error split|C=C_stat+C_sys with correlated instrument blocks; compare to quadrature scalar error|S2 quoted statistical/systematic redshift uncertainties
No-slip local metric test scope|S2 z probes Phi while astrometric ray bending probes Phi+Psi; derive rank of joint sensitivity|S2 imaging and spectroscopic measurements
Adiabatic vacuum background matching|match local Sgr A* metric to cosmological rho_L boundary; quantify r/Hubble corrections|S2 orbital scale and fixed framework vacuum
Pericentre data incremental likelihood|L_new=L(pre-2018,2018)/L(pre-2018) with shared nuisance retained|S2 historic orbit plus new pericentre observations
GRAVITY versus future Keck covariance plan|separate telescope noise but share orbit,reference stars and astrophysical nuisance|S2 2018 report; reserve 2019 independent observing report
Strong-field-to-galaxy same-action match|derive overlap region between central metric and filtered MONO outer branch without assigning potentials|S2 orbit likelihood and candidate action boundary conditions
''')
add(2018,5,r'''
DF2 discrete tracer likelihood|L=product_i N(v_i given v_sys,sigma_los²(R_i)+epsilon_i²)|DF2 globular-cluster-like velocities and errors
Dispersion near-zero boundary|sigma>=0; compare profile likelihood and prior-dependent posterior at zero|DF2 low observed tracer velocity spread
Single-tracer influence|Delta sigma_-i=sigma_all-sigma_without_i using refitted systemic velocity|DF2 individual tracer radial velocities
Membership contamination mixture|L_i=p_i L_member+(1-p_i)L_foreground|DF2 tracer positions, spectra and photometry
Distance rescaling of MONO dispersion|M_star proportional to D²; r proportional to D; derive sigma_los(D) from field plus Jeans equations|DF2 distance-dependent luminosity and size
External-field host geometry|g_ext=grad Phi_host at unknown three-dimensional group separation|DF2 projected position relative to NGC1052 and group distance uncertainty
Anisotropic Jeans degeneracy|d(nu sigma_r²)/dr+2beta nu sigma_r²/r=-nu dPhi/dr|DF2 tracer density and sparse line-of-sight velocities
Finite-aperture projected dispersion|Sigma sigma_los²=2int_R^infty (1-beta R²/r²)nu sigma_r² r dr/sqrt(r²-R²)|DF2 actual tracer radii and light profile
External-field orientation projection|sigma_los(n)=n_i sigma_ij n_j with anisotropic filtered potential|DF2 shape and line-of-sight orientation uncertainty
Tidal-equilibrium validity|t_cross=r/sigma versus t_tide=abs(g_ext/dot g_ext); derive stationarity criterion|DF2 size, velocities and host orbit dependency
Baryonic mass-to-light uncertainty|g_N(r)=G_N Upsilon L(<r)/r² with stellar-population prior|DF2 photometry and independently sourced population constraints
Tracer rotation subtraction|v_i=v_sys+V_rot sin(theta_i-theta0)+noise|DF2 sky positions and radial velocities
Globular-cluster dynamical friction|dot E=-F_df dot v derived for candidate wake response, not Chandrasekhar import|DF2 luminous tracer masses and radii
Small-sample coverage calibration|P_theta[theta in interval(d)] estimated under exact heteroscedastic tracer sampling|DF2 sample geometry and measurement errors
Pressure-boundary contribution|nu sigma_r²(r)=int_r^rt nu g dr plus P_boundary term|DF2 finite tracer extent and outer-pressure uncertainty
Non-spherical light deprojection|rho_b obtained from axisymmetric projected brightness with inclination family|DF2 imaging ellipticity and radial profile
Heat-filter tidal survival|solve S on host-plus-satellite domain; compare internal-force eigenvalues with tidal tensor|DF2 host geometry and baryonic distribution
Deep-equilibrium coefficient audit|sigma²=C/2 conditional target; derive aperture conversion rather than equating it to observed sigma_los²|DF2 tracer aperture and baryonic mass
Acceleration-scale fixed-footing comparison|Delta log L=L(a0_can)-L(a0_alt) with identical distance,Upsilon,environment priors|DF2 velocity likelihood and fixed framework scales
Group peculiar-velocity distance ambiguity|v_recession=H0 D+v_group; do not infer D from recession speed alone|DF2 group radial velocities and distance indicators
Velocity-error floor calibration|epsilon_i² -> epsilon_i²+s_floor²; infer identifiable floor versus intrinsic dispersion|DF2 spectral uncertainty model
Outermost-tracer leverage|kernel K_i(r)=delta sigma_los(R_i)/delta g(r); locate genuinely measured acceleration range|DF2 radial sampling pattern
Apparent dark-mass estimator portability|M_est=k R sigma²/G_N has k depending on profile,beta,boundary; derive k candidate-specifically|DF2 published mass inference and underlying observables
DF2 discovery selection conditioning|p(d given selected,theta)=p(d,selected given theta)/P(selected given theta)|DF2 low-surface-brightness discovery and tracer-selection criteria
DF2-to-DF4 shared-environment prediction|predict p(sigma_DF4 given DF2,host) before using DF4 velocities, sharing host field|DF2 2018 report; future distinct galaxy test requires 2019 source
''')
add(2018,6,r'''
Triple differential-acceleration forcing|ddot r_inner=F_inner+Delta_SEP g_outer(t); derive Delta_SEP from body sensitivities|J0337 pulse arrival times and triple orbital geometry
Nordtvedt timing sidebands|delta t=sum_nm A_nm cos(n omega_inner t+m omega_outer t); derive SEP-selected harmonics|J0337 timing cadence and measured orbital frequencies
Strong-body sensitivity derivation|s_A=-partial log m_A/partial log G_eff at fixed baryon number|J0337 neutron-star and white-dwarf composition plus stellar-equilibrium dependency
Outer-orbit tidal contamination|delta a_tide=T_outer r_inner; distinguish quadrupolar tide from differential uniform acceleration|J0337 hierarchical orbital timing solution
Three-body action conservation|sum_A m_A a_A=0 internally only after all interaction terms are varied|J0337 timing residuals and candidate three-body Hamiltonian
Inner-orbit eccentricity polarization|e_forced proportional to Delta_SEP g_outer/(n_inner² a_inner) with resonance denominator derived|J0337 eccentricity-vector timing terms
Romer-delay geometry|Delta_R=-n dot r_pulsar/c; derive perturbed trajectory timing signature|J0337 pulse arrivals and astrometric direction
Shapiro-delay contamination|Delta_S=-2G_light m/c³ log(1-s sin phase) as GR-limit diagnostic|J0337 conjunction timing and inclination covariance
Einstein-delay clock contribution|Delta_E=int[(v²/2-Phi)/c²]dt with constants and signs fixed by proper time|J0337 orbital clock modulation
Outer-white-dwarf mass degeneracy|F_Delta,mouter after joint timing fit; quantify forcing-mass covariance|J0337 outer-orbit mass function
Red-noise versus SEP harmonics|C=C_white+C_red; project SEP template through C^-1|J0337 timing-noise spectrum and long-baseline sampling
Ephemeris-induced annual residual|delta t=-n dot delta r_Earth/c; retain annual leakage into orbital harmonics|J0337 barycentric timing corrections
Dispersion-measure chromatic separation|Delta t_DM=K_DM DM(t)/nu_radio² versus achromatic SEP signal|J0337 multi-frequency arrival times
Preferred-frame inner-orbit polarization|delta a_pref from action u_pref and orbital velocity; derive distinct harmonic basis|J0337 triple orbital orientation and sky motion
Strong versus weak EP parameter split|Delta_SEP=Delta_weak+(s_NS-s_WD)q_strong; identify measured combination|J0337 timing bound and independent MICROSCOPE information
Finite-size white-dwarf quadrupole|Q_ij produces delta a proportional to Q/r⁴; derive timing-phase contamination|J0337 white-dwarf spin and radius dependencies
Heat-filter hierarchical force matching|apply S to complete triple source, not pairwise scalar nu; quantify non-superposition|J0337 measured inner/outer separation hierarchy
High-acceleration recovery residual|delta a/a from exact MONO continuation at both orbital scales|J0337 orbital frequencies and mass/length likelihood
Orbit-averaging remainder|R=integral exact forcing minus secular averaged forcing over timing window|J0337 cadence and hierarchical periods
Pulse-profile evolution timing bias|delta TOA from frequency/time-dependent template shape; project onto SEP mode|J0337 pulse profiles if available
Timing-model projection loss|R_proj=I-M(M^T C^-1 M)^-1 M^T C^-1; apply to SEP template|J0337 fitted spin/orbital timing design matrix
Response derivative validation|partial TOA/partial Delta from variational ODE versus symmetric finite differences|J0337 reference timing solution and actual cadence
Relativistic three-body cross terms|terms proportional to G²m_A m_B/(r_AB r_AC c²) derived from candidate action|J0337 timing precision and hierarchical positions
Triple-to-galaxy external-field bridge|derive relation, if any, between body sensitivity Delta_SEP and filtered weak-field external response|J0337 SEP limit and pinned MONO branch
SEP constraint admissible-action set|B={action cells whose marginalized timing likelihood survives}; keep canonical/alternative rho_L distinct|J0337 differential-acceleration measurement and declared matter coupling
''')
add(2018,7,r'''
Eleven-year common red-process likelihood|C_ab=C_noise,a delta_ab+Gamma_ab S_common; derive Gamma from tensor response|NANOGrav 11-year timing residuals
Hellings-Downs response derivation|Gamma_ab=int dOmega sum_A F_a^A F_b^A with pulsar terms retained until approximation justified|NANOGrav pulsar sky positions and timing baselines
Ephemeris dipole separation|C_SSE,ab=n_a^i Cov(delta r_i,delta r_j)n_b^j/c²|NANOGrav ephemeris-sensitive residual correlations
Clock monopole separation|C_clock,ab=C_clock(t,tprime) independent of pulsar angle|NANOGrav shared-clock timing residuals
Upper-limit prior transport|p(A given d) proportional to L(A)pi(A); compare uniform-A and log-A bounds explicitly|NANOGrav reported background limit and original prior
Power-law strain energy conversion|Omega_GW(f)=2pi² f² h_c²/(3H0²) only after tensor-energy convention derived|NANOGrav strain-amplitude limit and candidate G_rad
Finite-span spectral leakage|C_ab(t_i,t_j)=int df P(f)cos[2pi f(t_i-t_j)]Gamma_ab with low-frequency cutoff tested|NANOGrav irregular 11-year cadence
Pulsar red-noise confounding|P_a(f)=A_a² f^-gamma_a plus common component; compute identifiable combinations|NANOGrav per-pulsar noise constraints
Dispersion-measure noise projection|r_DM=K_DM DM(t)/nu²; propagate chromatic residual covariance into common spectrum|NANOGrav multi-band observations
Solar-wind timing contamination|DM_SW=int n_e,SW dl; derive seasonal cross-pulsar angular structure|NANOGrav observing geometry and solar elongation
Pulsar-term coherence boundary|phase_p=2pi f L_p(1+n dot p)/c_T; quantify distance uncertainty averaging|NANOGrav pulsar distances and Fourier support
Tensor propagation dispersion in PTA|Gamma_ab(f;c_T(f)) from exact Earth/pulsar transfer functions|NANOGrav cross-correlation data and fixed two-tensor action
Spectral turnover source interpretation|h_c=f^-2/3 [1+(f_b/f)^kappa]^-1/2 as diagnostic; derive f_b from candidate binary hardening|NANOGrav low-frequency upper-limit shape
Binary environmental hardening map|df/dt=df/dt_GW+df/dt_env; derive n(f) proportional to 1/(df/dt)|NANOGrav strain limits and independent galaxy-core inputs
Eccentric harmonic background|h_c²(f)=sum_n int dz dM n_sources h_n²(f/n)|NANOGrav spectral sensitivity with candidate binary dynamics
Solar-system mass perturbation score|delta r_SSB=sum_p delta m_p r_p/M_total; map planetary-mass uncertainty into timing|NANOGrav ephemeris nuisance design
Jupiter-orbit covariance with common process|F_A,J=Tr(C^-1 C_,A C^-1 C_,J)/2|NANOGrav long-period timing residuals
Single-pulsar dominance diagnostic|Delta logL_-a compared using conditional predictive probability|NANOGrav pulsar-level residual/noise products
Pair-angle information rank|rank Gamma_basis on measured pulsar pair angles; bound distinguishability of monopole,dipole,quadrupole|NANOGrav 11-year sky coverage
Timing-fit low-frequency attenuation|P_post=R_timing P_pre R_timing^T; derive transfer for spin and astrometry fitting|NANOGrav timing design matrices
Fourier-basis truncation bias|Delta C from omitted frequencies; bound induced amplitude posterior shift|NANOGrav residual spectrum and actual sampling
Background stationarity test|C(t,tprime)=C(t-tprime) versus epoch-dependent amplitude; compare segment-conditioned predictions|NANOGrav 11-year observation epochs
Nine-to-eleven-year information increment|L_new=L_11/L_9 only with compatible shared-data noise and calibration|NANOGrav new release versus earlier timing span
No-new-species background interpretation|map strain constraint into tensor stress of existing action; avoid importing cosmic strings as framework matter|NANOGrav stochastic upper limit and candidate field inventory
Preferred-time PTA causality scope|retarded timing response must be ordered in global preferred time even if c_T diagnostic varies|NANOGrav pulsar-Earth transfer and criterion-B candidate
''')
add(2018,8,r'''
GW170729 new-event source map|derive h(f;M,chi,dL) for candidate then refit this newly reported event|GWTC-1 GW170729 strain/posterior with GR assumptions explicit
GW170809 new-event coherence|R_coh=min_theta sum_I norm(d_I-h_I(theta))² on this event|GWTC-1 GW170809 detector data
GW170818 new-event network rank|singular values of noise-whitened F_T at this event sky support|GWTC-1 GW170818 network information
GW170823 new-event merger residual|delta h_merger=d-h_candidate with source and calibration covariance|GWTC-1 GW170823 signal
Catalog selection normalization|L_pop=exp(-N_exp)product_i integral L_i(theta)p_pop(theta)dtheta; derive N_exp|GWTC-1 search selection and observing time
Search-pipeline union efficiency|p_det,union=1-P(no search detects); include correlated pipeline outcomes|GWTC-1 three-search candidate tables
Marginal-event astrophysical mixture|L_i=p_astro L_signal+(1-p_astro)L_noise; do not promote candidates to detections|GWTC-1 marginal-event list and search statistics
O1-O2 calibration hierarchy|deltaC_run shared among events within run; derive joint waveform likelihood|GWTC-1 homogeneous reanalysis products
Mass-spectrum propagation bias|p(m_detector) transported through candidate z(dL),selection and Jacobian|GWTC-1 detector-frame mass-distance information
Spin-population prior feedback|p(chi_eff given hyperparameters) changes single-event gravity-score marginalization|GWTC-1 spin posteriors and original sampling priors
Two-normalization catalog compatibility|same a0 and action cell across all events; compare joint likelihood per fixed footing|GWTC-1 event likelihoods with common theory parameters
Merger-rate model dependence|R=N/(VT) only for assumed source distribution; derive VT under candidate amplitude transport|GWTC-1 rate inference and injection-selection dependency
Neutron-star-black-hole nondetection|P(N=0)=exp[-R_NSBH VT_NSBH]; recalculate VT before transporting rate bound|GWTC-1 nondetection and search sensitivity
BNS versus BBH transport ratio|R_d=dL_GW,BNS/dL_GW,BBH at matched z depends on source calibration and selection|GWTC-1 event classes and waveform assumptions
Event reanalysis incremental covariance|Delta theta_new-old with common strain; no multiplication of old and new posteriors|GWTC-1 versus 2017 event reports
Posterior-sample likelihood recovery|L(theta) proportional to p_post(theta)/pi_orig(theta) only within supported parameterization|GWTC-1 posterior archive priors and waveform family
Population outlier gravity test|p(d_i given d_-i,common action) with selection conditioning|GWTC-1 leave-one-event predictive likelihood
Mass-redshift degeneracy under modified expansion|M_source=M_det/(1+z_candidate(dL)); jointly update event population|GWTC-1 mass-distance samples and candidate H(z)
Residual stacking without phase alignment bias|sum_i w_i R_i with source-frame resampling and covariance preserved|GWTC-1 waveform residual products if obtained
Common dispersion coefficient catalog fit|DeltaPsi_i=A I(z_i)f^(alpha-1); one A shared across events|GWTC-1 event phase/distance likelihoods
Polarization catalog accumulation|L_pol=product independent-event L_i with shared calibration hyperparameters|GWTC-1 detector-network geometries
Energy-budget catalog consistency|E_rad,i=M_initial,i c²-M_final,i c² from candidate dynamics versus strain flux|GWTC-1 inspiral/remnant estimates rederived for candidate
Duty-cycle exposure correction|VT=int dt dz dtheta p_det(t,z,theta) dV/dz p(theta)/(1+z)|GWTC-1 observing intervals and instrument duty cycles
New-event-only validation set|fit common action on pre-catalog detections, predict four newly reported events|GWTC-1 newly reported subset with no training leakage
Catalog-to-stochastic consistency|Omega_GW from inferred source rate and candidate emitted spectrum; predict O2 search observable|GWTC-1 population likelihood; 2019 stochastic source reserved as independent output
''')
add(2018,9,r'''
HSC pseudo-Cl mixing|C_tilde_l=sum_lprime M_llprime C_lprime+N_l; derive spin-two mask response|HSC first-year shear power spectra
Four-bin lensing geometry|C_l^ij=int W_i W_j P_Weyl/chi² dchi; retain deep-source kernel tails|HSC tomographic source distributions
HSC E-B leakage correction|[E_tilde,B_tilde]=M_spin[E,B]; quantify finite-field leakage|HSC disconnected field masks
Deep-field photometric-redshift transfer|n_wide(z)=sum_cells p(z given cell)w_wide(cell); propagate limited calibration-field variance|HSC source redshift calibration inputs
Shape-selection response|R_total=R_shape+R_selection; derive weighted shear estimator|HSC magnitude/photo-z cuts and shape responses
Multipole-scale nonlinear cut|k=(l+1/2)/chi; calculate redshift-dependent nonlinear support for each retained l bin|HSC measured multipole range
HSC disconnected-patch covariance|Cov_total=sum_patch Cov_patch+cross_patch long-mode terms|HSC field windows and shear spectra
Source blending covariance|e_obs=(F1 e1+F2 e2)/(F1+F2) diagnostic; derive lensing response with redshift blend|HSC deblending flags and image-simulation dependency
PSF residual leakage spectrum|C_obs=C_true+alpha² C_PSF+2alpha C_gamma,PSF|HSC PSF ellipticity diagnostics
Intrinsic-alignment luminosity weighting|A_IA(z,L) folded through selected source distribution; compare to constant-amplitude approximation|HSC source luminosities and tomographic shear
HSC-DES calibration cross-check|Delta C after matching n(z) and windows; use independent shape systems with shared cosmic variance|HSC first year and DES Y1 overlap
Alternative S8 exponent audit|S8_alpha=sigma8(Omega_m/0.3)^alpha; derive likelihood principal direction rather than equate different alpha|HSC published alpha choices and joint parameter surface
Baryon removal versus gravitational clearing|Delta C_l from delta rho_b compared with candidate carrier-gate response at fixed lensing potential map|HSC small-scale shear and independent gas dependency
Shear covariance cosmology transport|C_Gaussian proportional to (C_l+N_l)^2; include non-Gaussian candidate trispectrum|HSC covariance model and mocks
Mock realism transfer test|Delta C_model from changing only survey geometry versus candidate density dynamics|HSC realistic mock-shear validation description
Ellipticity weight bias|gamma_hat=sum w e/sum wR; derive correlation terms when w depends on shear|HSC source weights and response matrices
Tomographic auto-cross redundancy|PSD condition det C_l>=0 after noise subtraction; identify inconsistent bin combinations|HSC auto/cross bandpowers
Angular resolution filter degeneracy|T_obs(l)=T_PSF(l)T_gravity(l); distinguish image transfer from heat filtering|HSC instrument calibration and candidate xi
High-z source-tail gravity leverage|delta C_l/dn(z_tail) versus delta C_l/dSigma(k,z)|HSC source selection reaching high redshift
Lensing-only preferred-time constraints|derive metric geodesic observable from foliation-dependent potentials; no automatic tensor causality inference|HSC shear map and criterion-B action
HSC foreground-lens source overlap|GI kernel support assessed from measured n_i(z); derive scale-dependent IA leakage|HSC adjacent tomography bins
Noise-subtraction uncertainty|C_hat=C_raw-N_hat; covariance includes uncertainty and correlation of N_hat|HSC shape-noise estimator and source catalog
HSC canonical-alternative shape residual|Delta C_l predicted with fixed different vacuum normalizations and common nuisance priors|HSC full bandpower likelihood
Field-by-field gravity-score stability|theta_-patch predictive residual with patch calibration hyperparameters|HSC six-field data if released
First-year information beyond DES|I_HSC_given_DES with common-sky covariance and distinct source-depth kernels|HSC first-year report and DES Y1 source inventory
''')
add(2018,10,r'''
Redshift-weighted distance basis|chi(z)/chi_fid(z)=alpha0[1+alpha1 x+(alpha2/2)x²] with x defined by report|DR14 weighted anisotropic BAO coefficients
Radial-transverse geometry split|alpha_perp=(D_M/r_d)/(D_M/r_d)_fid; alpha_parallel=(H r_d)_fid/(H r_d)|DR14 weighted anisotropic correlations
Distance derivative H consistency|H(z)=c/[dchi/dz] for flat radial comoving distance; propagate coefficient covariance|DR14 distance-polynomial estimates
Correlated endpoint distances|C_y=J C_alpha J^T for y=(D_M1,H1,D_M2,H2)|DR14 reported endpoint covariance, extraction required
Optimal weight candidate mismatch|w_a(z) proportional to C^-1 partial xi/partial alpha_a; recompute under candidate response|DR14 redshift-weighting scheme
Quadratic basis truncation|R3(z)=chi_true-chi_quadratic; bound induced BAO endpoint bias|DR14 broad quasar redshift range
Alcock-Paczynski ruler cancellation|F_AP=D_M H/c; propagate correlated distance and expansion measurements|DR14 anisotropic BAO constraints
Weighted effective-redshift ambiguity|z_eff,a=int z w_a pair_density/int w_a pair_density; signed weights require careful interpretation|DR14 different redshift weights
Weighted covariance cross terms|Cov(xi_w1,xi_w2) from same pairs with weights w1w2|DR14 weighted pair catalogs/mocks
Configuration anisotropy multipoles|xi_l(s)=(2l+1)int dmu xi(s,mu)P_l(mu)/2|DR14 anisotropic correlation estimates
Quasar redshift systematics radial mode|sigma_r=c sigma_z/H; derive damping impact on alpha_parallel versus alpha_perp|DR14 redshift-error distribution
Growth nuisance versus radial dilation|partial xi/partial f sigma8 versus partial xi/partial alpha_parallel|DR14 RSD-containing anisotropic templates
Lightcone evolution correction|xi(z1,z2) differs from equal-time xi(z_mean); derive leading Delta z² term|DR14 wide redshift-weighted sample
Fiducial cosmology reparameterization|transform polynomial coefficients between fiducials and verify observable invariance|DR14 published fiducial-distance convention
Ruler length versus evolving gravity|r_d fixed by early evolution, while D_M,H by late evolution; derive shared-action relation|DR14 multiple-redshift ruler ratios
Curvature from distance derivatives|[H D_Mprime/c]²=1-K D_M²; assess identifiable curvature mode|DR14 correlated transverse/radial constraints
Acceleration-scale redshift test|a0(z) tied to rho_DE(z) only if declared; propagate into candidate H(z) and clustering|DR14 weighted redshift leverage
Weighted broadband nuisance basis|B(s,z)=sum_ab b_ab s^a x(z)^b; find acoustic mode left after projection|DR14 weighted correlation functions
Mock-based weight improvement audit|compare Var(alpha) with/without weights at fixed realization, not independent ensembles|DR14 actual-data and mock-weighting outputs
Endpoint extrapolation boundary|evaluate polynomial uncertainty near sample edges using coefficient covariance and remainder|DR14 reported distances toward redshift endpoints
2017 monopole conditional increment|L(anisotropic weights given old monopole) using joint same-quasar covariance|DR14 2017 isotropic and 2018 weighted reports
Redshift-bin compression entropy|I_full-I_coeff from nonlinear candidate likelihood; quantify loss beyond local Fisher approximation|DR14 weighted coefficient likelihood
Angular completeness evolution|W(n,z) couples redshift weights to angular systematics; derive spurious anisotropy|DR14 completeness maps and quasar weights
Null radial-transverse consistency|fit common candidate H then predict D_M integral; compare measured perpendicular mode|DR14 both anisotropic acoustic directions
Anisotropic BAO common-action region|intersect allowed alpha0,alpha1,alpha2 surface with derived expanding background and two fixed a0 footings|DR14 weighted measurements and candidate FLRW solution
''')
add(2019,1,r'''
Keck redshift temporal-shape residual|Delta z(t)=z_obs-z_candidate from exact emitter-observer frequency ratio|S0-2 2018 March–September radial velocities plus historical orbit
Independent-telescope redshift replication|Delta Upsilon=Upsilon_Keck-Upsilon_GRAVITY with common orbit/environment nuisance|Keck report and 2018 GRAVITY redshift measurement
Three-pericentre-event leverage|F_ab=sum_eventblocks J_a^T C^-1 J_b; quantify phase-specific redshift information|S0-2 pericentre observing blocks described in report
Keck instrument zero-point transport|v_obs=v_model+Z_OSIRIS+Z_NIRSPEC with instrument-specific drift if supported|S0-2 spectrograph identities and radial-velocity calibration
Historical orbit conditioning|p(d_2018 given d_1995:2017,theta) integrates common astrometric-frame parameters|S0-2 new velocities and historic baseline
Astrometric confusion bias|theta_centroid=(F_star theta_star+F_blend theta_blend)/(F_star+F_blend)|S0-2 imaging and confusion flags
Redshift parameter versus metric perturbation|delta Upsilon(t)=delta z_metric(t)/z_rel,GR(t); constancy must be tested|S0-2 measured relativistic-redshift time template
Relativistic versus Newtonian likelihood|Delta logL after all orbital parameters refit; calibrate composite Newtonian null|S0-2 reported comparison and raw astrometry/velocities
S0-2 reference-frame correlated errors|C_theta,ij=C_stat,ij+A_i Cov(frame)A_j^T|S0-2 historical astrometric transformations
Romer delay and redshift covariance|z(t_emit(t_obs)) with dt_emit/dt_obs=1/(1+v_parallel/c+... )|S0-2 rapid line-of-sight motion around pericentre
Spectral-line atmospheric shift|z_line=z_geodesic+z_atmosphere(T,logg,rotation); compare lines separately|S0-2 spectra and atmosphere calibration dependency
Extended-mass precession-redshift coupling|delta omega and delta z from the same deltaPhi_ext(r), jointly marginalized|S0-2 full orbit and central stellar-density constraints
Source distance versus black-hole mass|derive joint angular/radial likelihood ridge M proportional to R0^p with fitted p|S0-2 astrometry and spectroscopy covariance
Pericentre epoch uncertainty response|partial z/partial t_p=-dot z plus orbital parameter cross terms|S0-2 timing and velocity sampling
Photon bending astrometric correction|delta theta from integral grad_perp(Phi+Psi)dl/c² along S0-2 rays|S0-2 closest projected approach and imaging uncertainty
Finite light-source size correction|z_observed=int I_surface z_surface dA/int I_surface dA|S0-2 angularly unresolved spectra and stellar radius prior
Acceleration-law outer-orbit leverage|K(t,r)=delta theta(t)/delta g(r); locate sensitivity beyond pericentre|S0-2 1995–2017 astrometry
Preferred-frame redshift anisotropy|delta z=Q_ij v_i u_pref,j/c² from allowed action terms; derive coefficient|S0-2 orbit orientation and actual observation epochs
No-slip measurement sufficiency|rank J(Phi,Psi) from redshift and deflection before asserting Phi=Psi|S0-2 joint astrometric/spectroscopic signal
Posterior-chain reanalysis gate|reuse chains only if candidate residual is evaluable at original latent orbit parameters with original prior known|S0-2 author-linked posterior chains, payload uninspected
Telescope-sharing sky-frame covariance|Cov(Keck,VLT) includes common reference-source motions but independent detector noise|S0-2 cross-telescope astrometric standards
Barycentric correction implementation audit|z_BCRS from observer four-velocity; compare additive and multiplicative convention residuals|S0-2 observation timestamps/site ephemeris
High-y vacuum correction ceiling|bound integral deltaPhi_MONO(r(t))/c² under fixed a0 and xi domain|S0-2 orbit support and both acceleration normalizations
Out-of-fit 2018 epoch prediction|train on pre-pericentre epochs, predict post-pericentre velocities with full conditional covariance|S0-2 March–September time series
Pericentre-to-PPN bridge|derive Upsilon in terms of candidate PPN coefficients and stellar dynamical parameters, not Upsilon=gamma by assertion|S0-2 measured redshift parameter and common-action PPN expansion
''')
add(2019,2,r'''
Time-delay Fermat observation map|Delta t_ij=(D_DeltaT/c)Delta phi_ij only after deriving photon arrival functional|H0LiCOW six-lens delays and image constraints
Metric slip in strong-lens potential|psi(theta)=(D_ls/(D_l D_s c²))int(Phi+Psi)dl with normalization derived|H0LiCOW lens images and stellar kinematics
Mass-sheet distance ambiguity|kappa_lambda=lambda kappa+1-lambda; Delta phi_lambda=lambda Delta phi|H0LiCOW imaging and time-delay data
External convergence transport|D_DeltaT,true=D_DeltaT,model/(1-kappa_ext) under stated convention|H0LiCOW line-of-sight environmental likelihoods
Stellar anisotropy breaking mass sheet|sigma_ap²=int aperture projected Jeans solution; retain beta(r) family|H0LiCOW lens-galaxy velocity dispersions
Finite aperture seeing correction|sigma_obs²=int PSF*I sigma_los²/int PSF*I over slit|H0LiCOW spectroscopic apertures and imaging PSFs
Microlensing delay nuisance|Delta t_obs=Delta t_macro+Delta t_micro(band,epoch)|H0LiCOW multiseason quasar light curves
Source-position transformation boundary|beta -> f(beta) can preserve images while changing delays; characterize physically admissible candidate maps|H0LiCOW extended arcs and measured delays
Six-lens conditional consistency|p(d_i given d_-i,common H0,action) with lens-specific astrophysical nuisance|H0LiCOW joint six-lens report
Angular distance versus time-delay distance|D_DeltaT=(1+z_l)D_l D_s/D_ls; derive independent D_l from dynamics only if metric map known|H0LiCOW redshifts,delays,kinematics
Cosmology-dependent kinematic inference|R=D_l theta changes baryon density and velocity model when H0 varies|H0LiCOW lens light and dispersion data
Baryon-only filtered lens solve|solve finite 3D baryon source with S and derive both potentials before ray tracing|H0LiCOW lens light and stellar mass-to-light inputs
Line-of-sight multi-plane coupling|beta=theta-sum_a D_as/D_s alpha_a(theta_a); derive cross-plane Jacobian|H0LiCOW environment galaxies and lens geometry
Lens light mass-to-light gradients|Upsilon(r)=Upsilon0 exp[q log(r/r0)]; project effect on delays and dispersion|H0LiCOW multiband stellar light profiles
Dark-halo surrogate portability|replace GR mass-profile posterior with raw image/kinematic likelihood when candidate source relation changes|H0LiCOW model-dependent mass-profile chains
Delay covariance from common curves|Cov(Delta t_ij,Delta t_ik) retains shared image light curve and variability model|H0LiCOW delay-estimation products
Blind-analysis prior sensitivity|Delta H0 under prior families on mass-sheet/anisotropy directions at fixed blinded data|H0LiCOW blind inference settings and posterior likelihood
Curvature distance-ratio degeneracy|D_ls=S_K(chi_s-chi_l); compute H0-K covariance across lens redshifts|H0LiCOW diverse lens-source redshifts
Vacuum acceleration common-scale matching|rho_L=4a0²/(G_N c²) enters background while local lens response uses same action|H0LiCOW time-delay distances and fixed a0 footings
Lens population selection correction|p(lens_params given selected) proportional to lensing_crosssection times parent distribution|H0LiCOW monitored-lens selection and modeling priors
Quasar variability nonstationarity|L_curves with epoch-dependent covariance; quantify time-delay shifts from stationary approximation|H0LiCOW long-term image light curves
Time-delay versus supernova anchor bridge|H0 cancels in relative SN distances but is supplied by lens likelihood; share cosmology only once|H0LiCOW plus Pantheon matched supernova IDs
GR-independent distance compression audit|D_DeltaT posterior sufficient only if candidate imaging/dynamics map is unchanged|H0LiCOW distance posterior versus underlying likelihood
Stellar dynamics-light bending G ratio|G_dyn from velocities and G_lens from images; derive measured ratio with mass-profile covariance|H0LiCOW lens spectroscopy and arcs
Common-action six-lens admissibility|intersection_i B_i(action,Upsilon_i,beta_i) with one global kernel and coupling cell|H0LiCOW six-lens observations without per-lens gravity retuning
''')
add(2019,3,r'''
LMC Cepheid period-luminosity calibration|m_H,W=mu_LMC+M_H+b(log P-1)+Z metallicity|SH0ES new LMC HST Cepheid photometry
Same-camera zero-point cancellation|Delta m=m_Cepheid,host-m_Cepheid,LMC; derive surviving count-rate calibration terms|SH0ES WFC3 matched-system observations
Count-rate nonlinearity transfer|m_corr=m_obs+q log(count_rate/count_ref); propagate q across ladder dynamic range|SH0ES stated WFC3 linearity calibration dependency
LMC geometry thickness correction|mu_i=mu_center+5log10(D_i/D_center); model inclined disc positions|LMC Cepheid sky positions and geometric-distance anchor
Eclipsing-binary anchor covariance|Cov(mu_LMC,M_Cepheid) propagated from independent geometric distance, not duplicated as prior and data|SH0ES LMC calibration plus separately verified binary-distance source
Cepheid period-break leverage|M(P)=M0+b1 logP+b2 max(0,logP-logPbreak)|SH0ES long-period LMC and host Cepheids
Metallicity-ladder degeneracy|partial H0/partial Z_coeff via weighted host-LMC metallicity difference|SH0ES Cepheid metallicities and host calibration
Reddening Wesenheit coefficient|W=H-R(V-I); derive residual dust sensitivity under different extinction laws|SH0ES multiband Cepheid photometry
Crowding bias transfer|Delta m_crowd from artificial-star recovery conditioned on host surface brightness|SH0ES LMC versus supernova-host imaging environments
Parallax-anchor zero-point coupling|varpi_obs=varpi_model+zeta; derive covariance with Cepheid absolute magnitude|SH0ES Milky Way anchor subset
Maser-anchor gravity interpretation|D_maser inferred from angular rotation and acceleration; rederive if central force law changes|SH0ES NGC4258 anchor dependency, raw data authentication required
Three-anchor conditional consistency|p(anchor_i given other two,common Cepheid relation) with shared calibration covariance|SH0ES LMC/MW/maser ladder components
Supernova calibration Jacobian|H0 proportional to 10^[(M_B+5a_B+25)/5]; propagate correlated M_B,a_B|SH0ES calibrated supernova magnitude and Hubble-flow intercept
Cepheid selection truncation|L_PLM conditional on detection and period-quality cuts; derive normalization|SH0ES Cepheid magnitude/period selection
Intrinsic period-luminosity scatter hierarchy|M_i=M_relation+epsilon_i with host-correlated component|SH0ES individual Cepheid residuals
Cepheid gravitational coupling response|P proportional to (G_star rho_mean)^-1/2 only as limiting pulsation scaling; derive luminosity change jointly|SH0ES measured periods and stellar-structure dependency
Environmental coupling ladder bias|Delta M_env=F(g_host,a0,stellar parameters) derived from same action, not a free host correction|SH0ES Cepheids across different host environments
LMC depth versus color covariance|Cov(delta mu_depth,color) can bias Wesenheit slope; fit spatial-color relation|SH0ES LMC spatial photometry
HST scanning/pointing photometry audit|flux ratio invariance after mode-specific aperture and detector corrections|SH0ES new observing strategy metadata
Anchor improvement information increment|I_new=LMC_new calibration information conditional on earlier ladder samples|SH0ES 2019 updates and overlapping earlier Cepheids
Hubble-flow peculiar-velocity floor|Cov(a_B) includes correlated low-z velocities; derive effect on H0|SH0ES calibrated Hubble-flow supernovae
Host population mismatch|M_Cepheid(P,Z,age) distribution differs by selected host; integrate latent age before transport|SH0ES LMC versus host Cepheid populations
Posterior tension theory dependence|compare p(H0 given ladder,candidate) to p(H0 given CMB,candidate), not fixed GR posterior overlap|SH0ES ladder and Planck spectral inference dependency
Vacuum-scale H0 consistency surface|derive H0(rho_L,G_cosmo,other densities) with rho_L fixed separately by each a0 footing|SH0ES expansion-rate likelihood and candidate FLRW branch
Ladder-to-standard-siren independent bridge|predict siren distance-redshift relation from calibrated ladder cell; account for shared peculiar-velocity field|SH0ES H0 result and authenticated GW170817 distance data
''')
add(2019,4,r'''
Forest transmitted-flux observation map|F=exp(-tau); tau=int n_HI sigma_alpha dl with velocity and thermal convolution|DR14 Ly-alpha spectra and continuum estimates
Ly-beta-region incremental forest information|L(alpha-region,beta-region) with same quasar continuum covariance|DR14 new Ly-alpha absorption measured in Ly-beta wavelength region
Forest anisotropic BAO dilation|xi_F(r_parallel,r_perp) -> xi_F(alpha_parallel r_parallel,alpha_perp r_perp)|DR14 absorption correlation bins
Continuum-fitting distortion matrix|xi_meas=D xi_true; derive D from per-quasar continuum projection|DR14 continuum procedure and spectral sampling
Metal-line contamination displacement|r_parallel,metal from mistaken transition wavelength ratio; derive correlated templates|DR14 wavelength-resolved forest correlations
Damped-absorber masking response|W_DLA affects both pair counts and large-scale forest bias|DR14 absorber masks and flux correlation data
Thermal broadening versus gravity|P_F multiplied by exp(-k_parallel² b_T²) while candidate growth changes full k,mu dependence|DR14 anisotropic flux correlations
Peculiar-velocity gradient mapping|s_parallel=r_parallel+v_parallel/(aH); derive flux Jacobian|DR14 redshift-space forest signal
UV-background fluctuation bias|delta_F=b_delta delta+b_eta eta+b_Gamma deltaGamma|DR14 broadband forest correlations and ionizing-background priors
Forest BAO phase robustness|smooth transfer b_F(k,mu) can bias peak position; quantify projection onto dilation score|DR14 acoustic peak and broadband alternatives
Lyman-alpha auto-cross overlap covariance|Cov(xi_FF,xi_QF) includes common spectra/quasars; joint result not independent product|DR14 autocorrelation report and companion cross-correlation dependency
Radial transverse ratio test|F_AP=D_M/D_H; retain full D_H-D_M covariance|DR14 reported BAO distance pair
Ruler calibration without Planck prior|infer D_H/r_d,D_M/r_d; treat r_d as candidate-derived or nuisance explicitly|DR14 high-redshift acoustic measurement
High-redshift vacuum leverage|partial(D_H/r_d)/partial rho_L under candidate FLRW rather than assumed LCDM|DR14 high-z distance likelihood
Baryon-only growth forest test|derive P_delta and velocity divergence from candidate baryon/carrier equations|DR14 flux broadband information and hydrodynamic calibration requirement
Acceleration-trigger clearing flux budget|Delta mean F=int p(g)Delta F(g,gate)dg; compare occupied versus cleared absorber fraction|DR14 transmitted-flux statistics plus independently sourced gas model
Pressure-smoothing filter degeneracy|T_F(k)=T_pressure(k)T_gravity(k,xi); seek anisotropic separation using thermal term|DR14 radial/transverse correlation shape
Quasar redshift error cross-contamination|quasar continuum rest-frame errors shift absorption mapping coherently along spectrum|DR14 quasar-redshift estimates and continuum fits
Sky-subtraction correlated pixels|C_flux,ij includes same observed-wavelength residual; propagate to radial correlation|DR14 spectroscopic calibration and masks
Spectral resolution transfer|F_obs=LSF*F_true; derive power suppression and variable-resolution covariance|DR14 line-spread function by exposure
Forest effective-redshift weighting|z_eff(r)=sum_pairs w_pair z_pair/sum_pairs w_pair; quantify scale dependence|DR14 absorption-pair weights
Broadband-model model selection|marginalize acoustic scale over physically motivated and polynomial broadband spaces|DR14 report's two broadband treatments
Mock-covariance candidate dependence|Cov_xi requires candidate flux trispectrum, not only rescaled GR two-point power|DR14 covariance products and simulation assumptions
Forest-to-quasar distinct-tracer bridge|joint gravity response to flux and quasar density with shared initial modes and sample covariance|DR14 forest and earlier quasar clustering reports
High-z distance-to-local-a0 closure|derive map rho_L -> H(z) and rho_L -> a0 without equating G_cosmo and G_N|DR14 measured ruler ratios and fixed framework normalizations
''')
add(2019,5,r'''
IPTA combined arrival-time likelihood|r_joint=[r_EPTA,r_NANO,r_PPTA]; C includes same-epoch shared pulse and clock terms|IPTA DR2 timing data and overlap metadata
Duplicate observation provenance|construct unique TOA keys by telescope,epoch,backend,frequency before merging|IPTA constituent regional timing archives
Backend jump identifiability|r=M theta+sum_backend J_b offset_b+n; remove one gauge offset|IPTA DR2 backend timing conventions
Combined clock standard transport|TOA_TT=TOA_site+clock_chain; propagate correlated time-standard uncertainty|IPTA DR2 observatory clock metadata
Regional ephemeris harmonization|r_new=r_old-n dot(delta r_SSB)/c with timing refit|IPTA constituent solar-system ephemerides
Cross-observatory profile calibration|delta TOA from polarization calibration mismatch; fit backend frequency response|IPTA pulse-profile and calibration dependencies
Long-baseline spin-red-noise separation|timing fit removes polynomial subspace; compute remaining low-frequency transfer|IPTA expanded observation spans
Binary-pulsar parameter covariance|fit Keplerian and relativistic timing terms with common noise, not stitched point estimates|IPTA timing ephemerides
Astrometric parallax timing signature|Delta_pi proportional to r_Earth² perpendicular/(2c d); derive annual geometry|IPTA pulsar timing parallaxes
Proper-motion timing residual|Delta_mu=-r_Earth dot(mu Delta t)/c|IPTA sky positions and proper-motion timing terms
Shklovskii period correction|dot P_shk=P mu² d/c; propagate correlated distance/proper-motion uncertainty|IPTA pulsar periods and astrometry
Galactic acceleration timing map|dot P_obs/P=dot P_intr/P+(a_p-a_obs)dot n/c+mu²d/c|IPTA timing periods and distance uncertainties
Wide-binary orbital-period gravity response|dot P_b residual after kinematic corrections constrains energy loss and local force jointly|IPTA binary timing systems with suitable measurements
DM event versus achromatic process|r_DM proportional to nu^-2; compare localized event kernels with red stochastic basis|IPTA multi-frequency residuals
Solar elongation noise weighting|S_TOA depends on angular distance from Sun; derive seasonally varying covariance|IPTA observation epochs and radio frequencies
Cross-array noise hyperparameter transfer|hierarchical EFAC/EQUAD/ECORR model per backend with shared pulsar process|IPTA DR2 noise characterization
Sky-coverage quadrupole conditioning|singular spectrum of pulsar-pair tensor correlation design versus dipole/monopole|IPTA DR2 sky distribution
Earth-pulsar term frequency resolution|Delta f=1/T and phase uncertainty 2pi f delta L/c; derive resolvable coherence|IPTA distances and spans
Single-source continuous-wave search map|r_a(t)=F_a^A integral[h_A(Earth)-h_A(pulsar)]dt|IPTA residuals; proposed search distinct from release claim
Memory-burst timing ramp|r_a(t)=F_a Delta h (t-t0)H(t-t0) after timing projection|IPTA released cadence and residual sensitivity
Nonstationary common-process diagnostic|C_ab(t,tprime)=Gamma_ab A(t)A(tprime)K(t-tprime)|IPTA combined long-baseline residuals
NANOGrav overlap exclusion|IPTA likelihood conditional on reused NANO data; do not multiply by 11-year likelihood|IPTA DR2 and NANOGrav source-observation matches
Region-held-out tensor prediction|fit common process to two regional arrays, predict third with shared pulsars conditioned|IPTA regional provenance labels
Radio-frequency propagation gravity split|separate plasma dispersive delay from candidate tensor/light metric propagation|IPTA multi-band TOAs and single-metric action
IPTA release-to-action constraint map|derive timing observation functional for pinned action; report identifiable coefficient subspace|IPTA DR2 measured timing products without treating noise ephemerides as theory-free
''')
add(2019,6,r'''
Energy-phase photon-count likelihood|N_Ephi~Poisson[int R(E,Etrue)F_Etrue(phi)dEtrue+B_Ephi]|NICER J0030 phase-energy counts and response matrix
Surface-to-observer ray map|I_nu/nu³ invariant along metric null geodesic; integrate spot visibility and bending|NICER pulse waveform and candidate exterior metric
Compactness versus light-bending degeneracy|u=G_metric M/(R c²); derive waveform derivatives with respect to M,R,G_metric|NICER phase-resolved spectrum
Gravitational redshift surface transfer|1+z_s=[-g_tt(R)]^-1/2 for static emitter, then include rotation|NICER spectral-temperature and pulse-shape information
Hotspot geometry identifiability|rank partial N_Ephi/partial(spot_latitude,area,temperature,compactness)|NICER inferred emitting-spot configurations
Three-spot versus alternative topology|compare posterior predictive counts with equal background/calibration treatment across spot maps|NICER best-fit emission pattern and independent-analysis dependency
Rotational Doppler asymmetry|D=[gamma(1-beta dot n)]^-1; F_nu scales D³ with spectral argument shifted|NICER spin frequency and asymmetric pulse waveform
Oblate stellar surface correction|R(theta)=R_eq[1-e_shape cos²theta+...]; derive photon normal and area changes|NICER rotating-star geometry and candidate stellar solution
Frame-dragging ray contribution|g_tphi enters k_mu u^mu and null deflection; bound effect at observed spin|NICER pulse timing and candidate angular momentum
Atmosphere beaming response|I_E(mu_em;T,g_s) folded through ray map; compare beaming uncertainty to gravity score|NICER hydrogen-atmosphere model dependency
Background spectral degeneracy|N_source(E,phi)+B(E); use off-pulse and independent background information coherently|NICER background count estimates
Instrument effective-area covariance|A_eff(E)=A_ref(E)[1+sum q_a e_a(E)]; profile calibration modes|NICER response calibration products
Interstellar absorption transport|F_obs(E)=exp[-N_H sigma(E)]F_surface(E); separate N_H-temperature-redshift ridge|NICER soft X-ray spectrum
Distance flux-area degeneracy|F proportional to A_spot/d²; characterize whether radius information survives free spot area|NICER flux and external parallax dependency
Phase alignment timing systematics|N(E,phi+delta phi(E)); bound energy-dependent clock or folding offsets|NICER event arrival times and spin ephemeris
Pulse harmonic compactness score|a_n(E)=int F_E(phi)e^-inphi dphi; identify harmonics least degenerate with spot area|NICER energy-dependent harmonic content
GR posterior mass-radius portability|p_GR(M,R) cannot be reused if bending/redshift map changes; define raw-count refit requirement|NICER published mass-radius contours and inference assumptions
Candidate hydrostatic stellar equation|derive dP/dr and dm/dr from action with G_N,G_E distinct; match to exterior|NICER allowed waveform region plus explicit EOS dependency
EOS-gravity joint identifiability|rank partial waveform/partial(EOS coefficients,gravity coefficients) with fixed ordinary matter content|NICER J0030 count likelihood
Surface gravity atmosphere consistency|g_s from same metric as bending; feed it into atmosphere spectrum rather than independent GR value|NICER atmosphere tables and stellar metric
Heat-filter finite-star matching|S depends on spatial metric and boundary; vary it before solving stellar equilibrium|NICER compact-star size constraints and candidate xi
Positive-pressure stellar sequence|dM/dcentral_density turning points only conditional stability diagnostic; derive radial-mode operator|NICER mass-radius admissible region and candidate matter action
Independent spot-model conditional replication|compare Miller/Riley waveform predictions using same photons; never multiply their posteriors|NICER J0030 primary report and companion analysis to authenticate
Canonical-alternative strong-field decoupling|estimate derivative of waveform with respect to rho_L for fixed a0 footing, including coupling matching|NICER count precision and two normalization branches
X-ray-to-radio compactness bridge|combine waveform M/R sensitivity with an independent timing mass only for same star and authenticated data|NICER J0030; identify missing independent mass measurement without inventing one
''')
add(2019,7,r'''
J0740 Shapiro delay observation map|Delta_S=-2r log(1-s sin phi) in low-e limit; derive r,s from candidate metric|J0740 orbital-phase-specific timing
Shapiro range coupling ambiguity|r=G_light m_comp/c³; mass is conditional on G_light=G_N|J0740 measured delay range and companion mass inference
Shapiro shape inclination map|s=sin i only for specified geometry and ray law; derive finite-eccentricity correction|J0740 conjunction timing and inclination posterior
Binary mass-function bridge|f=(4pi²/G_orb)(a_p sin i)³/P_b²=m_c³ sin³i/(m_p+m_c)²|J0740 projected semimajor axis and orbital period
Orthometric delay harmonics|h3=r varsigma³; varsigma=s/(1+sqrt(1-s²)); transform prior Jacobian|J0740 Shapiro likelihood parameterization
Targeted-conjunction information gain|F_new-F_old from actual phase sampling, retaining shared timing-noise covariance|J0740 new Green Bank orbital-phase observations
Near-conjunction plasma mimic|Delta t_plasma proportional to DM(phi)/nu²; compare to achromatic logarithmic delay|J0740 multi-frequency conjunction TOAs
Companion quadrupole time delay|deltaDelta_Q proportional to integral Q_ij n_i n_j/r³ dl; derive from metric|J0740 companion geometry and timing residuals
Mass posterior asymmetric tails|compute highest-density and profile-likelihood regions without Gaussianizing m_p|J0740 reported asymmetric mass posterior
Companion mass prior effect|p(m_p given d)=int L(r,s,f)pi(m_c,cos i)dm_c di with exact Jacobian|J0740 mass/inclination prior definitions
Eccentricity-Shapiro covariance|Delta_R,e basis overlaps delay harmonics; compute nuisance-orthogonal Shapiro score|J0740 low-eccentricity orbital timing
Astrometric annual orbital parallax|delta x(t) from changing line of sight; compare with Shapiro inclination information|J0740 timing astrometry and orbital projection
Kinematic orbital-period derivative|dot P_b,obs=dot P_b,int+P_b(a_los/c+mu²d/c)|J0740 measured or bounded period derivative, data status to verify
Strong-body sensitivity mass interpretation|m_inertial,m_grav,m_metric from varied stellar action; determine which enters timing mass|J0740 timing mass likelihood and candidate stellar model
White-dwarf radius occultation control|geometric impact parameter b=a cos i versus R_comp; check delay-only model domain|J0740 orbital inclination and companion-radius dependency
Retarded companion position correction|Phi evaluated along moving source light path; derive O(v_comp/c) correction|J0740 orbital-phase timing precision
Two-potential Shapiro integral|Delta_S=-(1/c³)int(Phi+Psi)dl; compare with dynamical Phi from mass function|J0740 delay and orbital dynamics
High-y MONO timing correction|integrate filtered companion potential along pulses; keep source and observer boundary terms|J0740 conjunction ray geometry and fixed a0 values
Timing jitter epoch correlation|C_jitter block-correlates simultaneous frequency channels; propagate to range r|J0740 targeted high-cadence observations
Template evolution frequency bias|delta TOA(E_radio) from profile mismatch; infer residual chromatic structure|J0740 pulse-shape calibration data
Solar-system ephemeris mass covariance|annual/broadband timing terms covary with position and binary mass; refit jointly|J0740 NANOGrav baseline and ephemeris choice
Maximum-mass EOS implication boundary|M_max(EOS,action)>=M_J0740 only after posterior mass is rederived in same action|J0740 timing likelihood and declared ordinary-matter EOS
NANOGrav catalog reuse accounting|condition on J0740 TOAs rather than multiply mass posterior by parent timing likelihood|J0740 12.5-year subset and later PTA catalog overlap
Massive-star branch stability|derive radial-mode omega0² for stellar configurations in J0740 allowed timing region|J0740 mass constraint and candidate equilibrium sequence
Shapiro-to-NICER cross-object EOS bridge|one EOS and gravity cell predicts both J0740 timing mass and J0030 waveform, with independent-star likelihoods|J0740 and NICER J0030 primary measurements
''')
add(2019,8,r'''
DF4 diffuse-light-conditioned cluster likelihood|L_DF4=L_diffuse(v_sys) product_i N(v_i given v_sys,sigma_los²(R_i)+epsilon_i²), with common wavelength-calibration covariance retained|DF4 measured cluster radial velocities and diffuse-light systemic velocity
Diffuse-light versus tracer systemic test|Delta v=v_diffuse-v_clusters with shared wavelength-calibration covariance|DF4 integrated-light and cluster spectra
Seven-tracer dispersion coverage|simulate actual heteroscedastic small-sample likelihood; calibrate interval coverage at sigma near zero|DF4 tracer geometry and uncertainties
DF4 host-field prediction from DF2|p(sigma4 given host,DF2 photometry) derived before fitting DF4 velocities|DF4 and DF2 shared NGC1052 group environment
Shared-distance covariance of two dwarfs|Cov(M2,M4) from D_group² luminosity scaling while radii scale as D_group|DF4/DF2 distance likelihoods
Differential external-field test|Delta sigma²=sigma4²-sigma2² predicted by distinct baryon profiles at common host field|DF4 and DF2 measured sizes and luminosities
Tidal stripping versus equilibrium|I_double_dot=2(2K+W+surface terms); derive minimum disequilibrium needed for observed dispersion|DF4 structural and velocity measurements
Tidal-tail projection contamination|v_los=v_bound+v_stream(s); test spatial velocity gradient with membership mixture|DF4 sky tracer positions and diffuse morphology
Galaxy-light mass deprojection|rho_star(r) from Abel inversion of I(R), with finite outer light uncertainty|DF4 imaging profile and mass-to-light prior
Cluster selection luminosity bias|p(tracer given selected) depends on luminosity,radius and velocity-quality cuts|DF4 luminous-cluster spectroscopy selection
Galaxy-host three-dimensional separation|r_host²=R_projected²+Delta D²; propagate into external acceleration distribution|DF4 projected location and uncertain group depth
Host mass-model uncertainty|g_ext from baryonic host filtered field; do not import an unconstrained dark halo|DF4 host photometry/gas measurements requiring authentication
External tidal tensor anisotropy|T_ij=partial_i partial_j Phi_host; project onto dwarf principal axes|DF4 morphology and host direction
Velocity-gradient rotation degeneracy|v_i=v_sys+Omega_proj x_i+noise; distinguish rotation from tidal streaming|DF4 tracer positions and radial velocities
Instrument wavelength-error floor|epsilon_total²=epsilon_stat²+s_cal² with common and independent calibration components|DF4 Keck spectra and calibration metadata
Distance-estimator gravity portability|surface-brightness-fluctuation calibration may depend on stellar populations; state independent distance assumptions|DF4 reported distance and calibration dependency
Pressure-support finite boundary|Jeans solution with P(rt) varied physically; bound effect on aperture dispersion|DF4 observed tracer extent
Heat-filter satellite-host nonadditivity|Phi[rho_host+rho_sat] differs from Phi_host+Phi_sat because nu is nonlinear|DF4 baryon profiles and projected separation
Phantom-density sign local test|rho_ph=div[(nu-1)grad Su]/4pi G_N after S*; compute along DF4 tidal geometry|DF4 spatial profile and candidate MONO source
Common-kernel two-dwarf likelihood|L_DF2,DF4 with shared xi,a0,host and separate stellar nuisance|DF4/DF2 velocities without per-object force corrections
Low-dispersion discovery conditioning|condition on discovery/selection before interpreting frequency of such galaxies|DF4 reported discovery and selection pathway
Diffuse-light dispersion prospective extraction|derive spectral LOSVD likelihood and minimum resolution needed; mark missing dispersion rather than infer from systemic velocity|DF4 diffuse-light spectra, published systemic velocity only authenticated
Globular-cluster orbital survival|integrate candidate orbits plus tidal tensor; require survival over independently inferred stellar age|DF4 cluster radii and stellar-age dependency
Canonical-alternative external-field discrimination|Delta logL with fixed a0 footings and same host posterior|DF4 sparse velocity likelihood
Two-dwarf environmental falsifier|derive joint predictive interval for ratio sigma4/sigma2 resistant to common distance/host normalization|DF4 and DF2 distinct tracer measurements
''')
add(2019,9,r'''
O2 cross-correlation energy map|C_hat(f)=Re[s_H*(f)s_L(f)]/normalization; derive normalization from tensor energy and detector response|LIGO O2 stochastic cross spectrum
Overlap-reduction geometry|gamma_T(f)=normalization int dOmega sum_A F_H^A F_L^A exp(2pi i f n dot Delta x/c)|LIGO baseline and antenna orientations
O1-O2 combined likelihood|L_joint=L_O1 L_O2 with independent strain segments but shared calibration hyperparameters|Published O1+O2 stochastic combination
Power-law integrated bound|Omega(f)=Omega_ref(f/f_ref)^alpha; infer Omega_ref with actual frequency covariance|O2 stochastic spectral upper limits
Flat-spectrum normalization H0 dependence|Omega=rho_GW/rho_crit with rho_crit=3H0²/(8pi G_cosmo); retain G_rad/G_cosmo|O2 reported normalized energy density limit
Magnetic Schumann transfer|C_mag=T_H(f)T_L*(f)M_HL(f); propagate uncertain transfer functions|O2 magnetometer cross spectra and coupling estimates
Noise-notch selection bias|Q(f)=0 in vetoed bins; derive lost signal and correlated-noise response|O2 frequency masks and stochastic filter
Scalar/vector limits as diagnostic controls|gamma_A(f) from alternate antenna patterns; do not introduce extra gravity modes into operative action|O2 reported non-tensor background limits
Tensor dispersion overlap response|gamma_T(f;c_T(f)) changes baseline phase; recompute before applying GR-normalized bound|O2 cross spectrum and pinned tensor dispersion
Calibration-amplitude common scale|C_obs=(1+deltaA_H)(1+deltaA_L)C_true; marginalize multiplicative uncertainty|O2 detector calibration likelihood
Calibration-phase cross-spectrum loss|Re[e^(i Delta phi_cal)C_signal]; quantify quadratic attenuation and imaginary residual|O2 complex cross spectra and phase calibration
Nonstationary segment weighting|Omega_hat=sum_s w_s C_s/sum_s w_s with w_s depending on PSD_s|O2 segment PSD and data-quality selection
Time-slide stochastic null|C_slide from unphysical detector lag tests noise tails while destroying astrophysical coherence|O2 off-source/time-shift cross-correlation products
Stochastic spectral covariance|Cov(C_f,C_fprime) includes window leakage and overlapping segments|O2 window function and segment overlap
Resolved-event subtraction boundary|C_total=C_unresolved+C_resolved; identify whether loud event segments were removed|O2 data-quality masks and GWTC-1 event times
Catalog-predicted compact-binary background|Omega(f)=f/(rho_crit c²)int dz R(z)dE_s/df_s/[(1+z)H(z)]|GWTC-1 rate/posterior and O2 stochastic likelihood
Source population upper-limit interpretation|bound integral R(z)E_s rather than rate alone without fixed mass/spin distribution|O2 compact-binary spectral limit
Broken-power-law background identifiability|Omega=Omega_b(f/f_b)^alpha1 below fb and alpha2 above; compute resolvable combinations|O2 frequency sensitivity support
Anisotropy leakage into isotropic estimator|Omega(n,f)=sum_lm a_lm Y_lm; isotropic estimator response to nonmonopoles|O2 sidereal observing window
Duty-cycle burst foreground|non-Gaussian intermittent source distribution changes estimator variance; derive fourth-moment correction|O2 segment cross-correlation distribution
Tensor kinetic positivity energy conversion|rho_GW proportional to Q_T<dot h²>; a strain upper limit becomes energy bound only for Q_T>0|O2 observed cross spectrum and candidate quadratic action
Vacuum-generated tensor spectrum|derive source stress spectrum from existing action fields; compare predicted Omega to O2 likelihood|O2 bound without adding cosmic strings or particles
Filter-induced high-frequency suppression|T_h(k,xi) from derived tensor equation; distinguish detector band transfer from leaf scalar heat filter|O2 spectral sensitivity and candidate filter variation
O2 correlated-noise uncertainty envelope|sup_Cmag in allowed set Omega_hat(C-Cmag); report partially identified bound|O2 magnetic noise estimate with transfer uncertainty
Stochastic-to-PTA spectral bridge|propagate one candidate source spectrum across nHz–Hz including source evolution and selection|O2 and authenticated NANOGrav 11-year likelihoods, no assumed shared power law
''')
add(2019,10,r'''
Visibility-domain ring observable|V(u,v)=int I(theta)exp[-2pi i(u theta_x+v theta_y)]d²theta|EHT 2017 calibrated M87 visibilities released in 2019
Closure-phase station-gain invariance|arg(V_ab V_bc V_ca) cancels antenna phases; derive noise likelihood|EHT triangle closure phases
Closure-amplitude gain invariance|abs(V_ab V_cd/V_ac V_bd) cancels station amplitudes under multiplicative gains|EHT quadrangle visibility amplitudes
Ring-diameter visibility zeros|V_ring(q)=F J0(2pi q R) for ideal thin ring; derive finite-width/asymmetry corrections|EHT baseline-dependent visibility amplitude
Brightness depression versus shadow|I_center/I_ring depends on emissivity and absorption as well as capture boundary|EHT reconstructed central depression and visibility constraints
Photon critical curve from metric|for spherical baseline d(r²/A(r))/dr=0 gives critical impact b²=r²/A; extend to rotation explicitly|EHT ring scale and candidate stationary metric
Angular mass-distance degeneracy|theta_g=G_metric M/(c² D); ring data constrain alpha_ring theta_g|EHT measured angular morphology and external distance dependency
Emission-ring versus photon-ring calibration|d_emission=alpha_emission(metric,plasma,inclination)theta_g; derive alpha rather than set GR value|EHT intensity ring and radiative-transfer model library
Crescent asymmetry Doppler map|I_nu proportional to D³ j_(nu/D) integrated along rays; separate flow velocity from metric|EHT azimuthal brightness asymmetry
Scattering transfer uncertainty|V_obs=V_intrinsic exp[-D_phi(b)/2] for ensemble scattering model; test applicability to M87|EHT wavelength/baseline data and scattering prior
Four-day variability covariance|V_d=V_mean+deltaV_d; infer common metric with day-specific plasma|EHT April 2017 four observation days
Imaging-prior posterior transport|compare image reconstructions via forward visibilities, not independent image-pixel likelihoods|EHT alternative imaging pipelines and common calibrated data
Station-gain hierarchical inference|V_obs,ab=g_a g_b* V_true,ab+n; marginalize gains constrained by closure quantities|EHT station calibration products
Sparse-uv nullspace characterization|find deltaI with sampled Fourier transform zero; identify morphology not constrained by data|EHT actual baseline sampling
Ring ellipticity metric-plasma degeneracy|e_image=e_metric+e_projection+e_emissivity to first order; compute full response beyond additive limit|EHT ring-shape likelihood and inclination uncertainty
High-frequency visibility compact flux|F_compact from long-baseline amplitudes versus total flux; propagate unresolved-jet contamination|EHT compact-source visibility and ancillary flux data
Thermal optical-depth shadow mimic|I_nu=int j_nu exp(-tau_nu)dl; quantify whether central dimming requires photon capture|EHT intensity constraints and explicitly uncertain emissivity
Horizon existence inference boundary|critical photon orbit does not prove horizon; compare metrics sharing exterior photon region|EHT ring observables and candidate boundary conditions
Kerr comparison without imported solution|derive candidate stationary exterior before mapping spin to critical curve|EHT GR-conditioned mass/spin simulation interpretation
Matter-photon same-metric ray tracing|Hamilton equations from H=1/2 g^munu p_mu p_nu=0; connect to candidate matter coupling|EHT visibility prediction and common action
Preferred-foliation near-hole regularity|global time gradient timelike/admissible through ray region; audit criterion-B compatibility|EHT probed exterior region and candidate foliation
Heat-filter curved-slice definition|S=exp[(xi²/2)Delta_h] with measure and boundary; vary metric dependence in near-hole field equations|EHT angular gravitational scale and candidate xi
Canonical-alternative shadow sensitivity|partial theta_crit/partial rho_L at fixed mass,distance; quantify whether EHT can resolve vacuum footing|EHT ring uncertainty and distinct a0 normalizations
M87 stellar-dynamics cross-calibration|compare G_dyn M from stellar kinematics with G_light M from critical curve using shared distance|EHT ring data and independently authenticated stellar-kinematic source
EHT data-release reproducibility certificate|hash calibrated visibility inputs, recreate closure observables and residual norms for one candidate image|Official 2019-D01-01 repository; payload must be downloaded/authenticated before execution
''')
# Release-specific physical bridges and falsifiers. These are authoring instructions,
# not claims that data products or candidate dynamics have already been computed.
contexts={
(2017,1):('GW170104','Vary the reduced tensor action, derive source energy balance and retarded propagation, then project geodesic deviation onto the two interferometers.','6 tensor propagation; 7 criterion-B evolution; 10 measured-G recovery','Reverse the frequency-dependent propagation phase while holding the injected source waveform fixed; the signed propagation statistic must reverse, not remain spuriously unchanged.','Inject a nondispersive coherent signal into independently selected off-source detector noise and recover zero excess phase within calibrated coverage.','the lower-mass GW170608 inspiral, with one shared propagation coefficient','GW170104 strain is reused in GWTC-1. Select one strain analysis or condition the update on the old data; calibration nuisance is shared with O2 events.'),
(2017,2):('GW170814','Derive the two tensor polarizations from the reduced action and calculate the detector-arm response in each measured site tetrad.','2 gravitational DOF; 6 standard tensor polarizations; 7 preferred-time evolution','Apply an unphysical relative time shift to Virgo alone; the network coherence or null-stream statistic must detect the mismatch.','Predict the withheld Virgo response from the LIGO channels and compare with off-source calibrated residuals.','the action constraint count, which is not established by observing two detector-response modes','The same three strain channels support all polarization tasks and GWTC-1. Alternative polarization fits and sky localizations are correlated summaries, not independent observations.'),
(2017,3):('GW170817','Derive source binding energy, tensor propagation and photon null characteristics from one matter-coupled action; derive source and observer clock conversion.','6 tensor speed; 11 single physical metric; 7 criterion B; 10 compact-source recovery','Inject a known artificial photon/GW delay and require recovery after marginalizing the explicitly stated intrinsic-emission-lag family.','Check photon and tensor arrival functionals independently in the derived GR limit, including endpoint clocks.','the independent host-distance and redshift route after those inputs are authenticated','GW170817 timing, strain, tidal inference and siren distance reuse one event. Do not multiply event posteriors or count its GWTC-1 entry again; electromagnetic lag priors remain shared.'),
(2017,4):('GW170608','Derive the conservative binary Hamiltonian and radiative flux from the same action, then obtain waveform phase by energy balance and detector response.','6 tensor radiation; 10 Newtonian/GR recovery; 2 gravitational DOF','Inject a phase term with a known nonzero negative-PN coefficient; a fitting procedure that silently fixes it to zero must fail the recovery test.','Compare the phase derivative reconstructed in time and frequency domains using independent numerical differentiation/integration.','GW170104 mass-scaling consistency at the same radiation and conservative couplings','GW170608 is a separate event from GW170104 but shares O2 calibration; it is later reanalysed in GWTC-1. Use strain only once and retain common calibration covariance.'),
(2017,5):('MICROSCOPE first result','Vary the ordinary-matter action, derive force balance and finite-body acceleration, then pass it through orbit, attitude and closed-loop instrument response.','5 ordinary matter conservation; 10 Newtonian recovery; 11 universal metric coupling','Inject a composition-antisymmetric force at the equivalence-principle modulation frequency; ensure the estimator does not absorb it into a common-mode or thermal nuisance.','Use the same-composition/reference-channel prediction where that channel is actually obtainable, keeping its calibration independent of the science fit.','strong-body free fall in J0337, with a separately derived sensitivity map','All tasks reuse the first-result sessions. Later MICROSCOPE releases contain overlapping measurements; any update must be conditional on shared sessions and calibration.'),
(2017,6):('DES Y1 cosmic shear','Derive both metric potentials and cosmological perturbations from the action; integrate photon geodesic deviation, intrinsic shapes and survey selection to obtain the measured shear statistic.','3 derived lensing potentials; 8 cosmology; 1 filtered MONO static limit','Rotate every source ellipticity by 45 degrees while retaining positions and weights; E/B parity diagnostics must change as predicted and cannot reproduce the original cosmological signal.','Evaluate the same candidate spectrum through real-space and harmonic-space projections with independently implemented mask/window normalization.','the DES Y1 galaxy-shear/clustering conditional likelihood','Cosmic shear is included in DES Y1 3x2 and shares footprint with DES BAO. Use one joint data vector and its cross-covariance, never separate multiplied shear and 3x2 posteriors.'),
(2017,7):('DES Y1 joint 3x2','Derive baryon/galaxy evolution, both metric potentials and photon deflection from one action, retaining explicit galaxy selection and bias as observational nuisance.','3 lensing; 8 cosmology; 5 matter conservation','Randomize lens positions within the mask while retaining source shapes; galaxy-shear correlation should vanish apart from the calibrated mask/random correction.','Check positive-semidefinite joint field covariance and reproduce a common mock in both projected-density and ray-deflection representations.','velocity-based dynamical potentials from independently authenticated tracers','The shear block is the same DES Y1 measurement as the standalone shear paper. Clustering/lensing increments must condition on it, with shared objects, sky modes and photo-z calibration retained.'),
(2017,8):('eBOSS DR14 quasar isotropic BAO','Derive the candidate FLRW distance map and photon-baryon acoustic ruler, then redshift-space tracer evolution, pair selection and the survey-window estimator.','8 expanding cosmology; 5 matter conservation; 13 scale-vacuum relation','Replace the acoustic wiggles by a smooth spectrum while keeping broadband shape and mask fixed; acoustic detection significance must fall to the calibrated null distribution.','Fourier transform the convolved power-spectrum prediction and compare with the independently integrated configuration-space estimator.','the later DR14 anisotropic distance derivative, conditioned on identical quasars','DR14 quasars recur in the 2018 weighted report and later SDSS releases. The new output here is the isotropic statistic; later anisotropic information is conditional, not a new independent catalog.'),
(2017,9):('Pantheon first report','Derive luminosity distance from the candidate metric and photon-number transport; explicitly model stellar standardization, photometric calibration and detection selection.','8 expanding FLRW; 11 photon metric; 13 vacuum matching','Apply a known coherent magnitude offset to one survey and require the calibration-sensitive statistic to recover it rather than falsely attributing it to gravity.','Check the analytic absolute-magnitude/H0 degeneracy and independently integrate the metric luminosity-distance relation.','independent angular-distance or standard-siren measurements after object and calibration overlap audits','Pantheon aggregates older supernova surveys and is reused by later compilations and distance ladders. Match supernova IDs and retain shared photometric calibration; proposed outputs are new applications, not newly observed supernovae.'),
(2017,10):('DES Y1 photometric BAO','Derive radial and angular distance maps and acoustic propagation from one action, then project through the observed photometric-redshift selection.','8 background evolution; 13 vacuum acceleration scale','Replace the true photo-z kernel by an intentionally displaced narrow kernel; the derived acoustic-scale bias must be recovered in mock validation.','Transform the predicted angular correlation to spherical-harmonic bandpowers using an independently calculated survey mask.','spectroscopic DR14 acoustic distances with their different redshift kernel','The three DES BAO estimators reuse the same galaxies; DES Y1 shear and clustering share sky modes and sometimes objects. Select one estimator or use its full shared-data covariance.'),
(2018,1):('Planck 2018 parameters','Vary the background and finite-wavelength perturbation equations, evolve the declared photon/baryon/ordinary-neutrino content and candidate carrier, then derive line-of-sight temperature/polarization transfer.','8 cosmology; 9 controlled zero-field limit; 13 scale relation','Feed a spectrum with deliberately shifted acoustic phase into the pipeline; the phase-sensitive residual must not disappear through a scalar S8/H0 summary replacement.','Recover the declared GR comparison spectra using an independent Boltzmann implementation only after the candidate-to-GR limit is proved.','Planck four-point lensing, with shared-sky covariance','This source shares temperature/polarization maps with Planck lensing and earlier releases. Final-mission reprocessing is an incremental calibration/polarization result; never treat 2015 and 2018 as independent skies.'),
(2018,2):('Planck 2018 lensing','Derive the candidate Weyl potential, null-ray remapping and four-point estimator response, including disconnected/connected noise biases and survey masking.','3 lensing potentials; 8 structure growth; 7 perturbative health','Run an unlensed Gaussian sky through the reconstruction with the same mask; the debiased lensing signal must be consistent with its calibrated null.','Compare temperature-only and polarization-only reconstruction residuals with their shared-sky covariance rather than multiplying their posteriors.','galaxy cosmic shear through a separately derived low-redshift kernel','The reconstruction and acoustic-smoothing analyses share Planck sky modes. CIB combinations, delensed spectra and estimator splits are dependent summaries and require full cross-covariance.'),
(2018,3):('Gaia DR2','Derive finite-body trajectories from the filtered field equation and ordinary-matter conservation, then map them through astrometric projection, parallax likelihood and catalog selection.','1 filtered MONO; 5 conservation; 10 measured Newton coupling','Shuffle velocities or binary pair membership within the selection-matched sky sample; coherent dynamical correlations must be lost without changing the error model.','Validate astrometric coordinate/unit transformations on an independently integrated orbit and retain the full published covariance matrix.','pulsar timing accelerations with separately authenticated distances','DR2 sources overlap DR1 and later Gaia releases; source solutions have shared observations and calibration. Do not treat a release difference as independent acceleration or count matched stars twice.'),
(2018,4):('GRAVITY S2 redshift','Derive massive-star geodesics, photon rays and emitter-observer clock ratios in the same central metric; match the metric to the filtered outer solution.','4 PPN; 10 GR recovery; 11 common photon/matter metric','Inject a spectral zero-point step at pericentre and require the instrument-aware model to distinguish it from the relativistic temporal template.','Integrate the invariant frequency ratio directly and compare with its independently derived post-Newtonian expansion over the measured orbit.','Keck S0-2 pericentre spectroscopy as a distinct instrument, sharing orbit and environment','S2 and S0-2 are the same star. GRAVITY and Keck data are distinct observing streams with shared orbit/reference/environment nuisance; historic astrometry reused across papers is counted once.'),
(2018,5):('NGC1052-DF2','Solve the finite baryon-plus-host filtered field, derive the collisionless tracer dynamics and project the actual discrete tracer selection into a velocity likelihood.','1 MONO phenomenology; 5 conservation; 10 weak-field recovery','Inject an interloper with a known velocity offset into the tracer sample; membership and dispersion diagnostics must expose its leverage.','Compare the Jeans prediction with orbit-ensemble sampling in the same potential and a separately checked finite-boundary virial balance.','DF4 as a distinct galaxy sharing the host field','DF2 velocities are reused in later reanalyses; DF4 is a different galaxy but shares NGC1052 group distance,host potential and population assumptions. Preserve that common nuisance covariance.'),
(2018,6):('J0337 triple free fall','Derive compact-body sensitivities and three-body forces from the same action, solve the trajectory and proper-time pulse propagation, and project through the timing fit.','5 conservation; 10 strong-field recovery; 11 universal matter coupling','Inject a known differential-acceleration sideband and require its recovery after refitting all orbital and noise parameters.','Compare the timing response computed by variational equations with direct perturbed integration and independently computed conservation residuals.','MICROSCOPE weak-body composition response after deriving the strong/weak sensitivity relation','The single triple-system timing span supports all sideband/SEP tasks. Later reports extend or reprocess the same TOAs; identify incremental epochs and shared timing-system calibration.'),
(2018,7):('NANOGrav 11-year background search','Derive tensor propagation and photon timing response from the action, include Earth and pulsar terms, and pass the covariance through fitted timing-model projection.','6 tensor sector; 7 criterion B; 11 matter/photon metric','Scramble pulsar sky labels while preserving individual residuals; a claimed quadrupolar correlation must weaken while individual red noise remains.','Recover an injected tensor correlation with independently calculated angular overlap integrals while fitting separate clock and ephemeris processes.','the O2 high-frequency stochastic observable through an explicitly derived source spectrum','NANOGrav earlier/later releases and IPTA contain shared TOAs. Background limits,ephemeris alternatives and spectral models are dependent fits to one timing sample.'),
(2018,8):('GWTC-1','Derive event waveforms, detector likelihoods and source-population selection from one radiation sector and background distance map.','6 radiation; 10 GR recovery; 8 propagation background','Duplicate an event in a controlled catalog copy; the provenance-aware likelihood must reject the duplicate instead of tightening its common-theory bound.','Use the four newly reported events as a held-out set after fitting previously published events, keeping shared calibration parameters explicit.','the O2 stochastic background predicted from the same source population','GWTC-1 contains the 2017 GW events plus new reports and reanalysis. Do not count old and new posteriors independently; catalog rates share selection data and event likelihoods.'),
(2018,9):('HSC first-year cosmic shear','Derive both potentials and growth, then spin-two photon deflection, source redshift weighting and the pseudo-spectrum mask/calibration operator.','3 lensing; 8 structure formation; 1 filtered response','Inject a PSF-shaped ellipticity field with no gravitational shear; the PSF/B-mode diagnostics must reject its cosmological interpretation.','Calculate the same masked shear observable using ray-traced synthetic fields and an independently evaluated harmonic mixing matrix.','DES Y1 shear after matching source-depth kernels and sky overlap','HSC first-year power-spectrum and later configuration-space/peak analyses reuse galaxies. DES has some common sky modes; count each galaxy catalog once and retain overlap covariance.'),
(2018,10):('eBOSS DR14 weighted anisotropic BAO','Derive the candidate radial/transverse distance relation and acoustic ruler, then the actual signed redshift-weighted pair estimators.','8 FLRW; 13 scale relation; 5 tracer conservation','Artificially set off-diagonal distance-coefficient covariance to zero and demonstrate the resulting incorrect endpoint or derivative uncertainty.','Differentiate the reconstructed comoving-distance function and compare its H(z) with the independently inferred radial acoustic dilation.','the original 2017 quasar monopole through a conditional same-data likelihood','This is a new anisotropic/redshift-weighted measurement from the same DR14 quasars as the 2017 isotropic report. Its information gain comes from new projections, not independent observations.'),
(2019,1):('Keck S0-2 redshift','Derive the invariant photon frequency ratio and central stellar orbit together, with explicit instrument response and historical astrometric-frame covariance.','4 PPN; 10 GR recovery; 11 single metric','Inject a pericentre-correlated instrumental velocity drift and require separate nuisance diagnostics to flag its redshift-template overlap.','Predict post-pericentre velocities from a pre-pericentre fit and compare exact-geodesic and post-Newtonian implementations.','the GRAVITY observing stream for the same star with telescope-specific noise','S0-2 is S2; 2019 reports new Keck pericentre measurements plus old astrometry, not a new object. Joint use with GRAVITY shares orbit,group environment and reference frame.'),
(2019,2):('H0LiCOW XIII','Derive both metric potentials, the photon arrival-time functional and stellar dynamics from one action, then fit imaging,delays and kinematics jointly.','3 lensing; 4 PPN; 8 cosmology; 13 vacuum scale','Apply a mass-sheet transformation to a synthetic lens; imaging-only inference must retain the corresponding distance degeneracy rather than claim it is broken.','Independently ray-trace image positions/delays and solve stellar orbit or Jeans dynamics for the identical physical lens potential.','supernova relative distances or a standard siren with independent calibration','The six-lens combination reuses earlier lens measurements; do not multiply individual-lens and combined distance posteriors. Time delays share light curves, and stellar/environment nuisance recurs across analyses.'),
(2019,3):('SH0ES 2019 LMC calibration','Derive the background luminosity-distance relation and any candidate-dependent stellar clock/luminosity response, then propagate calibration and selection through the distance ladder.','8 cosmology; 10 stellar high-field recovery; 13 scale relation','Offset the LMC photometric zero point by a known amount and require the inferred absolute-magnitude/H0 shift to match the analytic calibration Jacobian.','Fit each geometric anchor held out in turn, predicting its calibration from the others while retaining common HST and supernova covariance.','time-delay lenses or standard sirens with distinct absolute-calibration systematics','New LMC HST photometry updates a ladder containing older Cepheids and supernovae. Overlap with Pantheon and later SH0ES releases requires object matching and shared-calibration covariance.'),
(2019,4):('eBOSS DR14 Ly-alpha BAO','Derive background/acoustic evolution and baryon gas dynamics, then neutral-hydrogen radiative transfer,redshift-space mapping and continuum-projected flux correlations.','8 cosmology; 5 matter conservation; 13 scale-vacuum relation','Inject a metal-line correlation at its wavelength-offset separation; the contamination-aware estimator must not misidentify it as acoustic dilation.','Recover the radial/transverse acoustic scale from independent configuration-space and forward spectral-transfer calculations with identical masks.','quasar-density BAO with distinct bias physics and common survey modes','The forest and quasar samples share sightlines and cosmological modes; Ly-alpha/Ly-beta-region correlations reuse spectra. Auto/cross-correlation combinations need their joint covariance.'),
(2019,5):('IPTA DR2','Derive pulsar clock,orbital and tensor timing responses from the common action, then transform observatory clocks and merge uniquely identified arrival times.','6 tensor timing; 10 orbital recovery; 11 common matter/photon metric','Insert duplicate TOAs from overlapping regional archives; the merge and likelihood pipeline must reject them rather than gain false precision.','Withhold one regional observing stream and predict its residual distribution after fitting common pulsar dynamics to the remaining independent measurements.','Gaia-based kinematic acceleration and distance constraints after source matching','IPTA DR2 combines EPTA,NANOGrav and PPTA records, often for the same pulsars and observations. Maintain telescope/epoch/backend provenance and condition any NANOGrav combination on reused TOAs.'),
(2019,6):('NICER J0030','Derive stellar equilibrium and exterior metric from the action, then surface radiation,ray propagation,rotational clocks and detector photon counts.','10 compact-star recovery; 11 photon metric; 7 stellar health','Replace the energy-dependent response by an intentionally incorrect flat area and require energy-resolved residuals to reveal the induced compactness/temperature bias.','Compute photon bending/redshift using an independent geodesic integrator and compare held-out phase-energy bins, not just the fitted mass-radius contour.','J0740 radio timing through a shared ordinary-matter EOS and gravity cell','Miller and companion spot-model analyses use the same NICER J0030 photons. Their posteriors are alternative analyses, not independent data; later reprocessings share exposure and response calibration.'),
(2019,7):('J0740 Shapiro timing','Derive pulsar binary trajectories,clock rates and photon time delay from the same compact-body metric and matter coupling, then fit the actual timing design.','4 PPN; 10 strong-field recovery; 11 metric universality','Inject a chromatic conjunction delay; a valid Shapiro analysis must identify its frequency dependence rather than convert it directly into companion mass.','Compare conjunction timing harmonics in range/shape and orthometric coordinates including the exact prior Jacobian.','NICER J0030 stellar structure under the same EOS and gravitational couplings','Targeted conjunction observations augment a NANOGrav baseline. The timing mass and later PTA release reuse TOAs; do not multiply the derived mass posterior by its parent data likelihood.'),
(2019,8):('NGC1052-DF4','Derive the host-plus-dwarf filtered potential and collisionless stellar/tracer evolution, then the discrete and integrated-light spectroscopic observables.','1 MONO response; 5 conservation; 10 weak-field limit','Deliberately replace the diffuse-light systemic velocity by a dispersion estimate; the observation-type audit must reject this invalid input substitution.','Check the derived aperture dispersion with independently sampled orbits and use DF2 only through a shared-host conditional prediction.','DF2 as an environmental comparison with distinct tracer velocities','DF4 is distinct from DF2, but group distance,host potential and some calibration assumptions are shared. Reanalyses of DF4 velocities are not independent realizations.'),
(2019,9):('LIGO O2 stochastic search','Derive tensor stress-energy,propagation and detector cross-correlation response from the same action; account separately for correlated environmental noise.','6 tensor dynamics; 7 positivity; 8 background propagation','Apply an unphysical detector time slide or inject a known magnetic correlation; the gravitational interpretation must fail the appropriate coherence/environmental test.','Integrate the overlap-reduction function independently and validate the full estimator on signal-free noise with the actual segment/window selection.','GWTC-1 source-population energy budget without assuming a new particle sector','O2 and O1 segments are reused in event catalogs and later stochastic releases. Event excision/selection and shared calibration link catalog and stochastic analyses; overlapping runs are counted once.'),
(2019,10):('EHT M87 first ring','Derive a stationary candidate exterior metric,photon Hamiltonian and plasma radiative transfer, then Fourier-sample the image through the interferometer response.','3 photon deflection; 10 strong-field recovery; 11 common metric; 7 criterion B','Randomize station-independent closure phases while preserving visibility amplitudes; a claimed asymmetric image must fail closure-data prediction.','Check station-gain cancellation in closure quantities and independently ray-trace a limiting metric with analytically known photon critical curve.','stellar-dynamical mass-distance information for M87 after separate source authentication','All 2019 M87 imaging/modeling papers reuse four days of 2017 visibilities. Images,closure products and GR-simulation mass inferences are correlated transformations, not separate datasets.')
}
SCALE=('Use a0=(c/2)sqrt(G_N rho_Lambda), with rho_Lambda a mass density and 1/2 explicitly adopted unless independently derived. '
       'Keep canonical a0=9.3619e-11 and alternative a0=1.1279e-10 m/s² as distinct fixed models; G_N,G_E,G_bare,G_cosmo are not identified without proof. ')
DISCIPLINE=('Pin action revision,matter coupling,heat-filter metric/measure/domain/boundaries,kernel,gate and initial data. '
            'Filtered MONO is operative; Q,RAR and MU2 are comparison branches unless an observation-map bridge is proved. '
            'No extra particles or per-object force fits may silently repair a mismatch. Criterion B uses a global preferred time; classical agreement is not quantum completion or thirteen-gate closure. ')

for year in (2017,2018,2019):
 sources=json.loads((P/f'{year}_sources.json').read_text())
 tasks=[]
 for s,source in enumerate(sources,1):
  label,foundation,gates,negative,independent,bridge,overlap=contexts[year,s]
  rows=blocks[year,s]
  for j,(name,eq,inputs) in enumerate(rows):
   idx=(s-1)*25+j+1
   tid=f'MY{year}-{idx:03d}'
   nxt=rows[(j+1)%25]
   kind='audit' if any(k in name.lower() for k in ('audit','portability','boundary','certificate','accounting','fallacy','ceiling','scope','sufficiency')) else 'derivation' if any(k in name.lower() for k in ('map','derivation','bridge','matching','response','transfer','equation')) else 'inference'
   priority='P0' if j in (0,1,2,24) else ('P1' if j<20 else 'P2')
   tasks.append({
    'id':tid,'year':year,'source_id':source['source_id'],'title':f'{label}: {name}',
    'principle':f'{name} must be inferred from the measured observation functional and its nuisance directions. A source-reported GR/LambdaCDM posterior is conditional on its original observation map; this task seeks a new, explicitly scoped candidate-theory result.',
    'math':eq+'. Symbols are task-local; define units,normalizations and domains before calculation. Approximate/GR reference expressions in this work order are diagnostic limits to derive, not an asserted candidate law.',
    'measurement_input':inputs+'. Anchor: '+source['primary_url']+'. '+source['data_access']+' Any additional measurement named here must receive its own primary-source authentication and version pin before use; otherwise give a symbolic/partially identified result.',
    'deliverable':f'{tid}: deliver {name.lower()} as an explicit observation-map derivation and a reproducible equation/estimand evaluation, with its numerical region or non-identifiability witness, nuisance covariance and approximation-error envelope. Save the unique result as {tid.lower()}_result.md plus its task-specific input/likelihood manifest; no catalog-authoring step executes this calculation.',
    'steps':[
     f'Authenticate the pinned {source["identifier"]} measurement version and extract only the inputs required for {name.lower()}: {inputs}. Separate measured quantities from derived GR parameters, mark inaccessible data, and lock the source/selection/covariance provenance.',
     f'{foundation} Specialize that derivation to {name.lower()}; identify the precise observable and all approximation conditions before using the displayed estimand.',
     f'Derive and evaluate the task equation: {eq}. Carry the actual release window,units and nuisance correlations; if information is missing, compute the admissible symbolic range or rank deficiency rather than inventing a central value.',
     f'Run the negative and independent controls below on this estimand, then propagate their residuals into the uncertainty/error budget for {name.lower()}. State whether each check is analytic, finite numerical or data-limited.',
     f'Write the {tid} result with an explicit allowed/excluded/unidentified parameter region or conditional lemma, the release-overlap ledger and the exact implication to {gates}. Separate new evidence from unproved dynamics and nominate the three continuations below.'
    ],
    'controls':[
     'Negative control: '+negative+f' Evaluate its effect on the specific {name.lower()} statistic, not only on a global fit score.',
     'Independent control: '+independent+f' Archive the residual relevant to {name.lower()} and its units; a Boolean success is insufficient.',
     'Inference control: repeat the actual '+name.lower()+' estimand after an admissible nuisance/approximation change identified in the displayed equation; report whether any apparent gravity sensitivity is entirely prior or truncation driven.'
    ],
    'first_principles':foundation+' The obligation is specifically '+eq+'. '+SCALE+DISCIPLINE,
    'closure_bridge':f'The output for {name.lower()} can constrain {gates} only after the action-to-observable derivation above is established. Transfer the actual allowed region and error/domain conditions to one shared action cell; a missing dynamical map is an OPEN dependency, and an empirical fit cannot certify the other thirteen-gate requirements. '+SCALE,
    'new_information':f'New proposed application of the {source["report_date"]} {label} report: obtain {name.lower()}, specifically {eq}. This is an additional release-resolved estimand/conditional theorem beyond the old AS catalog\'s generic action,projection and evidence obligations; it does not claim that this historical measurement was unavailable in 2026, nor claim a literature novelty theorem. Other tasks on this source seek different mathematical outputs from the same data.',
    'overlap_handling':overlap+f' The 25 work orders attached to {source["source_id"]} are correlated analyses, not 25 datasets. For {name.lower()}, identify every reused row/epoch/mode and share the corresponding nuisance block before any combined significance or information-gain calculation.',
    'continuation':[
     f'Promising extension: carry the derived {name.lower()} likelihood/domain into the neighboring, distinct question "{nxt[0]}". Derive its new target {nxt[1]}, including cross-response/covariance with the present output; do not count the reused release as independent evidence.',
     f'Independent bridge: use the explicit {name.lower()} result to predict a matching observable in {bridge}. Derive the translation from the same action and authenticate that second observation before a joint inference.',
     f'Failed-route repair: if {name.lower()} fails its control or is not identifiable from {inputs}, preserve the failing residual/null direction. Determine the minimum additional calibrated observable or action-derived term that separates the degeneracy in {eq}; if none exists within the pinned model, deliver the scoped obstruction rather than retuning gravity per object.'
    ],
    'depends_on':[], 'priority':priority, 'kind':kind
   })
 assert len(tasks)==250
 assert len({x['title'] for x in tasks})==250
 assert len({x['math'] for x in tasks})==250
 def prose_spacing(v):
  if isinstance(v,str): return re.sub(r',(?=[A-Za-z])', ', ', v)
  if isinstance(v,list): return [prose_spacing(x) for x in v]
  if isinstance(v,dict): return {k:prose_spacing(x) for k,x in v.items()}
  return v
 tasks=prose_spacing(tasks)
 (P/f'{year}_tasks.json').write_text(json.dumps(tasks,indent=2,ensure_ascii=False)+'\n')
 print(year,len(tasks),'tasks',len(sources),'sources')
