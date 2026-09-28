import json,re
from pathlib import Path
OUT=Path(__file__).parent
S={}; K={}
def source(year,n,short,ident,date,title,authors,measurement,epoch,family,bridge,inputs,negative,independent,increment,version='v1 first-report scope; abstract page may display a later revision'):
 sid=f'Y{year}S{n:02}'
 url='https://arxiv.org/abs/'+ident
 S[sid]=dict(source_id=sid,year=year,title=title,authors_or_collaboration=authors,primary_url=url,identifier='arXiv:'+ident,report_date=date,date_precision='day',date_basis='First submission of this measurement/data-report on the opened primary arXiv page; observation and any earlier alert epochs are separate. Later revisions are not new calendar-year measurements.',version=version,observation_epoch=epoch,measurement=measurement,data_access='Primary report abstract and metadata accessible. Raw arrays, covariance, selection function and executable likelihood not inspected; obtain and pin these before numerical inference, otherwise deliver only the conditional observation map and a precise missing-data list.',verification='Opened primary abstract page and read reported observables and submission history. No full likelihood or numerical table authentication is claimed.',source_locator='Abstract and submission history',overlap_family=family,search_queries=['Direct primary-page identifier lookup: '+ident],checked_on='2026-09-27')
 K[sid]=dict(short=short,bridge=bridge,inputs=inputs,negative=negative,independent=independent,increment=increment,seeds=[])
 return sid
def seeds(sid,text):
 for line in text.strip().splitlines():
  a=line.split(' | ')
  assert len(a)==3,(sid,line)
  K[sid]['seeds'].append(a)

source(2020,1,'eBOSS final','2007.08991','2020-07-17','The Completed SDSS-IV extended Baryon Oscillation Spectroscopic Survey: Cosmological Implications from two Decades of Spectroscopic Surveys at the Apache Point observatory','eBOSS Collaboration; S. Alam et al.','Final BAO distance and redshift-space growth measurements across galaxy, quasar and Ly-alpha samples.','SDSS lineage over two decades; exact tracer epochs require extraction','SDSS_BOSS_eBOSS','Derive the homogeneous expansion, sound horizon and linear velocity transfer from one action; gates 8,10,13.','Published tracer distance/growth vectors, window functions, redshift distributions and cross-covariance; cosmological posteriors are comparison products.','scramble tracer redshift labels while keeping errors fixed','recover the survey fiducial ruler convention in a GR reference reduction','2020 final multi-tracer compression permits distance-growth consistency and overlap-aware increments beyond an abstract FLRW seed')
source(2020,2,'KiDS-1000 shear','2007.15633','2020-07-30','KiDS-1000 Cosmology: Cosmic shear constraints and comparison between two point statistics','M. Asgari et al.','Cosmic shear measured with COSEBIs, correlation functions and band powers.','KiDS fourth-release imaging; exact exposure dates uninspected','KiDS_imaging','Derive both metric potentials and light deflection before projecting the same-action matter response; gates 1,3,8,13.','Tomographic shear statistics, angular masks, redshift distributions, calibration nuisance data and their joint covariance.','rotate source ellipticities by 45 degrees','compare equivalent E-mode projections with their shared covariance','2020 KiDS-1000 multi-statistic release exposes filter-scale and tomographic residuals not fixed by an old generic S8 obligation')
source(2020,3,'ACT DR4','2007.07288','2020-07-14','The Atacama Cosmology Telescope: DR4 Maps and Cosmological Parameters','S. Aiola et al.','Temperature and polarization maps and angular power spectra at two frequencies.','2013–2016','ACT_CMB','Derive photon-baryon, metric and tensor transfer functions from the same action, with ordinary matter conservation; gates 5,6,8,13.','ACT temperature/polarization band powers, beams, masks, frequency calibration and covariance; no substitution of its LCDM H0 posterior.','shuffle the TE sign between alternating acoustic bands','recover a published GR reference spectrum through the ACT window operator','2020 arcminute ACT maps provide a distinct measured acoustic response and sky-mask operator beyond generic CMB predictions')
source(2020,4,'Planck NPIPE','2007.04997','2020-07-09','Planck intermediate results. LVII. Joint Planck LFI and HFI data processing','Planck Collaboration; Y. Akrami et al.','Joint LFI/HFI frequency maps, Solar dipole and large-scale polarization reprocessing.','Planck mission observations reprocessed; no new sky claimed','Planck_CMB','Propagate same-action metric and radiation transfer into the actual map-calibration operator; gates 5,8,13.','NPIPE map differences, dipole calibration, polarization spectra and end-to-end simulations; archive files not inspected.','reverse a detector-set calibration correction','compare detector-set cross spectra and explicitly account for their shared sky','NPIPE adds calibration and simulation information to older Planck observations; all proposed results isolate processing increments')
source(2020,5,'GWTC-2 O3a','2010.14527','2020-10-27','GWTC-2: Compact Binary Coalescences Observed by LIGO and Virgo During the First Half of the Third Observing Run','LIGO Scientific Collaboration and Virgo Collaboration','O3a compact-binary candidate detections and waveform-conditioned source properties.','2019-04-01 to 2019-10-01; some low-latency alerts preceded catalog','LVK_O3a','Derive radiative tensor equations, source motion and detector response; gates 2,5,6,7,10.','O3a strain or likelihood, PSDs, calibration and detection efficiency; posterior samples alone require prior removal and waveform support checks.','time-slide detectors to destroy coherent events','validate the GR limit using a separately implemented detector-response calculation','New catalog parameter estimation and previously unreported candidates add a population-level measurement; repeated single events count once')
source(2020,6,'GW190521 report','2009.01075','2020-09-02','GW190521: A Binary Black Hole Merger with a Total Mass of 150 Solar Masses','LIGO Scientific Collaboration and Virgo Collaboration','Short coherent gravitational-wave transient with merger-conditioned parameter inference.','2019-05-21; 2020 detailed parameter report','LVK_O3a','Derive the strong-field merger or an explicitly controlled ringdown reduction of the same action; gates 2,6,7,10.','GW190521 strain, PSD and calibration, time-frequency morphology and conditional source posterior.','shift the ringdown fit window into off-source strain','repeat with a waveform-agnostic coherent transient reconstruction','2020 detailed short-signal report permits a merger-versus-propagation identifiability result unavailable from generic GW tests')
source(2020,7,'GW190814 report','2006.12611','2020-06-22','GW190814: Gravitational Waves from the Coalescence of a 23 Solar-Mass Black Hole with a 2.6 Solar-Mass Compact Object','LIGO Scientific Collaboration and Virgo Collaboration','Asymmetric compact-binary signal and inferred mass/spin information.','2019-08-14; 2020 detailed parameter report','LVK_O3a','Derive same-action conservative dynamics and tensor multipoles in the asymmetric binary regime; gates 2,6,10.','GW190814 strain likelihood, frequency-dependent PSD and calibration; matter identity remains waveform-dependent.','suppress all subdominant modes in an injection with them present','recover the GR asymmetric-mass reference with independent waveform families','2020 asymmetric event opens separate multipole, tidal-degeneracy and strong-field calibration outputs beyond a universal propagation bound')
source(2020,8,'TDCOSMO IV','2007.02941','2020-07-06','TDCOSMO IV: Hierarchical time-delay cosmography -- joint inference of the Hubble constant and galaxy density profiles','S. Birrer et al.','Hierarchical time-delay and stellar-kinematic lens inference allowing mass-sheet freedom.','Previously observed time-delay lenses; new 2020 hierarchical measurement','TDCOSMO_H0LiCOW_lenses','Derive timelike and null geodesics from independently derived Phi and Psi before fitting time delays; gates 3,4,8,11,13.','Lens image positions, time delays, stellar kinematics, aperture response and environment priors; full joint data still to authenticate.','apply an untracked mass-sheet transform','check one lens with both image-plane and Fermat-potential residual calculations','2020 flexible-profile inference gives new degeneracy information on old lenses; its H0 result is not independent of H0LiCOW')
source(2020,9,'Gaia EDR3','2012.01533','2020-12-02','Gaia Early Data Release 3: Summary of the contents and survey properties','Gaia Collaboration; A. G. A. Brown et al.','Updated positions, parallaxes, proper motions and photometry; radial velocities largely carried from DR2.','Gaia early third-release observing baseline; exact dates require source extraction','Gaia_stellar_astrometry','Derive timelike motion in filtered MONO and project into angular astrometry with selection; gates 1,4,10.','EDR3 parallax/proper-motion covariance, photometry and astrometric flags; DR2 velocities are not fresh EDR3 measurements.','shuffle proper-motion vectors among matched-position stars','validate a high-acceleration astrometric control with external distances','EDR3 changes astrometric precision and systematics, enabling new correlated-error limits rather than another generic galaxy force fit')
source(2020,10,'SPARC environment report','2009.11525','2020-09-24','Testing the Strong Equivalence Principle: Detection of the External Field Effect in Rotationally Supported Galaxies','K.-H. Chae et al.','Rotation-curve residuals compared with independently estimated galaxy environments.','Existing SPARC rotation curves plus new 2020 environment comparison','SPARC_rotation_environment','Solve the actual nonspherical filtered MONO boundary problem before defining an external-field observable; gates 1,7,9,12,13.','Rotation curves, baryonic photometry, distances/inclinations and environment estimates with common catalog covariance.','permute environment strengths among matched baryonic profiles','compare exceptionally isolated systems using the same selection rule','2020 external-field estimates and blind environment comparison add a measured boundary condition to old SPARC curve tasks')
seeds('Y2020S01','''
Transverse ruler cancellation | R_ij=D_M(z_i)/D_M(z_j) | eliminate the shared sound horizon before testing expansion shape
Radial ruler cancellation | R_H=H(z_i)/H(z_j) | isolate relative expansion from radial BAO
Alcock Paczynski closure | F_AP=D_M H/c | derive a ruler-free angular-radial consistency relation
Curvature transport | [H D_M'/c]^2=1+Omega_k(H0 D_M/c)^2 | test curvature with covariance-aware derivatives
Sound horizon boundary | r_d=integral_zd^infty c_s/H dz | bound the early-time input required by the final BAO scale
Growth source reconstruction | D''+(2+H'/H)D'=S_grav D | reconstruct the source from the six RSD growth measurements
Velocity continuity transfer | theta=-aH f delta | derive the observable when ordinary matter continuity is action-derived
Tracer bias cancellation | P_gtheta^2/(P_gg P_thetatheta) | isolate deterministic bias failure across overlapping tracers
Redshift-window averaging | m_i=integral W_i(z)f(z)sigma8(z) dz | quantify effective-redshift compression bias
Reconstruction displacement response | x_rec=x-s; div s=-delta_g/b | bound use of GR reconstruction on filtered gravity
Ly-alpha anisotropic dilation | alpha_parallel=H_fid r_dfid/(H r_d) | separate the forest line-of-sight dilation from flux bias
Quasar transverse selection | delta_obs=delta_q+s_dust E | project measured angular completeness out of the ruler
LRG velocity dispersion | P_s=(b+f mu^2)^2 P exp[-k^2 mu^2 sigma_v^2] | infer where damping obscures the action-derived force
ELG stochastic growth | P_eps=P_gg-b^2 P_mm | recover the growth information lost to tracer stochasticity
Cross-tracer covariance rank | C_joint=[[C_a,C_ab],[C_ab.T,C_b]] | determine independent information in the final compilation
Ruler-free vacuum scale | a0/H0=c sqrt(3 Omega_L G_N/G_cosmo/(32 pi)) | state the cosmology and coupling premises behind the scale relation
Vacuum density derivative | d ln a0/d ln a=0.5 d ln rho_L/d ln a | constrain time evolution only after a background bridge
Distance-growth mismatch | r_g=f_sigma8_obs-f_sigma8[H_BAO] | identify missing dynamical response at fixed measured geometry
Wide-angle RSD correction | xi_s=xi_pp+(s/chi)^2 xi_wa | bound plane-parallel leakage into low-k growth
Integral-constraint mode | delta_obs=delta-mean_W(delta) | quantify the unmeasured homogeneous density mode
Fiducial cosmology Jacobian | P_obs=kJac P_true; kJac=alpha_perp^-2 alpha_parallel^-1 | transport the published compression to a new expansion model
Scale-dependent growth band | f_eff=integral W(k)f(k,z) dk | translate filtered response into the reported growth estimator
BAO phase versus amplitude | P=P_sm[1+A sin(k r_d+phi)] | separate phase displacement from changed growth amplitude
Survey-volume boundary response | delta m=J_boundary delta Phi_boundary | bound sensitivity of the final modes to nonlocal filter boundaries
Incremental legacy information | C_new|old=C_new-C_no C_old^-1 C_on | isolate final eBOSS information beyond earlier SDSS summaries
''')
seeds('Y2020S02','''
COSEBI heat-scale response | dE_n/dxi=integral T_n(theta) dxi_plus/dxi dtheta | locate measured modes sensitive to the operative heat filter
E-B ambiguous-mode bound | E_n=integral theta[Tplus xi_plus+Tminus xi_minus]/2 | separate finite-angle ambiguity from gravitational slip
Band-power window transport | C_b=integral W_b(ell)C_ell dell | derive the exact projection of a candidate Weyl spectrum
Tomographic source shift | delta C_ell=integral (delta W_i W_j+W_i delta W_j)P dchi/chi^2 | resolve redshift-calibration degeneracy with growth
Low-redshift bin leverage | DeltaF=F_all-F_without_bin2 | quantify information and contamination from the reported anomalous bin
Intrinsic alignment response | C_obs=C_GG+C_GI+C_II | derive a separable tidal-alignment nuisance operator
Multiplicative shear degeneracy | C_ij_obs=(1+m_i)(1+m_j)C_ij | identify which growth amplitudes calibration can absorb
Additive PSF leakage | e_obs=e_true+alpha e_PSF | bound a false large-angle filter signal
Shear ratio geometry | R=gamma_t(z_s1)/gamma_t(z_s2) | isolate distance kernels before inferring density response
Weyl versus force split | Sigma=(Phi+Psi)/(2 Phi_N); mu=Phi/Phi_N | state what shear alone cannot identify
Limber remainder | C_ell_exact-C_ell_Limber | bound the projection error at the largest measured angles
Nonlinear cutoff certificate | delta E_n=integral_k>kcut K_n P dk | certify safe measured modes without imported halo physics
Source clustering correction | <(1+delta_s)gamma gamma> | derive the missing three-point term from source selection
Reduced-shear correction | g=gamma/(1-kappa) | propagate measured shape response beyond linear shear
Born-path correction | delta gamma=integral grad_perp Phi delta x dchi | separate ray deflection from altered force kernels
Mask mixing inversion | pseudo C_ell=sum M_ellL C_L | determine recoverable modes for the KiDS footprint
Baryonic redistribution mode | integral delta rho_b dV=0 | distinguish mass-conserving feedback from gravity response
Filter physical versus comoving scale | xi_com=xi_phys/a | derive the redshift signature of the declared heat operator
COSEBI covariance conditioning | C_cond=C_E-C_EB C_B^-1 C_BE | use B modes as a systematic control without double counting
Three-statistic information overlap | rank([J_COSEBI;J_xi;J_band]) | determine which reported summaries add independent constraints
Distance-growth split response | delta C=J_D delta D+J_P delta P | separate geometry from perturbation physics
Finite-field super-sample mode | C_SSC=sigma_b^2 dC/delta_b dC.T/ddelta_b | bound common long-mode uncertainty under the candidate action
Canonical-alternative discriminant | DeltaE=E(a0_alt)-E(a0_can) | derive whether the two fixed normalizations are observationally distinguishable
No-slip null projection | n.T J_nuis=0; t=n.T[d-m_no-slip] | construct a test immune to declared calibration directions
KiDS-450 incremental covariance | L_1000|450=L_joint/L_450 | quantify new-area information with overlapping galaxies removed
''')
seeds('Y2020S03','''
Acoustic angle response | theta_star=r_s(z_star)/D_M(z_star) | map measured acoustic spacing to same-action geometry
TE phase displacement | C_TE approximately A cos(k r_s)sin(k r_s) | constrain a phase change distinct from amplitude calibration
EE diffusion tail | C_EE proportional exp[-2(ell/ell_D)^2] | separate diffusion physics from gravity-driven growth
Temperature lensing smoothing | delta C_TT=sum K_ellL C_L_phiphi | infer Weyl response from peak smoothing without adding a lensing posterior
Frequency coherent CMB mode | d_nu=a_nu s_CMB+f_nu | project frequency-dependent contaminants out of the measured spectrum
Beam width degeneracy | B_ell=exp[-ell(ell+1)sigma_b^2/2] | bound spurious small-scale filter suppression
Polarization angle leakage | E'=E cos2alpha-B sin2alpha | quantify instrumental rotation leakage into acoustic inference
Temperature calibration pivot | C_TT_obs=g_T^2 C_TT | derive the amplitude combination measurable independently of gain
Polarization efficiency pivot | C_TE_obs=g_T g_E C_TE | separate E-mode efficiency from gravitational transfer
Large-scale information dependence | F_joint=F_ACT+F_WMAP-C_overlap | quantify which modes require external large-angle information
Sky-region consistency | DeltaC=C_regionA-C_regionB | test regional systematics with correlated cosmic variance
Baryon loading contrast | R_b=3rho_b/(4rho_gamma) | reconstruct odd-even peak response before using a baryon-density posterior
Early integrated Sachs Wolfe | DeltaT_ISW=integral(Phi'+Psi')deta | isolate evolving metric potentials near recombination
Damping-distance degeneracy | theta_D=r_D/D_M | derive an acoustic-to-damping scale ratio independent of distance
Primordial tilt projection | d ln P_R/d ln k=n_s-1 | distinguish a response tilt from initial-spectrum freedom
Reionization amplitude identity | A_eff=A_s exp(-2tau) | determine the inaccessible amplitude direction without low-ell polarization
Tensor contamination bound | C_EE=C_EE_scalar+C_EE_tensor | bound the tensor contribution using the same two-degree action
Mask-dependent band response | d_b=sum W_bell B_ell^2 C_ell | calculate the exact measured response rather than point-sampling ell
Foreground trispectrum covariance | Cov(C_b,C_b')=Cov_G+T_bb' | assess non-Gaussian residual contamination
ACT-Planck overlap accounting | C_AP=Cov(C_ACT,C_Planck) | quantify common-sky covariance before parameter comparison
Helium-recombination nuisance | ne=ne(Yp,omega_b,z) | isolate atomic-recombination freedom from modified expansion
Drag versus last-scattering ruler | r_d/r_s=integral_zd c_s/H / integral_zstar c_s/H | make the CMB-to-BAO bridge explicit
Heat-filter acoustic response | S(k,a)=exp[-xi^2 k_phys^2/2] | derive whether a static operator extends to photon-era perturbations
High-ell robustness envelope | sup_eta |m(theta,eta)-m(theta,eta0)| | bound calibrated foreground freedom in gravity-sensitive bands
ACT-only scale matching | rho_L=4a0^2/(G_N c^2) | infer the allowed background match without importing Planck H0
''')
seeds('Y2020S04','''
NPIPE dipole calibration transfer | d(t)=g(t)T_dip(t)+s(t) | propagate the measured dipole calibration into large-scale metric inference
Detector-set noise orthogonality | <n_A n_B>=N_AB | test residual correlated noise in cross spectra
NPIPE-minus-legacy sky cancellation | Delta m=m_NPIPE-m_legacy | isolate processing change on the identical sky
Low-ell optical-depth response | C_EE_low approximately tau^2 A_s | measure the reionization amplitude after map-systematics marginalization
Joint LFI-HFI gain degeneracy | d_nu=g_nu sum_c A_nuc s_c | identify absolute versus relative gain directions
Solar dipole spectral consistency | D_nu=D_CMB+sum a_c f_c(nu) | separate frequency-independent dipole from foreground leakage
Polarization zero-level response | Q_obs=Q+q0; U_obs=U+u0 | quantify offsets after masked E-mode projection
Transfer-function calibration | T_ell=<C_out>/C_in | infer simulation-supported attenuation instead of assuming unit response
Simulation covariance precision | Var(Cinv) depends on Nsim and p | bound inversion error for the available end-to-end ensemble
Beam-convolved time-domain closure | d=P B s+n | verify the forward operator used by a gravity spectrum
Bandpass mismatch template | delta d=delta A_dust s_dust | estimate false polarization from unequal frequency response
Destriping long-mode nullspace | d=P m+F a+n | identify gravitational modes confounded with baseline offsets
Mapmaking prior sensitivity | mhat=(P.T Ninv P+R)^-1 P.T Ninv d | derive prior-induced low-ell suppression
Foreground-cleaning transfer | s_clean=w.T d | propagate data-dependent weights into signal covariance
Dipole-to-monopole leakage | delta a_00=M_01 a_1m | bound masking-induced vacuum-background confusion
NPIPE sky-cut stability | Delta tau=tau(mask1)-tau(mask2) | separate measurement stability from independent evidence
Noise anisotropy eigenmodes | N v=lambda v | identify poorly measured large-scale polarization combinations
Calibration-induced TE correlation | delta C_TE=(delta g_T+delta g_E)C_TE | quantify common gain propagation
Frequency jackknife metric test | r_nu=C_nu-C_clean | test whether an apparent slip response is spectrally universal
Legacy common-mode likelihood | L_NPIPE|legacy=L_joint/L_legacy | compute the true information gained by reprocessing
Dipole direction covariance | C_ang=J_cart C_D J_cart.T | propagate vector calibration uncertainty into sky anisotropy
Low-ell non-Gaussian likelihood | L(C_ell|a_lm) | assess failure of Gaussian compressed errors for vacuum matching
Polarization leakage harmonic kernel | E_obs=E+K_TE T | bound temperature contamination in the gravity-sensitive modes
Joint simulation provenance | C_total=C_signal+C_noise+C_cross | avoid counting one simulated sky as independent noise information
Scale-normalization calibration floor | delta a0/a0=0.5 delta rho_L/rho_L | propagate map calibration uncertainty through a derived background map
''')
seeds('Y2020S05','''
O3a tensor speed dispersion | omega^2=c_T^2 k^2+alpha4 k^4 | separate propagation phase from source-phase uncertainty
O3a polarization response rank | d_I=sum_A F_IA h_A | test measured detector rank without treating unmeasured modes as absent
Event-rate selection normalization | L=e^-Nexp product_i integral p(d_i|theta)R(theta)dtheta | derive the catalog likelihood with the actual search threshold
Astrophysical probability mixture | p(d)=p_astro p_sig(d)+(1-p_astro)p_noise(d) | retain uncertain candidates without hard gravitational claims
Waveform-prior removal | L(theta) proportional p_post(theta)/pi_ref(theta) | determine support needed before posterior reweighting
Mass-redshift degeneracy | M_det=(1+z)M_source | separate expansion tests from assumed mass distributions
Luminosity friction integral | dL_GW/dL_EM=exp[0.5 integral alpha_M d ln a^-1] | translate same-action tensor damping into catalog amplitude
Frequency-dependent calibration | h_obs=(1+delta A)e^(i delta phi)h | propagate calibration into common dispersion constraints
Hierarchical dipole-radiation coefficient | delta Psi_i=beta_i f^-7/3 | infer a source-derived common coefficient rather than independent event deformations
Network coherent residual energy | E_res=sum_I <d_I-h_I,d_I-h_I> | bound unexplained strain after calibration projection
Catalog threshold sensitivity | d log L/d rho_threshold | quantify gravity inference changed by the O3a detection cut
Cosmological lensing variance | Var(ln dL)=Var(kappa)+Var_inst | separate line-of-sight metric effects from tensor attenuation
Inclination-distance degeneracy | h_plus proportional (1+cos^2 i)/dL | identify amplitude information available from the network
Spin-precession confusion | h=sum_lm D_lmm'(angles)h_lm' | bound a false propagation signal from unmodeled precession
Inspiral-merger consistency | DeltaM=M_f^insp-M_f^post | derive the common-action matching criterion
Ringdown damping population | tau_lmn^-1=-Im(omega_lmn) | test a shared strong-field relaxation prediction
PSD uncertainty marginalization | p(d|h)=integral p(d|h,S)p(S)dS | obtain robust residual tails without fixed-noise overconfidence
Nonstationarity event weighting | S_n(f,t)=S0(f)+delta S(f,t) | bound time-dependent sensitivity selection
Subthreshold information gain | I=E log[L_all/L_highSNR] | measure the usable contribution of uncertain O3a candidates
Gravitational memory stacking | h_mem proportional integral flux_GW dt/dL | derive a tensor-only nonlinear memory template before stacking
Source acceleration phase | delta Psi proportional a_los f^-13/3 | distinguish environmental acceleration from modified radiation
Common-G strong-field map | G_binary=G_N Z_compact | derive compact-body response before using measured chirp masses
O3a event covariance | C_ij=C_cal_shared+C_individual delta_ij | account for shared detector calibration across events
Dispersive arrival-time moment | Delta t=integral [1/v_g(f,z)-1/c]dl | link phase and group-delay constraints consistently
Novel-candidate increment | L_increment=L_catalog/L_previously_reported | isolate the information first present in the final O3a report
''')
seeds('Y2020S06','''
Short-signal phase identifiability | rank(dh/d[M,q,spin,dispersion]) | establish which gravity parameters a merger-dominated transient can distinguish
Ringdown onset envelope | omega_hat(t0) | bound dependence of inferred damping on the fit start
Coherent burst versus template residual | DeltaE=E_template-E_burst | separate gravity failure from a restricted source model
Quasinormal frequency ratio | R=Re omega_220/Im omega_220 | remove mass scaling from the measured damped waveform
Higher-mode spectral support | h=sum_lm A_lm exp(-i omega_lm t) | determine whether observed frequency content identifies a second mode
Eccentric-merger confounding | dh/de projected orthogonal to dh/dbeta | bound phase deformations absorbed by source eccentricity
Head-on versus orbital morphology | E_cross/E_plus | derive the detector-projected polarization discriminator
Mass-scale vacuum hierarchy | epsilon=a0 G_N M/c^4 | derive a controlled strong-field small-acceleration-scale expansion
Merger duration observable | T90=t95(E)-t5(E) | predict a robust time-domain duration from the candidate action
Peak-frequency mass inference | f_peak M_det=F(q,chi) | identify theory dependence in mass-gap placement
Calibration phase versus damping | delta phi(f)=a+b f+c f^2 | estimate calibration directions degenerate with a short ringdown
Time-frequency ridge curvature | K=d^2f/dt^2 | extract a morphology statistic not fixed by total duration
Detector arrival coherence | Delta t_IJ=(x_I-x_J).n/c_T | derive what the event can say about tensor speed with uncertain sky position
Amplitude-decay ratio | R_A=h(t+Delta)/h(t) | test exponential relaxation independently of absolute distance
Remnant energy balance | E_in-E_rad=M_f c^2 | derive the action-specific radiative bookkeeping
Angular momentum balance | J_in-J_rad=J_f | test the spin inferred from waveform matching
Two-mode resolvability certificate | det F_modes>0 | determine when an overtone claim is identified by data
Start-time look-elsewhere correction | p_global=P(max_t0 T>Tobs) | calibrate ringdown anomaly significance across windows
Wavelet prior sensitivity | h=sum a_n psi_n | quantify burst reconstruction dependence on basis sparsity
Cosmological distance prior effect | p(M_src)=integral p(M_det,dL)p(z|dL)dz | preserve the source-frame mass uncertainty under alternative expansion
Magnification-mass degeneracy | dL_inferred=dL_true/sqrt(mu) | bound interpretation of a heavy merger under line-of-sight lensing
Residual polarization ellipse | epsilon_pol=minor/major | infer only detector-supported polarization combinations
High-frequency tail energy | E_tail=integral_f>fc f^2|h(f)|^2df | distinguish abrupt waveform truncation from physical relaxation
Finite-window Fourier leakage | htilde_W=Wtilde*h | bound false dispersive structure induced by gating
GWTC-2 shared-event exclusion | log L_joint=log L_521+log L_GWTC2_without521 | prevent a single transient from becoming two gravity tests
''')
seeds('Y2020S07','''
Asymmetric multipole ratio | R33=|h33|/|h22| | predict measurable higher-mode strength from action-derived radiation
Mass-ratio phase curvature | d^2Psi/df^2=Q(q,Mc,spin) | isolate asymmetric conservative dynamics
Secondary tidal response | delta Psi_tidal proportional Lambda_tilde f^5/3 | bound matter effects without asserting compact-object identity
Black-hole quadrupole relation | Q=-kappa_spin chi^2 M^3 | derive the spin-induced quadrupole to waveform bridge
Small-body self-force scaling | a=a0_GR+q a1+q^2 a2 | identify controlled asymmetric-mass expansion terms
Inclination from mode beating | h33/h22 projected through F_I | reduce amplitude-distance degeneracy using actual harmonic content
Spin-mass covariance direction | v_min=eigenvector_min(F_mass,spin) | find the gravity coefficient hidden by parameter covariance
Asymmetry-dependent dipole bound | F_dip proportional (s1-s2)^2 | derive compact-body sensitivities before using a dipole template
Inspiral energy flux balance | df/dt=-F_GW/(dE/df) | separate conservative and radiative modifications
Tidal disruption visibility | f_disrupt/f_ISCO | derive whether absence of a cutoff constrains matter coupling
Higher-mode calibration mimic | delta A(f) projected on dh33/dA33 | bound instrumental confusion with multipolar radiation
Precession null estimator | h_odd under orbital-plane reflection | test precession contamination of a polarization claim
Merger recoil momentum | P_rad=integral n dE/dOmega | predict an asymmetric remnant kick from the same tensor stress
Source-frame mass boundary | m2_src=m2_det/(1+z) | quantify dependence of compact-object classification on cosmology
Phase-order consistency | beta_n=fitted deformation at PN order n | test linked rather than independently adjustable action coefficients
Finite-size positivity bound | Lambda>=0 under stated passive matter assumptions | determine whether inferred tidal support obeys the assumed material class
Secondary spin upper envelope | chi2<=chi_max(EOS,theory) | separate a matter prior from a gravity result
Mode-frequency consistency | f33/f22 approximately 3/2 in inspiral | use measured harmonic locking as a source-model check
Radiated-energy fraction | epsilon_rad=E_rad/(M1+M2)c^2 | derive allowed range from candidate energy conservation
Posterior support loss | ESS=(sum w)^2/sum w^2 | certify whether GR posterior reweighting reaches the candidate theory
Sky-polarization degeneracy | det(F.T Ninv F) | bound network sensitivity at this event's sky location
Low-frequency environmental drift | DeltaPsi_env proportional f^-13/3 | separate long inspiral acceleration from tensor dispersion
Cutoff-frequency robustness | beta_hat(fmin,fmax) | isolate bands carrying an apparent departure
Extreme-ratio extrapolation error | R(q)=h_exact-h_asymptotic | bound model error before assigning a modified-gravity residual
O3a double-count exclusion | L_joint=L_814 L_catalog_without814 | keep this event's multipole information from duplicated population evidence
''')
seeds('Y2020S08','''
Mass-sheet Hubble degeneracy | kappa_lambda=lambda kappa+1-lambda; Delta t_lambda=lambda Delta t | derive the exact transformation in the candidate lens map
Kinematic mass-sheet breaking | sigma_los^2=integral K_beta(r)nu_star(r)g(r)dr | quantify which stellar data remove the lensing degeneracy
Anisotropy-distance covariance | beta_ani=1-sigma_t^2/(2sigma_r^2) | isolate orbital anisotropy from time-delay distance
Aperture convolution transport | sigma_ap^2=integral PSF I sigma_los^2/integral PSF I | derive the measured dynamical estimator
Time-delay Fermat closure | Delta t=D_dt Delta phi/c | recompute both geometry and projected potential for one action
Slip-sensitive dynamics ratio | R=mass_lens/mass_dyn | replace imported mass estimates with photon and stellar forward maps
External convergence uncertainty | D_dt_true=(1-kappa_ext)D_dt_model | propagate environment into the vacuum-scale inference
Hierarchical profile exchangeability | p(lambda_i|hyper) | test whether non-time-delay lenses can share the population prior
Lens selection reweighting | p(theta|selected) proportional S(theta)p(theta) | bound selection transfer between lens samples
Power-law curvature residual | d^2 ln rho/d(ln r)^2 | recover profile information suppressed by a single slope
Source-position transformation | beta'=f(beta) | classify image-preserving degeneracies beyond a mass sheet
Time-delay covariance rank | C_dt singular along common time origin | remove unobservable timing offsets
Microlensing delay bias | Delta t_obs=Delta t_geom+Delta t_micro | bound accretion-disk contamination before cosmography
Spatially varying stellar M/L | rho_star=Upsilon(r)I(r) | test baryonic-source uncertainty in filtered MONO
Heat-filter lens-plane reduction | psi(theta)=integral(Phi+Psi)dl/c^2 | determine whether projection commutes with the declared filter
Finite lens boundary contribution | psi=psi_local+psi_boundary | quantify a nonlocal environmental term
Image parity certificate | sign det(I-Hess psi) | test predicted caustic structure independent of H0
Radial magnification ratio | mu_r^-1=1-dalpha/dtheta | infer local derivative constraints on the lens potential
Tangential critical curve closure | alpha(theta_E)=theta_E | compare the critical radius with action-derived baryonic response
Velocity aperture scale lever | d ln sigma_ap/d ln R_ap | propose a measured radial lever on internal mass-sheet freedom
Seven-lens covariance decomposition | C=C_cal+C_population+C_individual | prevent common calibration from shrinking with lens count
Canonical alternative distance split | D_dt(a0_alt)-D_dt(a0_can) | quantify scale-footing distinguishability with fixed baryons
Lens cosmology factorization | D_dt=(1+zd)Dd Ds/Dds | derive distance ratios without inserting a LCDM prior
Hierarchical prior volume audit | log Z=log integral L pi dtheta | distinguish measurement likelihood from population-prior narrowing
H0LiCOW information increment | L_TDCOSMO|H0LiCOW | retain flexible-profile information without multiplying reused delays
''')
seeds('Y2020S09','''
Parallax zero-point force bias | r=1/(varpi-zp); g=v_t^2/r | propagate correlated distance bias into acceleration
Proper-motion frame spin | mu_obs=mu_true+omega cross n | isolate reference-frame rotation from Galactic streaming
Tangential velocity covariance | C_v=J C_ast J.T | carry position-parallax-motion cross terms into dynamics
Perspective acceleration | dot mu=-2(v_r/r)mu | subtract kinematic acceleration before testing gravity
Wide-pair common parallax mode | Delta varpi=varpi1-varpi2 | distinguish pair precision from an absolute distance constraint
Cluster expansion contamination | v_r_cluster=H_cluster r | separate non-equilibrium expansion from force inference
Solar reflex field | mu_reflex=-v_sun_perp/r | derive the frame correction before identifying acceleration anisotropy
Astrometric selection likelihood | p(d|S)=p(d)S(d)/P(S) | avoid quality-cut induced velocity tails
Unresolved photocenter orbit | x_ph=(L2 M1-L1 M2)x_rel/[(L1+L2)(M1+M2)] | quantify false low-acceleration excess
Five-parameter fit absorption | a_res=(I-P_design)a_true | determine which physical accelerations are removed by catalog fitting
Gaia-DR2 update covariance | C_Delta=C_EDR3+C_DR2-2C_cross | isolate the information added by EDR3
Photometric mass calibration | M_star=f(G,color,age,Z) | propagate stellar-model uncertainty into the MONO source
Distance-prior dependence | p(r|varpi) proportional L(varpi|r)pi(r) | bound inferred gravity changes from parallax inversion priors
Angular separation projection | r_perp=r theta | derive wide-pair geometry with common distance covariance
Galactic tidal tensor | T_ij=partial_i partial_j Phi | map proper-motion gradients to environmental tides
Vertical Jeans boundary term | d(nu sigma_z^2)/dz+nu dPhi/dz+R^-1 d(Rnu sigma_Rz)/dR=0 | quantify tilt contamination in vertical force
Radial Jeans streaming term | v_c^2=mean(vphi)^2+sigma_phi²-sigma_R²[1+dln(nu sigma_R²)/dlnR]-(R/nu)partial_z(nu sigma_Rz) | preserve pressure support before MONO comparison
Moving-group contamination | p(v)=f_bound p_b+(1-f_bound)p_stream | identify nonbound kinematic pairs
Spatial covariance floor | Cov(mu_i,mu_j)=K(theta_ij) | determine the force precision floor for dense tracers
Reference-frame acceleration dipole | mu_dip=(a_sun-(a_sun.n)n)/c | connect secular aberration to physical Galactic acceleration
Color-dependent astrometric bias | zp=zp(G,color,ecliptic_latitude) | bound a false mass-dependent force law
High-proper-motion completeness | N_obs=S(mu,G)N_true | derive selection correction for extreme trajectories
Action-angle equilibrium check | df(J)/dt=0 | test whether a chosen tracer population supports steady dynamics
Heat-filter resolution bound | xi/r_res | identify unresolved response scales in angular astrometry
Carried radial-velocity exclusion | I_new(v_r)=0 for unchanged DR2 rows | keep legacy velocities from appearing as new EDR3 gravity evidence
''')
seeds('Y2020S10','''
External-field vector response | g_int=F[rho_b,g_ext vector,xi] | replace a scalar external-field substitution by the boundary problem
Environment permutation statistic | T=sum residual_i gext_i | calibrate the measured environment association
Isolated-galaxy boundary limit | lim_gext->0 g_int | derive continuity into the isolated sample
Strong-field outer-curve suppression | Delta v2=R[g_with_ext-g_isolated] | predict the radius-dependent measured suppression
Tidal versus uniform field separation | g_ext(x)=g0+T x | distinguish external acceleration from tidal distortion
External-direction quadrupole | g_R(R,phi)=g0(R)+g2(R)cos2phi | derive an observable anisotropy absent in scalar fits
Filter-domain environment leakage | delta Phi/d rho_outside | quantify sensitivity to unobserved external mass
Distance-environment covariance | Cov(D,gext) | prevent a common distance calibration from generating an EFE trend
Inclination-environment confounding | v_true=v_los/sin i | bound a false environment dependence from inclination priors
Stellar mass-to-light cross bias | d residual/dUpsilon | separate baryonic normalization from boundary response
Gas-dominated control prediction | g_bar approximately g_gas | isolate systems with reduced stellar-population dependence
Environmental mass completeness | g_missing=G integral_missing rho rhat/r2 dV | bound unobserved catalog contributions
Uniform acceleration covariance | Phi->Phi-a_ext.x | derive which response survives a freely falling coordinate change
Source gate environmental activation | f_gate=f(|grad Su|/a0) | test whether environment changes the actual occupied branch
Weak-field derivative response | chi_ext=partial g_int/partial gext | distinguish monotone response from a fitted kernel imitation
External-field time dependence | tau_relax dot q+q=q_eq(gext(t)) | bound equilibrium assumptions for evolving environments
Outer-curve residual correlation | C_RR'=Cov(delta v(R),delta v(R')) | avoid counting rotation-curve radii as independent galaxies
Environment rank likelihood | p(rank residual|rank gext) | test an association less sensitive to absolute environment calibration
Low-acceleration floor | g_int~G_eff(gext)M/R2 in external-dominated limit | derive the permitted asymptotic behavior of filtered MONO
Baryonic surface-density matching | residual perpendicular to Sigma_b,D,i | separate environmental evidence from galaxy structural selection
Tidal truncation radius | g_int(r_t)=lambda_tide r_t | derive the domain where equilibrium EFE fitting ceases to apply
Canonical alternative EFE contrast | Delta_chi=chi_ext(a0_alt)-chi_ext(a0_can) | test normalization with the same environment inputs
Golden-galaxy selection correction | p(T|max selection) | quantify selection significance of exceptional systems
SPARC catalog reuse ledger | C_joint has shared rotation-curve blocks | isolate environment information from earlier SPARC force-law tests
No-slip environmental lensing bridge | Delta alpha=integral grad_perp(DeltaPhi+DeltaPsi)dl/c2 | derive a distinct lensing consequence of a surviving kinematic environment signal
''')
source(2021,1,'DES Y3 3x2pt','2105.13549','2021-05-28','Dark Energy Survey Year 3 Results: Cosmological Constraints from Galaxy Clustering and Weak Lensing','DES Collaboration; T. M. C. Abbott et al.','Joint measured shear, lens-galaxy clustering and galaxy-shear correlations.','DES first three observing years; exact exposure epochs uninspected','DES_imaging','Derive galaxy motion and both metric potentials from one action before the three projections; gates 1,3,5,8.','DES Y3 three-correlation vector, lens/source redshift kernels, masks, biases and joint covariance.','rotate source shapes while preserving lens positions','compare separate tracer and source selections with a shared-sky covariance','2021 joint correlations add observed galaxy-shear consistency beyond a generic shear-amplitude task')
source(2021,2,'AGC 114905 HI','2112.00017','2021-11-30','No need for dark matter: resolved kinematics of the ultra-diffuse galaxy AGC 114905','P. E. Mancera Pina et al.','Higher-resolution HI cube and resolved gas-disk rotation, with independently estimated inclination.','New interferometric observations; exact epochs uninspected','AGC114905_HI','Derive a three-dimensional filtered MONO gas-disk solution and its spectral projection; gates 1,5,9,10,13.','HI cube, channel response, beam, photometric inclination and gas surface density; cube availability not yet checked.','inject a face-on disk and deliberately hold its inclination fixed incorrectly','compare full-cube fits with independently extracted velocity moments','New 2021 resolution and inclination information make this an object-specific force and geometry test, not a renamed BTFR fit')
source(2021,3,'GWTC-3 O3b','2111.03606','2021-11-05','GWTC-3: Compact Binary Coalescences Observed by LIGO and Virgo During the Second Part of the Third Observing Run','LIGO Scientific Collaboration, Virgo Collaboration and KAGRA Collaboration','O3b compact-binary detections, including newly catalogued candidates.','2019-11-01 to 2020-03-27; some earlier low-latency alerts','LVK_O3b','Derive binary dynamics, tensor radiation and propagation under the same healthy action; gates 2,6,7,10.','O3b strain likelihoods, PSD/calibration and search efficiencies; source posteriors retain reference-waveform assumptions.','assign random coalescence times to cross-detector data','validate an O3b-only GR reference before any combined-run result','2021 catalog adds O3b measurements; tasks restrict evidence to new epochs or explicit O3a-to-O3b contrasts')
source(2021,4,'GWTC-2.1 reanalysis','2108.01045','2021-08-02','GWTC-2.1: Deep Extended Catalog of Compact Binary Coalescences Observed by LIGO and Virgo During the First Half of the Third Observing Run','LIGO Scientific Collaboration and Virgo Collaboration','Deeper O3a event search using final calibrated strain and improved noise subtraction.','Same 2019-04-01 to 2019-10-01 strain as GWTC-2; processing increment','LVK_O3a','Derive the strain map and detection operator before interpreting changed event support; gates 2,6,7,10.','Final O3a calibrated strain, candidate probabilities, threshold changes and old/new processing covariance.','treat old and reprocessed strain as independent copies and demonstrate overconfidence','compare candidate recovery with an injection set under both processing versions','2021 recalibration and deeper candidate list provide new processing information, not a second observation of old events')
source(2021,5,'SPT-3G EE TE','2101.01684','2021-01-05','Measurements of the E-Mode Polarization and Temperature-E-Mode Correlation of the CMB from SPT-3G 2018 Data','D. Dutcher et al.','Multifrequency EE and TE angular power spectra.','Four months in 2018','SPT3G_2018_CMB','Derive polarization generation and photon-metric transfer before applying the survey windows; gates 5,8,13.','SPT-3G EE/TE frequency cross spectra, band windows, beam/polarization calibration and covariance.','flip only one frequency-pair TE spectrum','recover agreement between independent frequency combinations under a GR reference','First 2021 polarization report adds measured acoustic and calibration modes beyond prior SPTpol data')
source(2021,6,'SH0ES Cepheid ladder','2112.04510','2021-12-08','A Comprehensive Measurement of the Local Value of the Hubble Constant with 1 km/s/Mpc Uncertainty from the Hubble Space Telescope and the SH0ES Team','A. G. Riess et al.','Cepheid photometry in SN hosts and geometric-anchor distance-ladder inference.','HST observations compiled across decades; new enlarged 2021 host report','SH0ES_Pantheon_distance_ladder','Derive cosmological luminosity distance and any gravity dependence of stellar pulsation; gates 5,8,10,13.','Cepheid periods and multiband photometry, anchor distances, SN calibration and covariance; published H0 is a derived result.','shuffle host identities between Cepheids and supernovae','fit geometric anchors separately before a joint ladder','2021 enlarged matched-instrument host sample supplies new calibration geometry beyond an abstract Hubble-tension task')
source(2021,7,'Double pulsar timing','2112.06795','2021-12-13','Strong-field Gravity Tests with the Double Pulsar','M. Kramer et al.','Long-baseline relativistic orbital timing and light-propagation measurements.','16-year timing span','PSRJ0737_double_pulsar','Derive compact-body motion, null delays and tensor energy loss from one action; gates 4,5,6,10,11.','Pulse timing data or full timing-parameter covariance, astrometry, dispersion and orbital nuisance terms; raw TOA availability unverified.','omit the kinematic contribution to orbital-period decay','use independently measured timing effects to overdetermine the same masses','2021 long-baseline timing resolves corrections absent from a generic binary energy-loss seed')
source(2021,8,'EDR3 resolved binaries','2101.05282','2021-01-13','A million binaries from Gaia eDR3: sample selection and validation of Gaia parallax uncertainties','K. El-Badry, H.-W. Rix and T. M. Heintz','Resolved binary catalog with empirical chance-alignment probabilities and parallax-error calibration.','Gaia EDR3 observations; new pair identification and validation in 2021','Gaia_stellar_astrometry','Derive filtered MONO relative motion with the Galactic boundary field, then catalog selection; gates 1,4,9,10.','Pair astrometry, magnitude/color, chance-alignment scores and full covariance; linked catalog exists but files not inspected.','construct shifted-sky false pairs with the same selection','validate parallax-difference widths on high-confidence close pairs','2021 pair membership and error inflation add new measurement structure beyond reusing the 2020 single-star catalog')
source(2021,9,'Pantheon+ light curves','2112.03863','2021-12-07','The Pantheon+ Analysis: The Full Dataset and Light-Curve Release','D. Scolnic et al.','Compiled SN Ia light curves, repeated survey measurements and sibling supernova comparisons.','Multiple surveys and epochs; exact dates require light-curve metadata','SH0ES_Pantheon_distance_ladder','Derive luminosity distance and photon transport while retaining empirical standardization nuisance parameters; gates 5,8,11,13.','Multisurvey flux light curves, observation times, redshifts, host associations and calibration covariance.','randomize repeat-observation survey labels','compare sibling-supernova differences that cancel host distance','2021 full light-curve release supplies duplicate and sibling controls; 2022 distance-inference paper is not an independent SN sample')
source(2021,10,'M87 ring polarization','2105.01169','2021-03-24','First M87 Event Horizon Telescope Results. VII. Polarization of the Ring','Event Horizon Telescope Collaboration','Linear-polarimetric horizon-scale images and temporal changes of M87 emission.','2017 April, same campaign as earlier total-intensity imaging','EHT_M87_2017','Derive null transport and polarization propagation in the candidate metric plus explicit plasma emission; gates 3,10,11.','Polarimetric visibilities or calibrated image summaries, station gains/leakages and scattering assumptions; full products not inspected.','scramble cross-hand phases while retaining total intensity','compare independent polarimetric imaging reconstructions with common visibility covariance','2021 first polarization measurement adds Stokes information to 2017 intensity data; it is not a new intensity campaign')
S['Y2021S10']['date_basis']='Opened arXiv primary report comments explicitly state publication in ApJL on March 24, 2021; May 3 arXiv deposit is later and is not used as first report date.'
seeds('Y2021S01','''
Three-probe slip closure | E_G=C_gkappa/(beta C_gg) | derive lensing-growth ratio with consistent windows
Lens-source stochasticity | r_gm=P_gm/sqrt(P_gg P_mm) | measure decorrelation before interpreting modified gravity
Galaxy-bias self-calibration | C_gkappa^2/C_gg | isolate lensing amplitude without a fixed linear bias
Source redshift cross-leakage | C_ij=sum_ab M_ia M_jb C_ab | derive mixing from source-bin migration
Lens magnification contamination | delta_g_obs=delta_g+(5s-2)kappa | separate magnification from clustering response
Shear-ratio nuisance projection | gamma_t(l,s1)/gamma_t(l,s2) | isolate geometry across source bins
Lens-sample unblinding change | Delta d=d_final-d_initial | quantify sensitivity to the documented lens-selection change
Three-probe covariance Schur test | C_shear|gg=C_ss-C_sg C_gg^-1 C_gs | identify independent shear information
Scale-cut information loss | F_cut=J_cut.T C_cut^-1 J_cut | determine which action coefficients are actually constrained
Nonlinear galaxy bias curvature | delta_g=b1 delta+b2 delta^2/2 | bound false scale-dependent gravity
Satellite occupation nuisance | P_1h depends on <N_c N_s> | separate galaxy occupation from metric response
Tidal alignment cross term | P_gI=b_g A_I P_delta_s | derive its distinct redshift and angular signature
Baryon compensation test | integral r2 delta rho_b dr=0 | constrain feedback that conserves the measured baryonic source
Lens photometric-redshift dilation | delta z_l -> delta D_l,delta W_l | separate lens geometry error from force suppression
Source-lens clustering boost | gamma_obs=B(theta)gamma_true | derive boost correction in the actual pair estimator
Survey mean-density response | delta_g=ng/nbar-1 | bound integral-constraint removal of low-k response
Reduced-shear 3x2 correction | C_ggamma receives <delta_g gamma kappa> | calculate the missing bispectrum term
Tomographic consistency eigenmode | C^-1/2 r=lambda v | localize a discrepancy to measured combinations
Common-potential growth-lensing map | Phi=Psi implies Sigma=mu under stated normalization | test the equality before data projection
Heat-filter galaxy cross window | C_gkappa=integral Wg Wk P_filtered/chi2 | identify angular filter response unique to cross correlations
DES-KiDS sky overlap | Cov_DES,KiDS from common modes | prevent two surveys' shared modes from false precision
Geometry-only null statistic | n.T J_growth=0 | construct a distance-kernel consistency test
Growth-only null statistic | n.T J_distance=0 | identify perturbation information insensitive to expansion shifts
Canonical versus alternative joint fit | Delta chi2=chi2_can-chi2_alt | compare fixed scale footings in the same nuisance cell
Year-1 to Year-3 increment | L_Y3|Y1=L_joint/L_Y1 | isolate new-area and improved-calibration evidence
''')
seeds('Y2021S02','''
Inclination-force degeneracy | v_c=v_los/sin i | infer the inclination needed by each fixed acceleration footing
Three-dimensional HI cube map | I(x,y,v)=integral rho_HI phi[v-vlos]dl | predict observed channels directly from the force solution
Beam-smeared rotation curvature | v_obs=(B*(I v))/(B*I) | quantify unresolved gradients in the new beam
Gas pressure correction | v_c^2=v_rot^2-R/rho dP/dR | derive turbulent support with radial density structure
Finite-thickness baryonic force | g_R=G integral rho(R,z)K_R dV | avoid a razor-thin disk substitution
Disk ellipticity inclination bias | q_obs^2=cos(i)^2+q0^2 sin(i)^2 | bound geometry inferred from a noncircular disk
Warp versus force residual | i=i(R); PA=PA(R) | distinguish changing orientation from radial response
Asymmetric drift anisotropy | P_RR != P_phiphi | derive the gas-moment correction without isotropy
MONO filter scale in a diffuse disk | S rho=exp(xi2 Delta/2)rho | determine suppression relative to the measured gas scale length
Distance-dependent baryonic acceleration | M_gas proportional D2; R proportional D | derive which disk-force combinations are distance invariant
HI opacity correction | N_HI proportional integral T_s tau dv | bound hidden gas mass from optically thin assumptions
Stellar light contribution | g_bar=g_gas+Upsilon g_star | isolate the small but uncertain stellar force
Approaching-receding split | Delta v(R)=v_app-v_rec | bound nonaxisymmetric disturbance
Radial gas-flow harmonic | vlos=sin i[v_phi cosphi+v_R sinphi] | identify inflow mistaken for circular support
Channel covariance rank | C_vv'=Cov(n_v,n_v') | avoid overcounting correlated spectral channels
External-field minimum | min_gext chi2[v_MONO(gext)] | determine required environment without fitting an arbitrary halo
Disk stability consistency | Q_g=kappa sigma/(pi G_eff Sigma_g) | test whether the fitted gas disk can persist dynamically
Vertical hydrostatic scale | dP/dz=-rho dPhi/dz | connect thickness and radial gravity from the same potential
Edge truncation filter artifact | delta g_R from rho(R>Rmax) | bound finite-map boundary uncertainty
BTFR residual from cube | Delta=4ln vflat-ln(G_N M_b a0) | infer a likelihood for the actual asymptotic diagnostic
Photometric kinematic inclination agreement | Delta i=i_photo-i_cube | measure internal geometry consistency
Noncircular m2 response | v_R,v_phi include sin2phi,cos2phi | quantify bar-like harmonics under the observed beam
Gas-mass radial covariance | C_Sigma(R,R') | propagate flux calibration jointly across rings
Old-new resolution increment | Delta cube=B_old*cube_new-cube_old | separate new spatial information from repeat photons
Filter-free high-acceleration anchor | lim_y>>1 g/g_N=1 | calibrate the force solver before this diffuse low-acceleration application
''')
seeds('Y2021S03','''
O3b-only damping evolution | dL_GW/dL_EM=Xi0+(1-Xi0)/(1+z)^n | infer an incremental redshift-dependent amplitude constraint
O3b neutron-star black-hole asymmetry | beta_dip proportional (sNS-sBH)^2 | derive the matter sensitivity needed by the new class of binaries
Run-dependent calibration comparison | Delta beta=beta_O3b-beta_O3a | distinguish detector evolution from propagation physics
O3b mass-population selection | Nexp=integral R(m,z)S_O3b(m,z)dmdz | derive gravity-dependent sensitive volume
New-candidate coherence | log B_coh=log Z_network-sum log Z_single | authenticate a signal before assigning a gravity residual
O3b phase-velocity moment | delta Psi=integral delta k(f,z)dl | map the new distance reach into dispersion leverage
Population tensor-energy positivity | E_T=Q_T hdot^2/2 with Q_T>0 | translate a candidate kinetic normalization into source amplitudes
Asymmetric-source mode diversity | rank(sum F_event) | measure added waveform directions beyond O3a
Luminosity-distance selection Jacobian | p_det(dL) proportional dV/dz dz/ddL | recalculate catalog selection under the candidate cosmology
O3b spin-orbit radiation link | beta_SO linked to conservative spin coupling | test action-correlated waveform coefficients
Tidal non-detection support | L(Lambda_tilde) | quantify which matter responses remain unmeasured
Neutron-star cutoff selection | Pdet depends on f_disrupt | avoid importing a black-hole selection function
O3b noise-origin mixture | p(d)=lambda_s p_s+lambda_n p_n | retain marginal triggers with calibrated uncertainty
O3b polarization geometry gain | det(F_new.T Ninv F_new) | isolate the network response gained by new sky directions
New-run memory accumulation | SNR_mem^2=sum h_mem.T C^-1 h_mem | derive the coherent information from O3b only
O3b lensing outlier influence | dL_obs=dL/sqrt(mu) | bound a single magnified source's effect on attenuation inference
Source cosmological acceleration | zdot=(1+z)H0-H(z) | estimate its waveform phase separately from local acceleration
Common-source energy closure | E_orbit+E_tensor+E_aux conserved | derive a missing-channel diagnostic without adding gravitational polarizations
O3b redshift-mass prior robustness | p(m_src|z) versus p(m_src) | separate evolution assumptions from gravity
Run-conditional Bayes factor | B=Z_O3b|O3a_candidate/Z_O3b|O3a_GR | prevent training and testing on the same old events
Catalog event reclassification | Delta p_astro under changed waveform support | quantify selection feedback from candidate dynamics
O3b detector duty-cycle response | S=integral duty(t)Pdet(theta,t)dt | derive exposure weighting for propagation tests
Subdominant mode phase locking | Psi_lm=(m/2)Psi22+delta_lm | test a linked harmonic prediction
O3b high-frequency residual moment | R_hf=integral_fcut^fmax |d-h|2/S df | isolate late-time strong-field mismatch
Full-catalog overlap subtraction | log L_new=log L_GWTC3-log L_shared_O1O2O3a | certify that the reported increment uses only new information
''')
seeds('Y2021S04','''
Calibration-update waveform displacement | Delta h=(R_final/R_old-1)d_old | measure the change in strain space before parameter comparison
Noise-subtraction signal transfer | d_clean=d-W witness | bound subtraction of physical gravitational signal
Deeper-threshold population normalization | Nexp(rho_min)=integral S_rhomin R dtheta | account for the altered candidate threshold
New-candidate incremental posterior | p(theta|new,old) proportional L_new p(theta|old) | isolate newly supported source information
Reprocessed-event covariance | Cov(theta_old,theta_new) | prevent repeat strain from becoming independent evidence
Probability-threshold discontinuity | dE[beta]/dp_astro_cut | measure sensitivity to hard event inclusion
Final-calibration phase eigenmodes | delta phi=sum a_n e_n(f) | project calibration updates onto propagation coefficients
Search-pipeline union probability | P(A union B)=P(A)+P(B)-P(A intersect B) | normalize multiple-pipeline selection
Subtraction-witness coherence | gamma2=|S_dw|2/(S_dd S_ww) | distinguish environmental noise from a physical transient
Astrophysical versus glitch Bayes map | p_astro=R_s L_s/(R_s L_s+R_n L_n) | derive the prior-rate sensitivity of uncertain events
Old-new mass-shift significance | T=Delta m.T C_Delta^-1 Delta m | test whether parameter changes exceed common-data noise
Shared-PSD update likelihood | L_final/L_old with correlated PSD estimates | identify actual noise-model information gained
Candidate false-alarm tail extrapolation | FAR(rho)=N_bg(>rho)/T_bg | quantify rare-event tail uncertainty
New asymmetric-binary leverage | dPsi/dq evaluated on newly found events | identify added mass-ratio sensitivity without recycled events
New positive-spin leverage | dPsi/dchi_eff | test whether deeper search changes a common radiation coefficient
High-mass search support | Pdet(M,chi,beta) | quantify selection near short-duration waveform boundaries
Detection-statistic gravity derivative | d rho_matched/d beta | recompute search response under candidate waveform mismatch
Reprocessing residual spectrum | Delta P=|d_final|2-|d_old|2 | localize changed frequency bands
Catalog prior-change separation | Delta log posterior=Delta log L+Delta log prior | distinguish data updates from inference convention
Threshold-crossing stability | P(event remains selected|calibration) | propagate calibration into catalog membership
Two-stage selection correction | p(d|search,followup)=p(d)S_search S_followup/Z | retain parameter-estimation follow-up selection
Marginal trigger stacking | sum p_astro_i score_i | derive a calibrated weak-event gravity score
Independent off-source validation | distribution T_offsource | test whether subtraction changes residual tails
GWTC-2 to 2.1 likelihood ratio | Lambda_update=L_finalstrain/L_oldstrain | report an update diagnostic without claiming independent sample size
O3a final-to-O3b bridge | shared hyperprior learned from final O3a | define a prospective O3b test that avoids tuning twice
''')
seeds('Y2021S05','''
Polarization acoustic-spacing estimator | Delta ell_EE approximately pi D_M/r_s | derive a peak-spacing likelihood without LCDM compression
TE zero-crossing response | C_TE(ell_zero)=0 | isolate phase information insensitive to overall calibration
EE-to-TE amplitude ratio | R=C_TE^2/C_EE | separate temperature transfer from polarization efficiency
Frequency-pair covariance modes | C_pairs v=lambda v | identify independent CMB combinations in the six estimates
Polarization beam mismatch | Delta B_ell=B_ell_E-B_ell_T | quantify a false phase-amplitude consistency violation
SPTpol incremental sky information | C_new|old=C_new-C_cross C_old^-1 C_cross.T | avoid counting overlapping polarization maps twice
Recombination width signature | E proportional integral visibility quadrupole deta | constrain time-width effects distinct from expansion distance
Photon velocity versus density phase | Theta0 proportional cos(kr_s); v_gamma proportional sin(kr_s) | test linked TE and EE acoustic solutions
Polarization lensing remapping | E_lensed(n)=E(n+grad phi) | derive the same-action remapping correction
Dust polarization spectral law | P_dust(nu)=A nu^beta Bnu(T) | project a foreground spectrum out of measured EE
Polarized point-source tail | C_ell_ps=constant | bound the high-ell contaminant to filter constraints
Atmospheric noise cross spectrum | N_AB(fscan) | derive residual covariance between observing subsets
Calibration-angle TE attenuation | C_TE_obs=cos(2alpha)C_TE | quantify a gravity-amplitude mimic
Frequency decorrelation of dust | C_dust(nu1,nu2)=r_dust sqrt(C11 C22) | test the assumption of perfect foreground coherence
Effective multipole-center bias | C_b-integral W_b C_ell dell | bound plotting-center approximations in likelihood construction
Low-ell cut response | DeltaF=F_ellmin1-F_ellmin2 | locate sensitivity to excluded large scales
Damping-tail baryon response | d ln C_EE/d omega_b | separate density from gravitational-transfer changes
Primordial running degeneracy | ln P_R=ln A_s+(n_s-1)lnk+alpha_s lnk2/2 | quantify initial-spectrum absorption of filtered response
Polarization-only vacuum matching | rho_L[H(z),G_cosmo] | derive a conditional acceleration-scale constraint with fixed stellar-independent inputs
Lensing-amplitude consistency | A_L_EE-A_L_TE | measure whether one Weyl prediction fits both spectra
Sky-mask E-to-B leakage | B_obs=M_BE E | bound an instrumental parity signature
Cross-frequency gain closure | g_95 g_150 g_220 ratios | solve relative gain using redundant frequency triangles
Common-sky Planck comparison | Delta C=C_SPT-W C_Planck | cancel cosmic variance where masks overlap
Filter redshift-integral support | K_xi(z)=partial C_EE/partial xi(z) | identify epochs to which measured polarization is sensitive
Future TT conditional prediction | p(C_TT|C_TE,C_EE) | provide a falsifiable withheld-observable bridge to the later temperature release
''')
seeds('Y2021S06','''
Cepheid pulsation-gravity response | P proportional (G_eff rho_star)^-1/2 | derive the stellar-structure premise before using a modified distance ladder
Geometric-anchor consistency | Delta mu_ab=mu_anchor_a-mu_anchor_b | infer independent anchor tensions with common photometric covariance
Wesenheit extinction degeneracy | W_H=m_H-R(m_V-m_I) | separate reddening law from gravitational luminosity change
Period-luminosity slope curvature | M=a+b logP+c(logP)^2 | quantify nonlinear period calibration in the enlarged host sample
Metallicity-distance covariance | M=M0+b logP+gamma Z | isolate metallicity leverage across anchors and hosts
Host crowding response | m_obs=m_true-2.5log(1+F_blend/F_star) | derive a flux-level bias model
Same-instrument zero-point cancellation | Delta m=m_host-m_anchor | establish which WFC3 calibration terms cancel
SN absolute-magnitude transfer | M_B=m_B-mu_Cepheid | propagate host-distance covariance into calibrator luminosity
Hubble intercept reconstruction | logH0=(M_B+5a_B+25)/5 | derive the ladder map without importing a posterior
Peculiar-velocity ladder floor | cz_obs=H0 d+v_pec | quantify low-redshift flow uncertainty shared across hosts
Anchor leave-one-out prediction | p(mu_a|other anchors) | test geometric calibration without refitting on the withheld anchor
Period-distribution mismatch | Delta M=b[mean logP_host-mean logP_anchor] | bound extrapolation from anchor to host populations
Selection-truncated Cepheid likelihood | p(m|m<m_lim)=p(m)/P(m<m_lim) | correct faint-end distance bias
Binary-Cepheid contamination | F_total=F_Cepheid+F_companion | constrain luminosity contamination rather than fit a gravity offset
Parallax zero-point transfer | varpi_obs=10^[-(mu+5)/5]+zp | retain Gaia common error in the stellar anchor
Maser-anchor coupling distinction | D_maser depends on G_dyn M | derive how the geometric maser distance changes under candidate dynamics
Eclipsing-binary anchor response | F_surface(T,Z), R_orbit | separate stellar-atmosphere and orbital-gravity inputs
Host shared-distance covariance | Cov(M_Bi,M_Bj)=Cov(mu_i,mu_j) | preserve common anchors across supernova calibrators
Photometric count-to-flux nonlinearity | F_cal=F_raw[1+epsilon log F_raw] | bound an instrument bias that mimics distance dependence
Cepheid environment test | Delta M(E)=M_highE-M_lowE | derive any MONO stellar-response effect before environmental regression
Ladder expansion-shape correction | dL=cz/H0[1+(1-q0)z/2+...] | measure dependence on finite-redshift cosmography
Canonical versus alternative stellar map | Delta P=P(a0_alt)-P(a0_can) | determine whether fixed scale choices affect the calibration stars
Host selection dependence | p(host|SN suitability,Cepheid visibility) | quantify calibration-sample transport to Hubble-flow SNe
Shared Pantheon covariance | C_ladder,SN from common light curves | prevent SH0ES and Pantheon from being independent likelihood factors
Vacuum relation residual | R=4a0^2/(c2 G_N rho_L)-1 | compare independently derived ladder and background inputs without refitting a0
''')
seeds('Y2021S07','''
Orbital-decay intrinsic extraction | Pbdot_int=Pbdot_obs-Pbdot_Shk-Pbdot_Gal | isolate radiation reaction from kinematics
Post-Keplerian mass intersection | PK_a=f_a(mA,mB,theory) | derive an overdetermined common-mass test
Relativistic periastron second order | omegadot=omegadot_1PN+omegadot_2PN+omegadot_SO | resolve spin and higher-order dynamics
Shapiro range-shape independence | DeltaS=-2r ln(1-s sinphi) | infer null propagation without fixing dynamical masses
Light-bending timing term | Delta_bend(phi) | derive a conjunction-dependent null-geodesic correction
Aberration pulse-phase coupling | DeltaA depends on spin orientation and orbital velocity | separate geometric pulse effects from gravity
Gravitational redshift timing | gamma_E=e(Pb/2pi)^(1/3)G_eff^(2/3)F(mA,mB)/c2 | derive the action-specific Einstein delay
Mass-ratio kinematic identity | R=xB/xA | establish assumptions needed for theory-independent mass ratio
Spin-orbit inertia leverage | omegadot_SO proportional I_A Omega_A | separate moment of inertia from gravity coefficients
Proper-motion orbital tilt | xdot/x=cot i mu sin(theta_mu-Omega) | remove apparent orbital evolution
Distance-dependent Galactic correction | a_los=a_pulsar-a_sun | derive the external field using the same force law
Dipole-radiation suppression | Pbdot_dip proportional (sA-sB)^2 | bound strong-field sensitivities rather than add a scalar graviton
Quadrupole-flux normalization | Pbdot=F_Q(G_rad,G_dyn,mA,mB,e) | test distinct measured and radiative couplings
Finite propagation retarded delay | Delta_ret=integral k_mu u_mu dl | derive the light-time correction under one physical metric
Dispersion-measure chromaticity | Delta_DM=K DM/nu2 | distinguish plasma delay from achromatic gravity
Secular eccentricity evolution | edot=edot_rad+edot_tide+edot_kin | predict a distinct long-term orbital observable
Orbital inclination evolution | idot from spin and frame motion | isolate preferred-frame torque
Preferred-frame orbital polarization | e_vec=e_forced(w,alpha1)+e_free | derive a PPN-sensitive timing signature
Strong-equivalence orbital effect | delta a=(sA-sB)g_ext | constrain differential free fall of compact bodies
Timing-noise covariance projection | C_timing=C_white+C_red+C_DM | prevent red noise from mimicking secular gravity terms
Pulse-profile evolution nuisance | phi_template=phi_template(t) | quantify profile-dependent TOA bias
Energy-mass loss consistency | mdot=-L_spin/c2 | include pulsar rotational energy loss in orbital evolution
Sixteen-year incremental information | F_long-F_short with common TOAs | isolate new secular leverage over older timing reports
Conjunction-window robustness | PK_hat(exclude conjunction) | separate light-path terms from global orbital dynamics
Criterion-B retarded-source test | t_global increases along source-detector response | connect a surviving timing map to causal ordering without imposing a metric-cone rule
''')
seeds('Y2021S08','''
Pair error-inflation calibration | z=Delta varpi/sqrt(sigma1²+sigma2²-2Cov12) | infer measurement noise before gravitational velocity tails
Chance-alignment mixture force | p(v)=p_bound p_orbit+(1-p_bound)p_chance | retain empirical membership uncertainty
Projected speed normalization | vtilde=v_perp/sqrt(G_N M/r_perp) | derive its distribution under the selected pair geometry
Sky-shift background transport | p_chance(v,r,G) from shifted positions | test background representativeness
Angular-resolution completeness | S(theta,DeltaG) | correct missing close pairs and hidden companions
Unresolved-triple velocity tail | v_obs=v_wide+v_photocenter | isolate contamination from the wide-orbit force
Parallax-difference binary prior | r1-r2 small but nonzero | distinguish physical depth from catalog errors
Mass-luminosity correlated nuisance | M1+M2=f(G1,G2,color,D) | propagate shared distance into both mass and velocity
Eccentricity-selection degeneracy | p(v_perp|r_perp)=integral p(v,r|e)p(e)de | identify gravity dependence not fixed by orbital priors
Galactic tide survival | r_J=(GM/lambda_tide)^(1/3) | bound contamination beyond the bound-pair domain
External-field direction anisotropy | vtilde(theta_gext) | derive a directional signal of the nonspherical boundary condition
White-dwarf main-sequence differential test | Delta vtilde_WDMS-MSMS | separate compactness and age selection effects
Co-moving association contamination | p_stream(v,r|age) | identify pairs that share birth motion without being bound
Proper-motion perspective projection | Delta v=Delta mu D+projection(v_sys) | correct geometrical false relative velocity
Radial-velocity validation subset | v3D²=vperp²+Delta vr² | derive an independent boundness control
Pair covariance spatial kernel | Cov(mu1,mu2)=K(theta) | quantify cancellation of common astrometric modes
Astrometric-quality truncation | p(v|RUWE cut) | measure hidden velocity-dependent selection
Separation-dependent force slope | alpha=d ln <v²>/d ln r | distinguish an amplitude shift from a transition shape
Galactic latitude selection | S(b,G,theta) | test sky-dependent contamination and extinction
Binarity probability calibration | E[1_bound|p_bound]=p_bound | authenticate probabilities using withheld validation data
Wide-pair binding energy sign | E=v²/2+Phi_rel(r) | derive boundness for filtered MONO instead of Newtonian rejection
Orbital phase dwell weighting | p(r|orbit) proportional 1/|vr| | construct the selected phase distribution
Mass-dependent transition radius | r_M=sqrt(G_N M/a0) | test scaling with mass without per-pair a0 fitting
EDR3 catalog derivation increment | L_pairs|single-star-data | record that pair classification adds structure but not independent astrometric photons
Binary-to-galaxy external-field bridge | chi_ext_binary versus chi_ext_disk | derive a shared response relation before combining scales
''')
seeds('Y2021S09','''
Repeat-supernova calibration difference | Delta m=m_surveyA-m_surveyB | isolate survey zero points with identical explosions
Sibling-supernova intrinsic scatter | Var(m1-m2)=2sigma_int²+Var_noise | cancel host distance to calibrate luminosity scatter
Flux-level light-curve likelihood | F(t,lambda)=x0[M0+x1 M1]exp(c CL) | keep standardization separate from gravity distance predictions
Color-luminosity host dependence | beta=beta(host dust,stellar population) | bound a false redshift-dependent expansion signal
Stretch distribution evolution | p(x1|z) | separate selection-driven population changes from distance curvature
Observer-to-rest-frame band transport | lambda_rest=lambda_obs/(1+z) | derive K-correction sensitivity to spectral templates
Redshift uncertainty propagation | C_mu_z=J_z C_z J_z.T | retain correlated peculiar-velocity errors
Very-low-redshift nonlinearity | mu=5log10 dL+25 | model the non-Gaussian distance effect of uncertain redshift
Survey overlap graph rank | Delta zp edges; graph Laplacian L | identify calibration offsets actually anchored by repeated SNe
Host dust versus intrinsic color | c=c_dust+c_intrinsic | determine identifiable combinations using repeated and sibling data
Photometric covariance time structure | Cov(F_t,F_t') | propagate reference-image noise through light-curve fits
SALT training-data overlap | Cov(template,data) | avoid treating trained templates as independent calibrations
Detection-efficiency surface | S(F_peak,x1,c,z) | derive selection correction without assuming a cosmological posterior
Malmquist correction transport | Delta mu_bias(theta)=E[mu_hat-mu|selected] | recompute bias when the candidate changes distances
Host peculiar-velocity covariance | C_vij=<v_i v_j> | derive same-action flow covariance for nearby events
SN sibling dust differential | Delta c_sibling | test local dust assumptions at fixed host environment
Repeat-event weight normalization | W_event=sum_surveys W_event,survey | prevent duplicate light curves from multiplying independent explosions
Intrinsic-scatter chromatic mode | C_int(lambda,lambda') | separate wavelength-correlated scatter from gray luminosity variance
Time-dilation consistency | t_rest=t_obs/(1+z) | test temporal calibration independent of distance brightness
Cross-survey passband uncertainty | delta F=integral delta T(lambda)S(lambda)dlambda | propagate passband errors into the Hubble diagram
Calibration redshift eigenmode | delta mu(z)=sum a_n e_n(z) | identify calibration modes degenerate with vacuum evolution
Low-z sample incremental leverage | F_z<0.01 conditional on calibrators | quantify new velocity and intercept information in the expanded release
Standardization gravity sensitivity | M_B=M_B(G_star,composition) | derive whether same-action stellar gravity alters the empirical candle
Photon conservation distance duality | dL=(1+z)^2 dA under conserved photon number | make the metric and transport premises explicit
Light-curve to 2022-distance covariance | C_lightcurve,distance from common flux data | prepare the later inference without counting a new sample
''')
seeds('Y2021S10','''
Polarized null-geodesic transport | k^nu nabla_nu f^mu=0 | derive gravitational polarization rotation through the candidate metric
Complex linear polarization field | P=Q+iU=|P|exp(2i chi) | predict a metric-plus-plasma image without confusing magnetic orientation with slip
Azimuthal polarization coefficient | beta2=integral P exp(-2i phi)dOmega/integral I dOmega | extract a ring-geometry statistic sensitive to transported field structure
Fractional polarization beam bias | m=|B*P|/(B*I) | quantify unresolved cancellation before physical interpretation
Faraday rotation separation | chi(lambda)=chi0+RM lambda² | distinguish plasma rotation from achromatic metric transport
Station leakage degeneracy | V_obs=J_a V_true J_b† | derive instrumental D-term contamination of polarized visibilities
Polarimetric closure trace | T_abcd=tr(V_ab V_cb^-1 V_cd V_ad^-1)/2 | isolate station-gain invariant information
Ring-brightness polarization covariance | Cov(I,Q,U) | retain shared reconstruction uncertainty in fractional polarization
Temporal polarization variation | Delta P=P_day2-P_day1 | separate source evolution from static metric structure
Image-prior orientation bias | p(P|regularization) | bound the reconstruction's imposed azimuthal pattern
Scattering Mueller transfer | S_obs=M_scatter S_intrinsic | propagate polarization-dependent transfer before ray tracing
Synchrotron pitch-angle map | j_P/j_I=Pi(p)exp(2i chi_B) | derive the source emissivity assumptions needed by a gravity constraint
Optical-depth depolarization | P_obs=integral j_P exp(-tau)dl | separate emitting-depth changes from geometric rotation
Circular-linear leakage control | V_stokes into Q,U via J | bound false linear patterns using calibration uncertainty
Polarization ring-radius contrast | R_P/R_I | derive a distinct spatial observable from the new Stokes data
Spin-inclination polarization degeneracy | rank d(beta2,m)/d(a,i,Bgeometry) | determine whether geometry is identifiable after plasma freedom
Null-congruence shear effect | d sigma/dlambda+2theta sigma=C_kakb | derive metric tidal distortion of polarized emission
Photon-ring path-order signature | P_n=transport_n(P_emission) | assess whether unresolved higher-order paths leave a measurable polarization moment
Polarization parity statistic | P(phi)-P*(-phi) | distinguish mirror asymmetry from calibration rotation
Total-intensity reuse exclusion | L_joint=L_I L_P|I | add polarization information without recounting the 2019 intensity measurement
Magnetic-field energy nuisance | beta_plasma=P_gas/(B²/2mu0) | prevent an assumed plasma state from becoming a gravity certificate
Week-scale variability structure function | D_P(Delta t)=<|P(t+Delta t)-P(t)|²> | measure evolving emission within the same campaign
Polarization basis invariance | P->exp(-2i psi)P | certify coordinate-independent reported moments
Independent imaging agreement covariance | C_reconstructionA,B from same visibilities | avoid treating image pipelines as independent experiments
M87 weak-to-strong metric bridge | metric_outer matched to metric_photon_region | derive a boundary-matching obligation before transferring galaxy-scale MONO to the ring
''')
source(2022,1,'Pantheon+ distances','2202.04077','2022-02-08','The Pantheon+ Analysis: Cosmological Constraints','D. Brout et al.','New bias-corrected SN distance and cosmological inference using Pantheon+ light curves.','Same underlying light-curve release first reported in 2021','SH0ES_Pantheon_distance_ladder','Derive dL from the candidate expanding solution and its conserved-photon metric; gates 5,8,11,13.','Bias-corrected distance vector, redshift/selection/calibration covariance and light-curve provenance; LCDM parameter posterior is not raw distance data.','substitute duplicate light curves for independent explosions','recover the source reference distance likelihood before transporting it','2022 adds distance-bias corrections and cosmological inference to 2021 flux data; tasks isolate that processing increment')
source(2022,2,'Gaia DR3 new products','2208.00211','2022-07-30','Gaia Data Release 3: Summary of the content and survey properties','Gaia Collaboration; A. Vallenari et al.','New radial velocities, spectra, binary solutions and other products; core astrometry retained from EDR3.','First 34 months of mission; same astrometric baseline as EDR3','Gaia_stellar_astrometry','Derive phase-space observation maps and binary dynamics from the same filtered action; gates 1,4,10.','New DR3 radial velocities, binary solutions, astrophysical spectra and selection metadata; EDR3 astrometry counted once.','relabel inherited EDR3 astrometry as new and show the spurious information gain','compare spectroscopic and astrometric orbital constraints where both exist','2022 new radial velocities and non-single-star solutions add dynamical components absent from EDR3')
S['Y2022S02']['date_basis']='2022-07-30 is the authenticated first arXiv report date for this summary, not a claim of the earliest archive release. Gaia DR3 actual archive release preceded this report within 2022; exact release date was not authenticated because official release pages failed to fetch. Calendar-year assignment is supported by the primary 2022 report.'
S['Y2022S02']['verification']+=' Opened v1 HTML and inspected abstract plus content/caveat locators; official release-page fetch failed. Exact first archive-release day remains unverified.'
source(2022,3,'SPT-3G added TT','2212.05642','2022-12-12','A Measurement of the CMB Temperature Power Spectrum and Constraints on Cosmology from the SPT-3G 2018 TT/TE/EE Data Set','L. Balkenhol et al.','New multifrequency temperature spectrum and updated joint covariance with earlier polarization spectra.','2018 observations; TT is new reported product, EE/TE reused','SPT3G_2018_CMB','Derive temperature, polarization and lensing transfer consistently from one action; gates 5,8,13.','New TT bands, TE/EE cross-covariance and updated nuisance operators; inherited polarization data are conditioned on once.','multiply old EE/TE likelihood twice and show false precision','predict TT conditionally from the earlier polarization release','2022 temperature information and revised joint covariance permit withheld-observable tests of the 2021 polarization inference')
source(2022,4,'MICROSCOPE final','2209.15487','2022-09-14','MICROSCOPE mission: final results of the test of the Equivalence Principle','P. Touboul et al.','Differential free-fall acceleration of titanium/platinum and platinum/platinum test masses.','Two-and-a-half-year mission with accumulated science segments; exact dates uninspected','MICROSCOPE_equivalence','Derive inertial/gravitational mass matching and force response from the ordinary-matter action; gates 4,5,10,11.','Differential electrostatic acceleration, orbital/spin phase, thermal/glitch templates and reference-mass channel.','inject a false composition label in the platinum reference pair','recover the known orbital-phase template with an independent time-domain fit','2022 final mission analysis adds a measured composition-sensitive force constraint and explicit thermal/transient systematics')
S['Y2022S04'].update(primary_url='https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.129.121102',date_basis='Opened primary PRL page: published 14 September 2022; this precedes the 30 September arXiv deposit.',version='PRL 129,121102 published 2022-09-14; arXiv v1 2022-09-30',source_locator='PRL publication metadata and Abstract; arXiv abstract',verification='Opened PRL abstract/publication metadata and arXiv abstract. Full time series and covariance uninspected.')
source(2022,5,'LEGA-C full-spectrum chronometers','2205.05701','2022-05-11','New Observational H(z) Data from Full-Spectrum Fitting of Cosmic Chronometers in the LEGA-C Survey','K. Jiao, N. Borghi, M. Moresco and T.-J. Zhang','Stellar-age fits and differential-age expansion measurement from passive-galaxy spectra.','LEGA-C spectra; same galaxies may overlap earlier Lick-index chronometers','LEGA-C_chronometers','Derive the relation between proper stellar age, redshift and the candidate homogeneous expansion; gates 5,8,13.','Passive-galaxy spectra, redshifts, fitted-age likelihoods and stellar-population nuisance models.','shuffle galaxy ages across redshift while retaining their errors','compare full-spectrum and Lick-index age differences for the same galaxies','2022 full-spectrum age inference adds a method-dependent expansion measurement and systematic comparison rather than independent photons')
source(2022,6,'JWST SMACS0723 lens','2207.07567','2022-07-15','First JWST observations of a gravitational lens: Mass model from new multiple images with near-infrared observations of SMACS J0723.3-7327','G. B. Caminha et al.','New JWST multiple-image positions augment pre-JWST cluster lens constraints.','JWST early-release 2022 images plus earlier HST/MUSE data','SMACS0723_cluster_lensing','Derive both cluster metric potentials and the lens equation from one action without importing a halo; gates 1,3,8,11.','New and old image positions, measured redshifts, photometry, masks and source-identification uncertainty.','swap source-family labels for multiple images','withhold one multiply imaged source and predict its positions','2022 new arcs increase independent constraints on the same cluster; tasks isolate new images and explicit old-new model change')
source(2022,7,'Cosmicflows-4 distances','2209.11238','2022-09-22','Cosmicflows-4','R. B. Tully et al.','Compiled galaxy/group distances with cross-method calibration and inferred peculiar velocities.','Multiple surveys and epochs; new 2022 compilation','Cosmicflows_distance_velocity','Derive the distance-redshift relation and peculiar-velocity response of conserved matter; gates 1,5,8,13.','Galaxy distances, redshifts, method labels, group membership and correlated zero-point uncertainties.','randomize sky directions while preserving distance errors','compare independently calibrated distance methods in common groups','2022 enlarged distance compilation and cross-calibration add observed spatial information while retaining old-object overlap')
source(2022,8,'PSR J0952 optical orbit','2207.05124','2022-07-11','PSR J0952-0607: The Fastest and Heaviest Known Galactic Neutron Star','R. W. Romani et al.','Companion multicolor light curves and radial velocities yielding conditional neutron-star mass.','Keck spectrophotometry and imaging; exact epochs uninspected','PSRJ0952_optical_orbit','Derive orbital dynamics, stellar heating and compact-object structure consistently; gates 4,5,10.','Phase-resolved companion spectra, radial velocities, multiband flux and orbital timing; published mass is model-dependent.','use luminosity-weighted velocity as center-of-mass velocity without correction','cross-check orbital amplitude with independent spectral-line subsets','2022 optical orbital measurements add strong-field source information, not a theory-independent maximum-mass datum')
source(2022,9,'Cosmicflows-4 field inference','2211.16390','2022-11-29','Gravity in the Local Universe: density and velocity fields using CosmicFlows-4','H. M. Courtois et al.','Reconstructed local velocity/density fields, pairwise velocity growth and bulk-flow measurements.','Same Cosmicflows-4 distances; 2022 field-processing increment','Cosmicflows_distance_velocity','Derive the velocity-density Green function and boundaries from the candidate action; gates 1,5,7,8.','Radial peculiar velocities, reconstruction operators, masks and covariance; reconstructed densities are model-conditioned products.','treat a reconstruction prior as an independent density observation','compare grouped and ungrouped velocity estimators with common-data covariance','2022 field reconstruction adds an estimator and growth inference to the September distance compilation, not independent distances')
source(2022,10,'Gaia BH1 orbit','2209.06833','2022-09-14','A Sun-like star orbiting a black hole','K. El-Badry et al.','Gaia astrometric orbit plus new radial velocities and spectroscopy of a dormant compact companion system.','Gaia DR3 astrometry plus ground-based follow-up; exact dates uninspected','Gaia_stellar_astrometry','Derive timelike binary motion and astrometric/velocity projection from the same high-acceleration limit; gates 4,10,11.','Gaia orbital solution/covariance, follow-up radial velocities and companion light limits; astrometric epoch data access unverified.','fit a luminous companion inconsistent with the measured spectral light limits','infer a spectroscopic mass function before adding Gaia orbital inclination','2022 radial-velocity validation adds information beyond a catalog dark-companion candidate; inherited Gaia data count once')
seeds('Y2022S01','''
Distance-covariance transport | C_new=J C_flux J.T+C_bias | derive the 2022 distance-vector covariance from the 2021 light curves
Bias-correction cosmology dependence | d mu_bias/dtheta | quantify selection corrections that must change under candidate expansion
Absolute-magnitude null direction | mu->mu+Delta; M_B->M_B-Delta | identify the unanchored distance degree of freedom
Deceleration from distance curvature | q(z)=(1+z)H'/H-1 | reconstruct expansion only on data-supported derivative scales
Jerk identifiability | j=q(2q+1)+(1+z)dq/dz | bound higher-derivative information in the expanded Hubble diagram
Curvature-luminosity degeneracy | dL=(1+z)S_k(integral c/H dz) | separate geometry assumptions from vacuum evolution
Piecewise expansion integral | dL_i=(1+zi)sum_j c Delta z_j/H_j | fit measured distances without a w0wa prior
Dark-energy density reconstruction | rho_DE=3H²/(8pi G_cosmo)-rho_m-rho_k | expose coupling and matter assumptions behind a0 inference
Constant-vacuum derivative test | d rho_L/dz=0 | test a constant scale against distance-supported expansion shape
Scale evolution conditional map | a0(z)/a0(0)=sqrt(rho_DE(z)/rho_DE(0)) | identify the exact assumptions needed to export SN results to galaxy physics
Redshift calibration mode | delta mu=5/(ln10) dln dL/dz delta z | bound spectroscopic redshift errors that mimic acceleration
Low-z velocity correction update | Delta mu_v approximately 5vpec/(ln10 cz) | isolate changed flow corrections from new supernova information
Distance-ladder common intercept | Cov(M_B,H0) | propagate shared Cepheid calibration once
SN-only shape likelihood | P_perp=I-1(1.T C^-1 1)^-1 1.T C^-1 | project out absolute magnitude before expansion tests
Survey-block systematic eigenmodes | C_sys=sum sigma_k² u_k u_k.T | identify dominant cross-survey calibration directions
Intrinsic-scatter model transport | C_int(theta_scatter) | quantify gravity inference changed by gray versus chromatic scatter
Host-population evolution | Delta M(z)=gamma f_host(z) | bound astrophysical brightness evolution separately from dL
Distance-duality comparison requirement | eta=dL/[(1+z)²dA] | derive an independent lensing/BAO bridge with no shared ruler counted twice
Robust outlier leverage | h_i=J_i F^-1 J_i.T/C_ii | identify individual SNe dominating curvature inference
High-redshift extension information | F_high|low | measure incremental expansion leverage from added redshift range
Pantheon-to-Pantheon+ overlap | C_cross from repeated SNe and zero points | compute the update without multiplying two Hubble diagrams
CMB-combination theory quarantine | L_CMB(theta) requires new transfer map | prevent a LCDM-compressed prior from certifying the candidate background
BAO inverse-ladder ruler freedom | H0 r_d constrained, H0 and r_d separately free | derive what combined distance data actually measure
Canonical-alternative vacuum likelihood | Delta lnL=r(a_can).T C^-1 r(a_can)-r(a_alt).T C^-1 r(a_alt) | compare fixed footings after deriving rho_L-to-distance dynamics
2021-to-2022 conditional evidence | L_distance|flux-processing | characterize new calibration/bias information without asserting fresh photons
''')
seeds('Y2022S02','''
New radial-velocity phase-space gain | v=(v_alpha,v_delta,v_r) | quantify dynamical information absent from EDR3 tangential motion
Spectroscopic selection gravity bias | S(G_RVS,Teff,sky) | derive tracer selection before a Galactic force estimate
Binary orbital photocenter transfer | p(alpha_ph)=integral delta_D[alpha_ph-(B-beta)a_rel/D]p(B,beta,a_rel,D)dB dbeta da_rel dD | connect non-single-star astrometry to mass ratios
Astrometric-spectroscopic orbit closure | a1 sin i=K1 P sqrt(1-e²)/(2pi) | compare independent orbit projections
DR3 inherited-astrometry exclusion | C_joint treats EDR3 block identically | prevent spurious parallax information gain
Radial-velocity template mismatch | v_meas=v_true+delta v(Teff,logg,Z) | bound a false Galactic streaming signal
Spectral gravitational redshift | v_gr=GM/(Rc) | distinguish stellar surface potential from center-of-mass velocity
Convective blueshift nuisance | v_spec=v_kin+v_gr+v_conv | derive spectroscopic systematics before testing gravity
Non-single-star selection transfer | P_NSS(P,e,alpha,SNR) | quantify orbital catalog completeness for gravity tests
Acceleration-solution absorption | theta(t)=theta0+mu t+0.5 adot t² | identify constant-acceleration information in catalog fits
Orbit-period alias support | L(P)=sum_alias L_alias(P) | avoid false force precision from one orbital mode
Milky-Way radial Jeans closure | g_R=-[partial_R(nu mean(vR²))+partial_z(nu mean(vR vz))+nu(mean(vR²)-mean(vphi²))/R]/nu | use the new radial velocities for a full moment constraint
Vertical velocity tilt measurement | sigma_Rz=<v_R v_z> | obtain the pressure cross term previously inaccessible
Phase-spiral disequilibrium clock | theta_z=Omega_z(J_z)t | derive force information without steady-state Jeans assumptions
Open-cluster escape envelope | v_esc²=2[Phi_boundary-Phi(r)] | connect new velocities to a finite-boundary potential
Binary mass-light degeneracy | M_dyn versus M_phot(Teff,luminosity) | separate stellar models from orbital gravity
Mean-spectrum covariance | C_spectrum includes basis-coefficient correlations | propagate spectral parameter errors into baryonic source masses
RVS line broadening contamination | sigma_line²=sigma_rot²+sigma_inst²+sigma_macro² | quantify velocity-estimator bias from broad spectra
Sky-inhomogeneous RVS sampling | n_obs(n)=S(n)n_true(n) | isolate large-scale velocity anisotropy from selection
Asteroid astrometric force residual | ddot r=-grad Phi+F_nongrav/m | use new epoch products only with explicit nongravitational terms
Microlensing event geometry | theta_E²=4G_lens M Dls/(c²DlDs) | derive the lensing coupling before compact-mass inference
Variability-based distance coupling | M_variable=f(period,Z,G_star) | expose gravity assumptions in newly classified distance tracers
Chemical-tracer force agreement | g_R(tracerA)-g_R(tracerB) | compare populations after measured abundance selection
Binary-to-field velocity covariance | C_v includes orbital contamination | remove unresolved orbital motion from Galactic dispersion
New-product conditional likelihood | L_DR3=L_EDR3 L_RVS,NSS,spectra|EDR3 | define the correct 2022 information increment
''')
seeds('Y2022S03','''
TT conditional polarization prediction | mean(TT|pol)=m_T+C_TP C_PP^-1(d_P-m_P) | test genuinely new temperature information
Joint covariance update effect | DeltaF=J.T(C_new^-1-C_old^-1)J | distinguish covariance revision from added data
Temperature acoustic odd-even contrast | A_odd/A_even | test baryon loading with a new observable channel
TT damping-tail heat response | dC_TT/dxi | compare the operative filter signature to polarization-only predictions
Thermal SZ spectral separation | DeltaT/T=y[x coth(x/2)-4] | remove hot-gas pressure contamination from gravity-sensitive temperature bands
Kinetic SZ degeneracy | DeltaT/T=-integral ne sigmaT vlos/c dl | derive velocity response before treating kSZ as a free amplitude
Cosmic infrared background correlation | C_CIB(nu1,nu2)=r sqrt(C11 C22) | isolate frequency-decorrelated emission from CMB lensing smoothing
Radio point-source temperature tail | D_ell_ps proportional ell² | bound residual small-scale source power
tSZ-CIB cross covariance | C_total includes 2C_tSZ,CIB | quantify omitted cross terms in the new TT likelihood
TT-TE acoustic phase consistency | Delta phi=phi_TT-phi_TE | test linked density and velocity transfer solutions
TT-EE lensing consistency | A_L_TT-A_L_EE | derive a new-channel Weyl-potential test
Temperature beam eigenmode | delta ln B_ell=sum a_n e_n(ell) | propagate beam calibration into TT damping
Frequency triangle closure | C_95x150 C_150x220/C_95x220 | test redundant relative calibration with common CMB signal
TT mask coupling | pseudo C_TT=M C_TT | transport model spectra through the new temperature mask
Temperature-polarization leakage | T_obs=T+epsilon E | bound detector leakage in joint covariance
SPT temperature Planck comparison | Delta C_TT=C_SPT-W C_Planck | cancel common sky before claiming independent tension
Primordial amplitude recovery | TT,TE,EE constrain A_s exp(-2tau) | identify remaining low-ell optical-depth dependence
Temperature recombination response | dC_TT/dx_e(z) | separate recombination uncertainty from candidate gravity
Baryon-clumping nuisance | <ne²>/<ne>² | assess a microphysics alternative without silently adding it to the gravity model
Early-potential decay signature | Delta Theta_ISW=integral(Phi'+Psi')deta | isolate TT information absent from pure polarization
TT-only high-ell residual mode | r_perp=P_nuisperp(d_TT-m_TT) | construct a calibrated departure statistic
Polarization inheritance ledger | logL_joint=logL_pol+logL_TT|pol | avoid using the 2021 EE/TE sample twice
Foreground prior sensitivity | d theta_grav/d lambda_foreground | quantify new-temperature constraint dependence on nuisance priors
Multipole truncation challenge | theta_hat(ellmax) | determine where nonlinear foreground uncertainty controls inference
Same-action channel prediction certificate | [TT,TE,EE]=T_action(theta) | require one transfer solution for all channels before empirical closure claims
''')
seeds('Y2022S04','''
Composition response from matter action | eta_AB=2(a_A-a_B)/(a_A+a_B) | derive differential acceleration rather than assume universal coupling
Orbital-phase matched estimator | etahat=(g.T C^-1 d)/(g.T C^-1 g) | estimate the WEP template with colored noise
Thermal coherent contamination | d_thermal=H_T*T(t) | bound temperature response at the equivalence-test frequency
Glitch transfer into orbital harmonic | d_glitch=sum A_k h(t-tk) | quantify leakage of short-lived events into eta
Reference-pair null calibration | eta_PtPt=0 under identical material response | use the measured reference channel to calibrate false signals
Miscentering gravity-gradient term | Delta a=T_Earth Delta x | separate tidal acceleration from composition dependence
Spin-frequency sideband structure | f_EP=f_orbit+f_spin | derive the phase convention of the measurement template
Electrostatic stiffness correction | a_es=-k_es x | propagate position-control dynamics into force inference
Common-mode rejection | d_diff=d_A-d_B+epsilon d_common | bound residual spacecraft acceleration leakage
Quadratic sensor nonlinearity | d_meas=d_true+q d_true² | predict harmonic contamination in the science band
Drag-free control transfer | a_res=H_control a_disturbance | derive which disturbances survive feedback
Rotation-centrifugal differential term | Delta a_rot=Omega cross(Omega cross Delta x) | compute inertial contamination with actual attitude data
Coriolis velocity term | Delta a_C=2Omega cross Delta v | isolate residual test-mass motion from gravitational force
Earth multipole template | Phi_E=-GM/r[1-sum J_l(R/r)^l P_l] | calculate the gravity-gradient model required by eta extraction
Material self-energy response | m_g/m_i=1+s U_self/(mc²) | separate strong-equivalence sensitivity from composition charge
Preferred-frame satellite response | delta a=F(alpha1,alpha2,w,spin) | derive a PPN signature in the mission geometry
Time-variable G coupling | a(t)=G_N(t)M/r² | determine differential versus common sensitivity of the instrument
Filter-scale terrestrial limit | xi/L_instrument | derive high-acceleration recovery for finite test-body geometry
Thermal phase uncertainty | H_T(f)=|H_T|exp(i phi_T) | bound phase-aligned systematic cancellation
Missing-data spectral window | d_obs=W(t)d(t) | quantify gaps that mix unrelated frequencies into the science harmonic
Colored-noise likelihood | C_ij=integral S(f)exp(2pi ifDelta t)df | derive correct confidence coverage for eta
Segment combination covariance | C_eta,ij includes shared calibration | combine mission segments without shrinking systematic floors
Blind-signal injection recovery | d->d+eta_inj g | demonstrate estimator response under the full reduction
Final-versus-initial mission increment | C_delta=C_final+C_initial-2C_cross | isolate new data and calibration leverage over early MICROSCOPE results
Universal-metric implication audit | nabla_mu T_A^munu=0 for each material | prove the exact matter-conservation premise connecting eta to the closure gates
''')
seeds('Y2022S05','''
Differential-age expansion map | H(z)=-1/[(1+z)dt/dz] | derive the proper-time clock relation in the candidate metric
Age-redshift slope posterior | t_i=t0+s(z_i-z0)+epsilon_i | infer a local derivative without fixing a cosmological age prior
Mass-dependent formation bias | t_star(z,M)=t_univ(z)-t_form(M,z) | separate downsizing from expansion
Full-spectrum versus Lick covariance | Delta t=t_full-t_Lick | compare methods on identical photons with shared errors
Stellar-library gravity dependence | F_lambda=F_lambda(age,Z,G_star) | derive whether modified stellar structure biases the clock
Metallicity-age degeneracy | J=[dF/dt,dF/dZ] | identify spectral directions that actually determine differential age
Dust-age spectral degeneracy | F_obs=F_intrinsic exp[-tau(lambda)] | bound reddening absorption of an age trend
Star-formation history mixture | F_lambda=integral SFR(t)SSP_lambda(age-t)dt | quantify old-population clock contamination
Young-star frosting bias | F=(1-f)F_old+f F_young | bound a small luminous young component in passive galaxies
Spectral-resolution transport | F_obs=LSF*F_model | derive the age bias from instrumental line broadening
Flux-calibration polynomial | F_obs=P(lambda)F_model | separate smooth calibration from age-sensitive spectral features
Noise-rescaling age uncertainty | C_true=s² C_pipeline | infer noise calibration before differentiating ages
Photometry-assisted age shift | Delta t=t_spectrum+photo-t_spectrum | isolate additional information and shared calibration
Passive-selection truncation | p(age|selected,z) | correct redshift-dependent passive-galaxy selection
Age-boundary prior effect | t_star<t_univ_prior(z) | detect circular cosmological information in spectral fitting
Redshift-bin finite-width bias | <dt/dz> versus Delta <t>/Delta z | quantify nonlinear averaging in H(z)
Asymmetric H likelihood | H=-1/[(1+z)s] | propagate a non-Gaussian slope posterior without symmetric-error substitution
Progenitor contamination drift | dt_form/dz | bound changing population membership along redshift
Correlated stellar-model systematic | Cov(t_i,t_j)=K_model(Z_i,Z_j) | avoid independent-error treatment of one shared library
Age offset cancellation | dt/dz invariant under t->t+constant | distinguish harmless common age offsets from slope systematics
Chronometer-ruler cross test | H_CC r_d versus (H r_d)_BAO | derive a sound-horizon measurement with explicit overlap assumptions
Chronometer-SN derivative closure | H_CC^-1 approximately d[D_L/(1+z)]/cdz | test geometry with covariance-aware smoothing
Vacuum-scale chronometer match | rho_L=3H²/(8pi G_cosmo)-rho_other | retain all density and coupling premises
Common-sample information increment | L_full-spectrum|Lick | identify method validation rather than doubled chronometer count
Clock conservation bridge | d tau_star/d tau_metric | derive the ordinary-matter clock premise needed by the expansion inference
''')
seeds('Y2022S06','''
New-arc lens-equation residual | beta_s=theta_i-alpha(theta_i,z_s) | test one source position across its measured new images
Pre-JWST to JWST conditional map | L_newarcs|oldarcs | isolate information carried by newly identified systems
Cluster baryon-only potential | Delta u=4pi G_N rho_b | construct the actual filtered source map before fitting a lensing mass
Weyl-potential image deflection | alpha=integral grad_perp(Phi+Psi)dl/c² | derive the photon observable from both metric fields
Multiple-source redshift lever | alpha_s proportional Dls/Ds | separate geometry from deflector normalization
Unknown-redshift source degeneracy | beta_s, z_s, alpha jointly free | prevent model-predicted redshifts becoming independent data
Image-family misidentification mixture | p(theta)=p_family L_family+(1-p_family)L_outlier | retain uncertainty in new JWST arc associations
Critical-curve topology | det(I-Hess psi)=0 | predict the observed image parity structure
Caustic area response | A_caustic=integral inside caustic d²beta | quantify source-selection bias under changed gravity
Galaxy-member perturbation | psi=psi_cluster+sum psi_member | derive baryonic substructure without arbitrary halo insertion
Finite-cluster filter boundary | S=exp(xi² Delta_domain/2) | measure sensitivity to domain and outer mass support
Line-of-sight lens-plane coupling | A_multi=I-sum U_i+sum beta_ij U_i U_j | bound a single-plane approximation
Magnification near-critical uncertainty | mu=1/det A | propagate nonlinear tails instead of Gaussian magnification errors
Source-plane versus image-plane bias | chi2_beta versus chi2_theta with Jacobian | derive the likelihood that does not favor high magnification
Einstein-aperture mass translation | M_E=pi R_E² Sigma_crit only under the specified lens map | distinguish GR effective mass from baryonic source mass
Central-image detectability | flux_central=mu_central F_source | derive a constraint using the actual detection threshold
Radial-arc derivative response | lambda_r=1-dalpha/dtheta | test the slope of the same-action potential
Tangential-arc curvature | curvature(theta_arc) depends on third derivatives psi | extract a derivative observable beyond point positions
PSF-limited centroid covariance | C_theta from PSF and arc morphology | bound image-position precision before force inference
Cluster member light-to-mass prior | rho_star=Upsilon_j I_j | propagate correlated population assumptions
Gas-map missing-source envelope | alpha_missing=operator[rho_gas_missing] | quantify required unmeasured baryonic support
Mass-sheet residual freedom | psi_lambda=lambda psi+(1-lambda)theta²/2 | characterize degeneracy with multiple source redshifts
Withheld-source predictive likelihood | p(theta_holdout|remaining families) | test out-of-sample caustic geometry
Canonical-alternative arc displacement | Delta theta=theta(a0_alt)-theta(a0_can) | compare fixed normalizations in measured angular units
Cluster-to-galaxy same-action bridge | shared xi,gate,couplings across source scales | specify a compatibility test without combining different empirical force laws
''')
seeds('Y2022S07','''
Distance-method overlap graph | mu_ij=mu_true_i+zp_j+noise | solve identifiable intermethod zero points
Grouped distance covariance | C_group=H C_gal H.T | carry shared calibration into group velocities
Log-distance to velocity transform | eta=log10(dz/d); v=c z-Hd | derive non-Gaussian peculiar-velocity likelihoods
Malmquist posterior correction | p(d|mu,selected) proportional L pi(d)S(d) | separate spatial selection from velocity inference
TF linewidth gravity dependence | M=a+b log W | derive how empirical linewidth calibration transports across force laws
Fundamental-plane dynamical dependence | log R=a log sigma+b log I+c | expose gravity assumptions in elliptical distances
SN cross-calibration overlap | Cov(mu_SN,mu_other) | account for shared supernovae with Pantheon+
Group-membership uncertainty | p(group_i|sky,z,d) | propagate uncertain associations into distance precision
Local monopole versus H0 | v_r=deltaH r+v_res | identify the expansion mode degenerate with distance zero point
Bulk-flow vector estimator | B=(sum w n n.T)^-1 sum w v_r n | derive window-weighted coherent motion
Velocity shear tensor | v_i=B_i+S_ij r_j | infer quadrupolar flow separately from the dipole
Radial selection window | W(k)=sum w_i exp(ik.r_i) | characterize scales actually measured by the catalog
Distance-method directional bias | zp_j(n)=zp_j0+d_j.n | test calibration dipoles that mimic bulk flow
Local void geometry correction | dL(z,n)=dL_bg+delta dL_pec | derive a directional distance map without importing a void profile
Group virial-motion suppression | v_gal=v_group+v_internal | quantify the tradeoff between grouped and individual velocities
TF inclination covariance | W_corr=W_obs/sin i | propagate correlated inclination errors into distances and source masses
FP aperture correction | sigma_corr=sigma_ap(R_ap/R_ref)^gamma | bound method-dependent velocity-dispersion calibration
TRGB anchor transport | M_TRGB=f(Z,G_star) | derive the stellar-gravity premise of the distance anchor
Surface-brightness-fluctuation calibration | mbar=Mbar(color)+mu | separate population scatter from distance fluctuations
Cepheid cross-anchor dependence | C_Cepheid includes common geometric anchors | retain ladder overlap in the full compilation
Low-redshift relativistic velocity definition | 1+z_obs=(1+z_cos)(1+z_pec) | bound linear cz approximations
Catalog-edge gravitational boundary | v_boundary=G_velocity[rho_outside] | quantify unseen external mass influence
New-versus-CF3 information | L_CF4|CF3 with shared galaxies | isolate added distances and recalibration
Vacuum-scale flow consistency | a0 fixed by rho_L while growth kernel predicts v | derive a same-action background-to-flow constraint
Distance-error tail robustness | p(mu)=Student_t or calibrated mixture | test whether coherent-flow evidence is driven by rare distance outliers
''')
seeds('Y2022S08','''
Companion mass function | f(M)=P K2³(1-e²)^(3/2)/(2pi G_dyn) | derive the dynamical relation before interpreting neutron-star mass
Irradiation velocity correction | K_COM=K_light+Delta K(heating) | separate luminosity weighting from center-of-mass motion
Light-curve inclination response | F(phi)=integral_visible I(T,mu)dA | infer geometry with an explicit heating model
Roche-lobe fill factor | f_R=R_comp/R_Roche(q) | propagate shape uncertainty into inclination and mass
Night-side flux bound | F_min=F_comp_night+F_contaminant | constrain inclination with the faint orbital phase
Day-side temperature distribution | sigmaSB T4=sigmaSB T0^4+F_irr(1-A) | derive energy balance rather than fit arbitrary hotspots
Spectral-line heating weights | v_line=integral I_line vlos dA/integral I_line dA | compare line-dependent orbital amplitudes
Asymmetric heating harmonic | F(phi)=F0+A1 cosphi+B1 sinphi+A2 cos2phi | isolate displaced heating from ellipsoidal geometry
Mass-inclination covariance | M_NS proportional K2³/sin³i | quantify nonlinear tails in the mass inference
Gravity-darkening response | T_eff proportional g_surface^beta | derive the local-gravity imprint on companion light
Limb-darkening nuisance | I(mu)=I0[1-u(1-mu)] | bound geometry bias from atmosphere assumptions
Distance-extinction covariance | F_obs=F_intrinsic exp(-tau)/D² | separate luminosity normalization from inclination
Orbital timing mass ratio | q=K2/K_NS | connect optical and radio orbital measurements consistently
Rapid-rotation support | M_max(Omega)=M_TOV+DeltaM_rot | separate a rotating star's measured mass from a nonrotating maximum
Same-action stellar equilibrium | dP/dr=F_TOV_action(rho,P,m) | derive the compact-star existence condition without imported GR TOV
EOS causality versus criterion B | cs²=dP/depsilon; gravitational cones separate | distinguish material sound-speed assumptions from the gravity causality target
Spin-induced shape correction | R(theta)=R0+R2 P2(costheta) | quantify rotating-star mass-radius mapping
Binding-energy mass distinction | M_grav=M_baryon-E_bind/c² | retain theory dependence of neutron-star mass support
Phase-limited RV sampling | F_K=sum_phase (dv/dK)²/sigma² | identify orbital amplitude information missing on the dark side
Atmospheric wind velocity | v_meas=v_orbit+v_wind(phi) | bound irradiation-driven velocity contamination
Template spectral mismatch | Delta v_template(T,Z,g) | quantify cross-correlation bias on the illuminated hemisphere
Photometric contamination mixture | F_total=F_comp+F_background | derive mass bias from unresolved constant light
Strong-field G normalization | G_dyn=G_N Z_body | separate measured Newton coupling from compact binary dynamics
Independent-line subset prediction | p(v_linesB|linesA,photometry) | test heating corrections with withheld spectra
Later-mass-update baseline | likelihood_2022 fixed before future photometry | create a reproducible reference for genuinely new orbital-phase observations
''')
seeds('Y2022S09','''
Velocity-density Green function | v(k)=i aH f(k) k delta(k)/k² | replace a GR inversion kernel by an action-derived one
Radial projection nullspace | u_i=n_i.v(r_i) | identify transverse velocity components unconstrained by the catalog
Wiener prior imprint | vhat=C_vu(C_uu+N)^-1 u | quantify reconstructed structure inherited from the prior
Grouped-ungrouped growth covariance | Cov(fs8_g,fs8_u) | compare estimators without treating them as independent measurements
SN-subset overlap projection | C_SN,all nonzero | isolate information from the supernova subset
Pairwise radial correlation geometry | <u_i u_j>=n_i^a n_j^b Psi_ab(rij) | derive the measured tensor projection
Bulk-flow window normalization | <B²>=integral P_v(k)|W(k)|²dk | relate the reported flow to a candidate spectrum
Density zero-mode exclusion | delta(k=0) not recovered from peculiar velocities | keep homogeneous expansion separate from local constraints
Reconstruction boundary mode | v=v_internal+v_external | bound finite-volume exterior influence
Velocity divergence estimator | theta=div v/(aH) | quantify differentiation noise and smoothing bias
Filter-scale reconstruction transfer | vhat(k)=T_rec(k)S_action(k)v_source(k) | separate numerical smoothing from physical filtering
Growth-amplitude model dependence | fsigma8 compressed from assumed Pshape | derive shape response before importing its posterior
Velocity vorticity null | curl v=0 only for specified dynamics | test an unassumed vector component
Distance-zero-point flow mode | delta mu constant -> v_r proportional r | isolate monopole calibration from density inference
Mask-induced bulk-flow mixing | B_obs=M B_true+L shear | quantify anisotropic-window leakage
Constrained-realization spread | Cov_rec=E[(v-vhat)(v-vhat).T] | interpret reconstruction uncertainty versus measurement uncertainty
Pair-weight selection bias | w_ij depends on distance and error | derive the effective growth-redshift window
Nonlinear velocity dispersion | Psi=Psi_linear+sigma_nl² delta_ij | bound small-scale contamination of large-scale growth
Redshift-space position correction | r_true=r_z-v_r/H | iterate coordinates consistently with the inferred velocity
Hubble-normalization conditional fit | p(H0|u,prior_velocity) | separate distance information from the reconstruction's assumed prior
Reconstruction phase correlation | r(k)=P_rec,true/sqrt(P_rec P_true) | measure recoverable phases using matched synthetic controls
Action-derived Euler closure | vdot+Hv+(v.grad)v=-grad Phi/a | link velocity growth to the actual matter force
Potential-density slip bridge | lensing probes Phi+Psi; velocities probe Phi | define an independent optical comparison rather than reuse density reconstruction
Distance-to-field incremental evidence | L_field|distances is estimator validation | prevent processed fields from becoming a second dataset
Nonlinear continuation threshold | max |delta| or |grad v| where linear inversion fails | identify the measured domain requiring a full evolving solution
''')
seeds('Y2022S10','''
Spectroscopic minimum companion mass | f(M)=P K³(1-e²)^(3/2)/(2pi G_dyn) | derive a lower bound before adding astrometric inclination
Astrometric orbital scale closure | a1/D=alpha1 | combine angular orbit and parallax without double use of Gaia priors
RV-astrometry joint orientation | vlos=K[cos(nu+omega)+e cosomega]+gamma | determine the node and inclination degeneracies
Photocenter versus barycenter orbit | alpha_ph=(B-beta)a_rel/D | account for allowed companion light
Spectral companion luminosity veto | F_comp/F_total<L_max | convert measured non-detection into an astrophysical alternative bound
Eccentric-orbit force residual | r(theta)=p/(1+e costheta) under inverse-square force | derive deviations with the candidate high-acceleration law
Periastron precession sensitivity | Delta omega=integral delta F_R cosnu dt | bound non-Newtonian force derivatives
Gravitational redshift variation | Delta v_gr=Delta Phi/c | derive a phase-dependent spectroscopic metric observable
Transverse-Doppler orbital term | Delta v_TD=v²/(2c) | separate relativistic kinematics from modified gravity
Light-travel orbital delay | Delta t=z_orbit/c | transport timing to emission phase consistently
Parallax-orbit alias covariance | C_varpi,orb from joint design matrix | quantify degeneracy between annual motion and orbital period
Systemic acceleration nuisance | gamma(t)=gamma0+adot_sys t | separate a tertiary or Galactic drift from orbital force
Ground-instrument velocity offsets | v_j=v_model+zp_j | calibrate follow-up spectrographs without overconstraining the orbit
Stellar-template mass uncertainty | M1=f(Teff,logg,Z,L) | expose model dependence in the dark companion mass
Mass function coupling degeneracy | f_obs=G_dyn M2³ sin³i/(M1+M2)² | determine which coupling-mass combination data measure
Dark binary alternative | M_dark=M_a+M_b with quadrupole Q_dark | derive the perturbation signature of an unresolved inner companion pair
Orbital-plane preferred-frame effect | dot L=Torque(alpha1,alpha2,w) | specify a PPN-sensitive secular signature
Galactic natal-kick reconstruction | v_birth=backward_orbit(v_now,Phi_Gal) | separate Galactic-potential uncertainty from binary formation inference
Gaia catalog-selection conditioning | p(orbit|selected) proportional L S_orbit | avoid orbital-detection bias in population extrapolation
RV-only posterior prediction | p(astrometric orbit|RV,parallax) | withhold Gaia orbital parameters as an independent projection test
Astrometry-only phase prediction | p(vlos(t)|astrometry) | validate the reported candidate using genuinely new follow-up data
High-acceleration MONO asymptote | g=g_N+a0 h_mono(g_N/a0) | derive observable corrections without substituting a different interpolation law
Finite-source filtered binary field | DeltaPhi=operator[rho_star+rho_comp] | test point-mass validity at the actual orbital separation
No-light dark-mass interpretation | p(compact|orbit,spectra) | distinguish an empirical dynamical mass from a metric-horizon claim
DR3-to-followup information increment | L_total=L_Gaia L_RV,spectra|Gaia | quantify what the 2022 discovery report adds to the inherited Gaia solution
''')
FRAME='Use a0=(c/2)sqrt(G_N rho_Lambda), with rho_Lambda a mass density and the one-half coefficient adopted unless actually derived. Keep canonical 9.3619e-11 and alternative 1.1279e-10 m/s² separate; retain G_N, G_E, G_bare and G_cosmo separately. Pin the action, matter coupling, source gate, boundary data, xi, S=exp[(xi²/2)Delta] and its adjoint. Operative target is filtered MONO, causality criterion B, thirteen same-action gates; Q/RAR/MU2 are labelled comparisons unless an equivalence is proved. No unannounced particles, halo, per-object a0 or quantum-completion claim.'

OLD_SCOPE={
 'Y2020S05':('AS448/AS449/AS1827','Replace their generic or synthetic network/phase exercises by the measured O3a selection-normalized, final-event likelihood result; explicitly compare alerted and first-catalog events.'),
 'Y2020S06':('AS1827','Resolve the specific short-signal source-generation/propagation rank and its measured window dependence for GW190521, including a burst-reconstruction comparison.'),
 'Y2020S07':('AS448/AS449','Use the measured asymmetric source harmonic support to return a coupled mode/phase constraint unavailable from a generic synthetic network.'),
 'Y2020S08':('AS430','Replace the synthetic mass-sheet fixture by the flexible TDCOSMO hierarchical lens population, jointly propagating aperture kinematics, selection and observed time delays.'),
 'Y2021S07':('AS1794/AS1795','Replace the bounded synthetic source fixture by the 16-year double-pulsar joint timing measurement and retain higher-order light propagation, orbital corrections and full timing covariance.'),
 'Y2021S08':('AS434/AS435/AS436/AS437','Use the full released empirical chance-alignment and error-inflation structure to measure a catalog-calibrated posterior and separation-binned held-out coverage. This adds empirical mixture calibration to the old directional statistic, synthetic-triple fixture, capped covariance sample and assumed orbit library.'),
 'Y2021S04':('AS448/AS1827','Measure the paired old/final-strain processing change on identical O3a data; the output is a correlated update certificate, not another independent dispersion bound.'),
 'Y2022S10':('AS436','Use the measured Gaia BH1 spectroscopic/astrometric orbital cross prediction and companion-light constraint, rather than a normalized velocity covariance exercise.')
}
for year in (2020,2021,2022):
 tasks=[]; src=[]
 for sn in range(1,11):
  sid=f'Y{year}S{sn:02}'; s=S[sid]; k=K[sid]; src.append(s)
  assert len(k['seeds'])==25,(sid,len(k['seeds']))
  for j,(title,eq,target) in enumerate(k['seeds']):
   serial=(sn-1)*25+j+1; tid=f'MY{year}-{serial:03}'
   next_title,next_eq,next_target=k['seeds'][(j+1)%25]
   output=f"{k['short']}: {title}"
   task=dict(id=tid,year=year,source_id=sid,title=output,
    principle=f"The measured {k['short']} observable must be generated by the declared gravitational and matter equations before a fitted residual can test gravity. This work will {target}; its evidential unit is this named output, not a new independent dataset.",
    math=eq+'. This is the proposed target relation/estimand to derive, not an assertion that the source established it or that GR formulae remain valid in the candidate. Define every symbol, units, estimator window and approximation from the authenticated data dictionary; replace any schematic term by its explicit action-derived expression before evaluation.',
    measurement_input=k['inputs']+' Focus on the measured quantities entering '+eq+'. Extract exact values, units, versions and cross-covariance at execution; do not invent unavailable rows or treat a model-conditioned mass/distance/growth posterior as a direct observable.',
    deliverable=f"Deliver {output}: a self-contained derivation of `{eq}`, an observable-space estimator or certified bound that will {target}, a data/likelihood provenance table, uncertainty decomposition, residual or counterexample file, and a stated domain of validity. If the required map or data are unavailable, deliver the precise conditional result and unresolved input list, not a numerical claim or closure pass.",
    steps=[
     f"Authenticate the {s['report_date']} report and the exact {k['short']} data products needed for {title}. Separate measured entries from reference-model deductions, record first-report versus observation dates, and trace shared objects/calibrations through overlap family {s['overlap_family']}.",
     f"Starting from the pinned action and its matter equations, derive the observation map for `{eq}`. {k['bridge']} Carry the projection, normalization, boundary terms and nuisance quantities required to {target}; if the action cannot supply them, state the missing equation explicitly.",
     f"Construct the specific {title.lower()} calculation using the measured input and full covariance. Solve or characterize the target `{eq}` analytically where possible, then specify an auditable numerical procedure with convergence/error bounds only for the parts requiring computation. Keep fixed scale-footing predictions and fitted nuisance diagnostics distinct.",
     f"Challenge {title.lower()} with the negative control below and with {k['independent']}. Show whether the claimed estimator detects the injected violation; compare its covariance or numerical residual to an independently computed representation, and retain failed cases.",
     f"Report the {title.lower()} result in measured units, its valid data/parameter domain and overlap-adjusted information contribution. Relate only the derived implication to the named closure gates, and write the three continuations with exact equations and new required observations. A bounded fit or surviving control is not global thirteen-gate closure."
    ],
    controls=[f"Negative control: {k['negative']}; additionally inject a controlled violation of the defining `{eq}` response and verify that the {title.lower()} diagnostic flags it rather than merely refitting nuisance freedom.",f"Independent control: {k['independent']}. Recompute the target `{eq}` with an independently coded projection, analytic limiting case or withheld measured subset; quantify residuals and shared covariance."],
    first_principles=f"{FRAME} {k['bridge']} For {title.lower()}, explicitly derive `{eq}` or identify it as an observation/statistical definition whose physical prediction still needs derivation. Derive the instrumental/geometric response and all imported GR limits from the selected candidate before empirical application; count independent coefficients and imposed priors.",
    closure_bridge=f"{k['bridge']} The output {title.lower()} supplies only the implication `{eq}` under its listed assumptions. Identify which of the thirteen gates receives new evidence and which remain untouched; matter/clock degrees must be counted separately from two tensor gravitational degrees, and criterion B requires well-posed evolution in one global time. Carry the same parameter cell into any cross-domain comparison.",
    new_information=f"{k['increment']}. The new proposed result is specifically to {target}, quantified by `{eq}`. Relative to the old AS catalog's generic equations, this task adds this release's measured projection, covariance and the named output. It does not claim that the measurement postdates the old catalog or that its mathematical idea is globally novel.",
    overlap_handling=f"Overlap family: {s['overlap_family']}. The 25 tasks using this report are distinct mathematical outputs from shared data, not 25 independent experiments. Build object/epoch/calibration intersections with earlier and later releases; use one joint likelihood or conditional Schur complement C_new|old=C_new-C_no C_old^-1 C_on where Gaussian assumptions hold. Never multiply a summary posterior by the likelihood from which it was made. For {title.lower()}, report the incremental information and exclude inherited observations when claiming a new-data test.",
    continuation=[f"Promising extension: after {title.lower()} survives, connect its actual uncertainty/domain to {next_title.lower()} via `{next_eq}`; the added target is to {next_target}. This requires a new derivation, not a relabeling of the first statistic.",f"Independent bridge: use the derived `{eq}` response to generate a withheld observable through this source's physical bridge: {k['bridge']} Obtain the needed independent measurement and cross-covariance before combining it with {k['short']}.",f"Failed-route repair: if {title.lower()} fails, distinguish a failed `{eq}` physical map from the specific contamination exposed by the negative control ({k['negative']}). Preserve the failing data/mode, derive the smallest source-native correction with all added freedom counted, and repeat the {k['independent']} check. If no repair is justified, retain the obstruction."],
    depends_on=[],priority='P0' if j in (0,1,2,24) else 'P1',kind=('derivation' if j%5==0 else 'audit' if j%5==4 else 'inference' if j%5 in (1,2) else 'computation'))
   if sid in OLD_SCOPE:
    prior,distinction=OLD_SCOPE[sid]
    task['new_information']+=f' Explicit old-catalog overlap: {prior}. {distinction} The task-specific requested new result remains {title.lower()} with `{eq}`; those old tasks are related context, not silently assumed completed dependencies.'
   tasks.append(task)
 assert len(tasks)==250
 assert len({t['title'] for t in tasks})==250
 assert len({t['math'] for t in tasks})==250
 assert len({t['deliverable'] for t in tasks})==250
 (OUT/f'{year}_sources.json').write_text(json.dumps(src,ensure_ascii=False,indent=2)+'\n')
 (OUT/f'{year}_tasks.json').write_text(json.dumps(tasks,ensure_ascii=False,indent=2)+'\n')
 print(year,len(src),len(tasks),'validated authored records')
