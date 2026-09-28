"""Serialize authored measurement work orders; no science calculation is executed.

Every row in PROGRAMS is a distinct proposed observable/estimand, not an assertion
that its anchor paper measured that new quantity. Archive extraction is future work.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCES=[]
CONFIG={}
def source(year, ident, date, title, authors, label, family, program, measurement, focus, epoch='unknown; extract observation dates before execution', access='Primary report accessible; machine-readable data, masks, covariance and likelihood archive contents not inspected. Availability of required ancillary products remains unverified.', version='v1 report; current abstract/submission history inspected, not full likelihood'):
    n=sum(s['year']==year for s in SOURCES)+1
    sid=f'Y{year}S{n:02d}'
    SOURCES.append(dict(source_id=sid,year=year,title=title,authors_or_collaboration=authors,primary_url=f'https://arxiv.org/abs/{ident}',identifier=f'arXiv:{ident}',report_date=date,date_precision='day',date_basis='Initial arXiv measurement-report submission shown by the primary page; later journal publication/revisions do not change the assigned year. Observation dates are separate.',version=version,observation_epoch=epoch,measurement=measurement,data_access=access,verification='Opened primary arXiv abstract page and read initial submission date, title, and reported observable. Full-text equations, tables, archive payloads and likelihood implementation were not audited; tasks require their extraction before numerical claims.',source_locator='Abstract; initial submission line and Submission history; Comments where archive availability is stated',overlap_family=family,search_queries=[f'{label} {year} measurement arxiv',f'https://arxiv.org/abs/{ident}'],checked_on='2026-09-27'))
    CONFIG[sid]=dict(label=label,program=program,focus=focus)

source(2023,'2304.05203','2023-04-11','The Atacama Cosmology Telescope: DR6 Gravitational Lensing Map and Cosmological Parameters','Madhavacheril et al.; ACT','ACT DR6 lensing','ACT-DR6-CMB','cmb_lensing','CMB lensing reconstruction and cosmological inference.','Broad ACT footprint and its lensing reconstruction: derive the response of the measured convergence spectrum to the common-action Weyl potential, excluding external BAO from the anchor-only result.','2017–2021','Comments identify public mass maps/likelihood at NASA LAMBDA and software at GitHub; links present, archive payloads not inspected.','v1 dated 2023-04-11; opened page v2 dated 2024-08-12')
source(2023,'2308.11608','2023-08-22','A Measurement of Gravitational Lensing of the Cosmic Microwave Background Using SPT-3G 2018 Data','Pan et al.; SPT-3G','SPT 2018 lensing','SPT-3G-CMB','cmb_lensing','Temperature-based CMB lensing spectrum.','SPT temperature reconstruction at two observing frequencies: isolate the temperature-foreground-sensitive Weyl response and compare with ACT only using overlap-aware covariance.','2018','Comments identify bandpower and likelihood products at pole.uchicago.edu; archive payloads not inspected.','v1 dated 2023-08-22; opened page v2 dated 2024-01-29')
source(2023,'2305.17173','2023-05-26','DES Y3 + KiDS-1000: Consistent cosmology combining cosmic shear surveys','DES and KiDS collaborations','DES–KiDS hybrid shear','DES-Y3+KiDS','shear','Joint measured cosmic-shear analysis under harmonized modelling.','The hybrid combination is new inference from overlapping pre-existing observations: measure the effect of harmonizing redshift and alignment response on a shared MONO prediction, not another independent survey.','unknown','Primary abstract inspected; hybrid data vectors, common masks and covariance not downloaded.','v1 dated 2023-05-26; opened page v2 dated 2023-10-19')
source(2023,'2306.16217','2023-06-28','The NANOGrav 15-year Data Set: Observations and Timing of 68 Millisecond Pulsars','Agazie et al.; NANOGrav','NANOGrav timing','NANOGrav-15yr','timing','Narrowband and wideband arrival-time measurements and pulsar timing models.','The timing release supports direct clock and orbital residual observables; do not substitute its companion background posterior for these measurements.','unknown','Abstract explicitly describes a public timing data release; arrival-time files and ephemerides not inspected.','v1 dated 2023-06-28')
source(2023,'2306.16213','2023-06-28','The NANOGrav 15-year Data Set: Evidence for a Gravitational-Wave Background','Agazie et al.; NANOGrav','NANOGrav angular correlations','NANOGrav-15yr','pta','Spatially correlated pulsar timing residual evidence for a stochastic background.','Separate the inter-pulsar correlation observable from auto-power and binary-population interpretation; the companion timing report contains the same observing realization.','unknown',version='v1 dated 2023-06-28')
source(2023,'2306.16216','2023-06-28','Searching for the nano-Hertz stochastic gravitational wave background with the Chinese Pulsar Timing Array Data Release I','Xu et al.; CPTA','CPTA DR1 correlations','CPTA-DR1','pta','Correlated signal and angular correlation search using FAST pulsar timing.','The CPTA discrete-frequency correlation measurement has a short-baseline window distinct from NANOGrav; derive its frequency-window-weighted response instead of importing a broadband amplitude.','unknown',version='v1 dated 2023-06-28')
source(2023,'2304.00704','2023-04-03','Hyper Suprime-Cam Year 3 Results: Cosmology from Galaxy Clustering and Weak Lensing with HSC and SDSS using the Emulator Based Halo Model','Miyatake et al.; HSC','HSC Y3 joint clustering','HSC-Y3','joint_lss','Galaxy clustering, galaxy–galaxy lensing and shear joint inference.','The HSC–SDSS joint measurement probes the relation of the dynamical source to light deflection; replace the imported halo emulator by an explicitly derived candidate response or report the missing bridge.','unknown',version='v1 dated 2023-04-03; opened page v3 dated 2023-04-06')
source(2023,'2304.00702','2023-04-03','Hyper Suprime-Cam Year 3 Results: Cosmology from Cosmic Shear Two-point Correlation Functions','Li et al.; HSC','HSC Y3 correlation functions','HSC-Y3','shear','Tomographic real-space cosmic-shear correlations.','Real-space finite angular cuts and broad high-redshift calibration priors define this HSC observation operator; a matched Fourier-space comparison is a correlated representation check.','unknown',version='v1 dated 2023-04-03; opened page v3 dated 2023-11-30')
source(2023,'2304.00701','2023-04-03','Hyper Suprime-Cam Year 3 Results: Cosmology from Cosmic Shear Power Spectra','Dalal et al.; HSC','HSC Y3 shear spectra','HSC-Y3','shear','Tomographic harmonic-space cosmic-shear spectra.','The HSC pseudo-spectrum mask and multipole selection replace real-space cuts: obtain a harmonic-space gravity response and quantify which modes the companion correlation analysis shares.','unknown',version='v1 dated 2023-04-03; opened page v2 dated 2023-04-04')
source(2023,'2311.12098','2023-11-20','Union Through UNITY: Cosmology with 2,000 SNe Using a Unified Bayesian Framework','Rubin et al.','Union3 distances','SN-compilations','supernova','Recalibrated Type Ia supernova compilation and distance inference.','Union3 uses heterogeneous survey photometry and a hierarchical standardization analysis; infer the candidate distance relation while retaining cross-survey calibration and latent populations.','unknown','Abstract states distances, light-curve fits and UNITY framework are released; exact archive payloads not inspected.','v1 dated 2023-11-20; opened page v4 dated 2025-06-20')

source(2024,'2404.03000','2024-04-03','DESI 2024 III: Baryon Acoustic Oscillations from Galaxies and Quasars','DESI Collaboration','DESI DR1 galaxy BAO','DESI-galaxy','bao','Galaxy and quasar acoustic-scale measurements.','First-year tracer-separated acoustic distances: retain reconstruction and reference-cosmology response before interpreting vacuum expansion.','DESI first survey year',version='v1 dated 2024-04-03')
source(2024,'2404.03001','2024-04-03','DESI 2024 IV: Baryon Acoustic Oscillations from the Lyman Alpha Forest','DESI Collaboration','DESI DR1 forest BAO','DESI-forest','forest','Forest absorption auto-correlations and quasar cross-correlations around the acoustic feature.','First-year high-redshift forest distances: infer geometry jointly with continuum projection, absorption bias and quasar redshift errors; do not treat a forest gas field as a galaxy density field.','DESI first survey year',version='v1 dated 2024-04-03; opened page v4 dated 2024-09-27')
source(2024,'2411.12021','2024-11-18','DESI 2024 V: Full-Shape Galaxy Clustering from Galaxies and Quasars','DESI Collaboration','DESI DR1 full shape','DESI-galaxy','clustering','Galaxy power spectra with growth and distance inference.','The broadband and velocity-anisotropy information augments the same first-year BAO sample; isolate the conditional information beyond reconstructed distances.','DESI first survey year','Comments identify public reproduction material and warn of later corrections to data-vector/matrix reporting; pin corrected payload and retain original report date.','v1 dated 2024-11-18; opened page v5 dated 2025-11-24')
source(2024,'2401.02929','2024-01-05','The Dark Energy Survey: Cosmology Results With ~1500 New High-redshift Type Ia Supernovae Using The Full 5-year Dataset','DES Collaboration','DES five-year distances','DES-SN5YR','supernova','Photometrically classified supernova distances with host redshifts.','Photometric classification and host-redshift selection are distinctive DES five-year nuisance channels; obtain a distance result conditional on their response, with external low-redshift calibrators deduplicated.','DES five observing years; exact epochs not extracted','Comments note data links added in v3; those archive files were not inspected.','v1 dated 2024-01-05; opened page v4 dated 2025-07-20')
source(2024,'2402.08458','2024-02-13','The SRG/eROSITA all-sky survey: Cosmology constraints from cluster abundances in the western Galactic hemisphere','Ghirardini et al.','eRASS1 cluster abundance','eRASS1-clusters','clusters','X-ray selected cluster abundance and lensing-calibrated cosmological inference.','eRASS1 count-rate selection and weak-lensing calibration are a coupled measurement: derive a candidate collapse and X-ray observation map before using abundance as a gravity test.','first eROSITA all-sky survey; exact dates not extracted',version='v1 dated 2024-02-13; opened page v2 dated 2024-07-25')
source(2024,'2402.08455','2024-02-13','The SRG/eROSITA All-Sky Survey: Dark Energy Survey Year 3 Weak Gravitational Lensing by eRASS1 selected Galaxy Clusters','Grandis et al.; DES and eROSITA-DE','eRASS1–DES lensing calibration','eRASS1-clusters+DES-Y3','cluster_lensing','Weak shear around X-ray selected clusters and mass calibration.','Cluster member contamination and X-ray centering affect the calibration that feeds the companion abundance result; work in shear space rather than treating its GR mass estimate as a raw mass.','eRASS1 with DES Y3 imaging',version='v1 dated 2024-02-13')
source(2024,'2412.01153','2024-12-02','The MeerKAT Pulsar Timing Array: The first search for gravitational waves with the MeerKAT radio telescope','Miles et al.; MeerKAT PTA','MeerKAT PTA first search','MeerKAT-PTA','pta','Noise-model-dependent spatial correlations in timing residuals.','Closely separated precise pulsars make the MeerKAT correlation evidence sensitive to noise modelling; quantify angular leverage and array-specific nuisance identifiability.','4.5-year baseline reported; exact endpoints not extracted',version='v1 dated 2024-12-02')
source(2024,'2406.03568','2024-06-05','Tests of General Relativity with GW230529: a neutron star merging with a lower mass-gap compact object','Sänger et al.','GW230529 inspiral tests','GW230529','gw_phase','Measured bounds on frequency-dependent inspiral phase deviations.','The long low-mass inspiral probes dipole-like phase structure but shares tidal and chirp-mass degeneracies; translate deviations to the pinned action without importing an extra scalar species.','2023-05-29','Primary phase-deviation report inspected; strain, calibration and posterior payloads not inspected.','v1 dated 2024-06-05; opened page v3 dated 2026-05-13')
source(2024,'2403.02314','2024-03-04','Dark Energy Survey Year 3 results: likelihood-free, simulation-based wCDM inference with neural compression of weak-lensing map statistics','Jeffrey et al.; DES','DES Y3 map statistics','DES-Y3','map_stats','Measured lensing maps analysed with spectra, peaks and neural compression.','Higher-order summaries extract information from existing DES maps; test whether their simulation-trained response is transportable to the actual MONO field, with no independent-data claim.','DES Y3 imaging; exact dates not extracted',version='v1 dated 2024-03-04')
source(2024,'2410.07956','2024-10-10','Constraints on compact objects from the Dark Energy Survey five-year supernova sample','Shah et al.','DES supernova magnification','DES-SN5YR','sn_lensing','Supernova magnitude-distribution constraints on compact lensing matter.','Use the high-magnification distribution of the same DES distance sample to constrain a derived metric lens map; no unrequested compact particle population is introduced.','DES five observing years; exact epochs not extracted',version='v1 dated 2024-10-10; opened page v2 dated 2024-11-20')

source(2025,'2503.14452','2025-03-18','The Atacama Cosmology Telescope: DR6 Power Spectra, Likelihoods and LambdaCDM Parameters','Louis et al.; ACT','ACT DR6 TT TE EE','ACT-DR6-CMB','cmb','Measured CMB temperature and polarization spectra.','ACT primary anisotropies add acoustic and damping information to earlier lens reconstruction from shared maps; compute conditional primary-spectrum information and propagate common calibration.','ACT DR6; exact observing epochs not extracted','Comments identify data at NASA LAMBDA and code at GitHub; links seen, likelihood payload uninspected.','v1 dated 2025-03-18; opened page v2 dated 2025-06-24')
source(2025,'2506.06274','2025-06-06','The Atacama Cosmology Telescope: DR6 Power Spectrum Foreground Model and Validation','Beringue et al.; ACT','ACT DR6 foreground measurements','ACT-DR6-CMB','foreground','Multifrequency foreground fits and measured kinematic SZ constraints.','The foreground report measures emission and velocity-weighted signals from the same ACT spectra; isolate candidate gas and transport predictions conditional on primary anisotropies.','ACT DR6; exact observing epochs not extracted',version='v1 dated 2025-06-06; opened page v2 dated 2025-11-12')
source(2025,'2503.14738','2025-03-18','DESI DR2 Results II: Measurements of Baryon Acoustic Oscillations and Cosmological Constraints','DESI Collaboration','DESI DR2 galaxy BAO','DESI-galaxy','bao','Three-year galaxy/quasar acoustic-distance measurements.','Use the DR2-minus-DR1 conditional acoustic information: new volume and revised reduction must be separated, with common targets and reconstructed modes represented once.','DESI first three survey years',version='v1 dated 2025-03-18; opened page v3 dated 2025-10-09')
source(2025,'2503.14739','2025-03-18','DESI DR2 Results I: Baryon Acoustic Oscillations from the Lyman Alpha Forest','DESI Collaboration','DESI DR2 forest BAO','DESI-forest','forest','Updated absorption/quasar acoustic correlation distances including systematic errors.','The DR2 forest reuses DR1 sightlines while adding spectra and changing absorber handling; measure an incremental high-redshift geometry constraint with the newly reported systematic component retained.','DESI first three survey years',version='v1 dated 2025-03-18; opened page v3 dated 2025-06-30')
source(2025,'2503.19441','2025-03-25','KiDS-Legacy: Cosmological constraints from cosmic shear with the complete Kilo-Degree Survey','Wright et al.; KiDS','KiDS Legacy shear','KiDS-Legacy+KiDS1000','shear','Final-survey cosmic shear with revised redshift calibration.','New area, deeper source selection and revised redshift calibration can move the inferred growth response separately; measure those increments relative to KiDS-1000 without multiplying their likelihoods.','completed KiDS survey; exact dates not extracted',version='v1 dated 2025-03-25; opened page v2 dated 2025-10-21')
source(2025,'2503.19442','2025-03-25','KiDS-Legacy: Consistency of cosmic shear measurements and joint cosmological constraints with external probes','Stölzner et al.; KiDS','KiDS Legacy internal contrasts','KiDS-Legacy+KiDS1000','shear_contrasts','Measured subset consistency and joint-probe shear inference.','Redshift, colour, angle and sky-region splits are correlated contrasts of the final KiDS sample; obtain a physical response contrast rather than reuse the companion total-amplitude inference.','completed KiDS survey; exact dates not extracted',version='v1 dated 2025-03-25; opened page v2 dated 2025-10-20')
source(2025,'2506.20707','2025-06-25','SPT-3G D1: CMB temperature and polarization power spectra and cosmology from 2019 and 2020 observations of the SPT-3G Main field','Camphuis et al.; SPT-3G','SPT-3G D1 spectra','SPT-3G-CMB','cmb','CMB TT, TE and EE measurements from later SPT-3G seasons.','The later SPT seasons add deep polarization information; separate season noise from shared sky covariance and obtain a polarization-led candidate acoustic constraint.','2019–2020',version='v1 dated 2025-06-25; opened page v2 dated 2026-04-01')
source(2025,'2508.18082','2025-08-25','GWTC-4.0: Updating the Gravitational-Wave Transient Catalog with Observations from the First Part of the Fourth LIGO-Virgo-KAGRA Observing Run','LIGO Scientific, Virgo and KAGRA collaborations','GWTC-4 O4a catalog','LVK-GWTC','gw_catalog','New compact-binary candidates and measured source parameters.','Use O4a detections as the incremental event set and carry the catalog selection function; GW230529 and older catalog events enter once, while source parameters remain waveform-dependent.','O4a 2023-05-24–2024-01-16 plus preceding engineering run',version='v1 dated 2025-08-25; opened page v3 dated 2026-06-26')
source(2025,'2509.04348','2025-09-04','GWTC-4.0: Constraints on the Cosmic Expansion Rate and Modified Gravitational-wave Propagation','LIGO Scientific, Virgo and KAGRA collaborations','GWTC-4 propagation','LVK-GWTC','gw_distance','GW distance/redshift population inference and propagation constraints.','The same event catalog supports a luminosity-distance propagation statistic only after population/host modelling; derive damping and selection jointly without treating statistical redshifts as direct observations.','events through O4a; older anchor GW170817 also included in reported combination',version='v1 dated 2025-09-04; opened page v3 dated 2026-08-20')
source(2025,'2509.08099','2025-09-09','Black Hole Spectroscopy and Tests of General Relativity with GW250114','LIGO Scientific, Virgo and KAGRA collaborations','GW250114 spectroscopy','GW250114','ringdown','Measured merger/ringdown mode information and GR consistency tests.','The loud single event supplies mode-resolved strong-field information; derive candidate remnant perturbations before mapping fitted frequencies into action constraints.','2025-01-14 event','Comments link an associated DOI data release; payloads, strain and mode likelihood not inspected.','v1 dated 2025-09-09')

PROGRAMS={}
def program(name,text):
    rows=[line.split('|') for line in text.strip().splitlines() if line.strip()]
    assert len(rows)==25,(name,len(rows))
    assert all(len(x)==4 for x in rows),(name,[x for x in rows if len(x)!=4])
    PROGRAMS[name]=rows

program('cmb_lensing', r'''
Weyl response bandpowers|C_L^kk=integral dchi W_k^2 P_W(L/chi,chi)/chi^2|Weyl transfer band amplitudes with reconstruction response|Set Psi=Phi without varying the action
Filter turnover in projected lensing|R_L(xi)=C_L^kk(xi)/C_L^kk(0)|Projected heat-filter turnover interval|Apply the filter to the final map instead of the source equation
Source-gate transition width|J_L=partial C_L^kk/partial x_gate|Gate-width distinguishability after source occupation marginalization|Replace the occupied source by baryons alone
Radial growth eigenmodes|F_ab=J_La Cov^-1_LLprime J_Lprimeb|Observable redshift eigenfunctions of Weyl growth|Interpret every redshift basis coefficient as independently measured
Geometry versus growth separation|delta ln C_L=K_D delta ln D+K_W delta ln P_W|Distance-free growth residual with a rank certificate|Fix the distance kernel to the preferred cosmology
Reconstruction normalization transport|R_L(theta)=expect[q_L]/phi_L|Candidate-dependent quadratic-estimator normalization map|Use the GR normalization for an altered unlensed spectrum
Curl versus gradient response|C_L^curl,grad=expect[omega_L phi_L*]|Curl/gradient contamination bound tied to scalar response|Treat a nonzero curl residual as MONO evidence
Disconnected bias dependence|N0_L=expect[q_L q_L*]Gaussian|Data-conditioned disconnected-noise correction|Subtract a noise bias from an unrelated spectrum
Connected reconstruction bias|N1_L=integral K_LLprime C_Lprime^phiphi|Self-consistent connected-bias correction|Hold N1 fixed while changing all lensing power
Mask mean-field coupling|m_L=expect[q_L]mask|Residual mask-to-Weyl leakage operator|Set the mean field to zero under an anisotropic mask
Foreground trispectrum direction|Delta C_L=T_fg contracted with Q_L Q_L*|Worst foreground-connected bias on gate response|Model foregrounds as Gaussian solely because their power is known
Frequency response contrast|Delta C_L=C_L^(nu1)-C_L^(nu2)|Achromatic lensing contrast after bandpass response|Attribute a frequency-dependent residual directly to gravity
Calibration-lensing degeneracy|delta ln C_L=J_g delta ln gain+J_W delta W|Gain-orthogonal Weyl mode|Treat map calibration as independent for every bandpower
Beam transfer curvature|B_l=exp[-l(l+1)sigma_b^2/2]|Beam-curvature projection onto the filter scale|Drop beam uncertainty at high multipole
Low-L boundary response|delta phi_L=G_L delta boundary|Large-scale boundary-condition sensitivity certificate|Periodize a finite footprint without measuring leakage
Nonlinear source correction|P_W=P_W,lin+Delta P_W,nonlin|Controlled nonlinear correction over released L bins|Import a dark-matter fitting function as a MONO prediction
Baryon rearrangement cancellation|integral d^3x delta rho_b=0|Mass-conserving baryon response envelope|Change baryon mass while calling it feedback redistribution
Matter-Weyl decorrelation|r_Wb=P_Wb/sqrt(P_W P_b)|Allowed decorrelation function requiring independent tracers|Assume perfect correlation from equal power amplitudes
Gaussian covariance failure|Cov=Cov_G+T_connected/area|Connected covariance impact on gate uncertainty|Rescale covariance only by sky fraction
Super-survey response|Cov_SSC=partial C/partial delta_b S partial C/partial delta_b|Separate-universe response conditional on candidate background|Set the background perturbation response to the GR value
Shared-map conditional information|C_cond=C_new-C_new,old C_old^-1 C_old,new|Incremental lensing information versus related maps|Multiply likelihoods made from the same CMB realization
Post-Born projection correction|kappa=kappa_Born+delta kappa_path|Path-deflection correction to selected bandpowers|Call the Born approximation exact in strong projected structures
Vacuum-density response|partial ln C_L/partial ln rho_Lambda=(1/2)partial ln C_L/partial ln a0+geometry terms|Vacuum-linked lensing response with both scale footings|Change a0 while holding its declared vacuum identity inconsistent
Potential-slip null combination|W=(Phi+Psi)/2; eta=Psi/Phi|Observable slip functional conditional on dynamical information|Interpret lensing alone as measuring both potentials separately
Nonparametric compatibility witness|min_theta (d-F(theta))^T Cov^-1(d-F(theta))|Finite measured-bin residual certificate for the pinned action|Tune one acceleration scale per multipole bin
''')
program('shear', r'''
Tomographic Weyl overlap|C_l^ij=integral W_i W_j P_W/chi^2 dchi|Bin-pair Weyl-response matrix|Use a GR matter spectrum as a measured Weyl spectrum
Redshift-tail transport|delta C_l=integral (delta W_i W_j+W_i delta W_j)P_W/chi^2|High-redshift tail induced gravity-bias bound|Shift only the mean of a multimodal source distribution
Multiplicative shear common mode|C_obs^ij=(1+m_i)(1+m_j)C^ij|Calibration-orthogonal growth combination|Allow unconstrained independent calibration in each angular bin
Additive PSF direction|xi_obs=xi_grav+alpha^2 xi_PSF+2alpha xi_cross|PSF leakage projection on the MONO response|Assign PSF-correlated power to a physical potential
Intrinsic alignment cross term|C_obs=C_GG+C_GI+C_IG+C_II|Gravity/shape-alignment separation with explicit response|Drop GI while retaining II
Finite-angle E/B separation|E_n=integral theta dtheta[Tplus_n xi_plus+Tminus_n xi_minus]/2|Finite-support E-mode response coefficients|Use an infinite-angle inversion on truncated measurements
Pseudo-spectrum mixing|C_tilde=M C+N|Mask-deconvolved candidate shear operator|Invert only the diagonal of the mixing matrix
Reduced-shear correction|g=gamma/(1-kappa)|Leading reduced-shear MONO correction to selected bins|Equate observed ellipticity with gamma at arbitrary convergence
Magnification-selected sources|n_obs=n0 mu^(2.5s-1)|Selection-induced change of the lensing kernel|Hold source density independent of foreground convergence
Source-lens clustering|expect[n_s gamma gamma] differs from expect[n_s]expect[gamma gamma]|Source-clustering correction to tomography|Randomize source redshifts while preserving claimed signal
Heat-filter angular scale|k_xi=1/xi; ell_xi(chi)=chi/xi|Observable filter-knee smearing across source bins|Use one angular cutoff for every lens distance
Gate-occupation response|delta C=integral W_i W_j delta P_W,gate/chi^2|Occupied-carrier gate sensitivity under source selection|Apply the baryon-only radial law to occupied environments
Baryonic redistribution moment|delta P(k)=O(k^2) for conserved localized mass rearrangements|Conservation-limited feedback nuisance basis|Permit constant large-scale mass creation as feedback
Distance-growth degeneracy|J=[partial C/partial D,partial C/partial P_W]|Rank-resolved geometry/growth subspace|Use a distance prior twice via calibration and cosmology
Non-Limber large-angle residual|C_l=4pi integral dlnk P_R Delta_l^i Delta_l^j|Exact-projection correction envelope|Take ell to infinity on the largest released angles
Unequal-time lensing kernel|C_l=integral dchi dchi' K_l P_W(k;chi,chi')|Unequal-time covariance bound|Set unequal-time correlation to unity by definition
Small-scale closure domain|epsilon_l=norm(F_full-F_truncated)/sigma_l|Certified retained angular domain for candidate response|Choose cuts after observing favorable residuals
Super-sample response|Cov_SSC=R_i S R_j|Footprint-dependent background-mode covariance|Treat disjoint source bins as disjoint sky volumes
Photo-z and alignment coupling|Cov(n_i,A_i) enters Cov(C)|Joint redshift/alignment bias contour|Factor correlated population calibrations
Cross-survey calibration cancellation|u^T J_cal=0; u^T J_grav nonzero|Shared-calibration-null shear contrast|Count overlapping calibration fields twice
Canonical versus alternative scale|Delta d=F(a0_alt)-F(a0_can)|Observable two-footing discrimination vector|Blend both normalizations into one fitted acceleration
Vacuum-evolution functional|delta ln a0(z)=0.5 delta ln rho_Lambda(z)|Shear-weighted vacuum-evolution sensitivity|Assume dynamical dark energy follows the identity without declaring an extension
Shear likelihood transport|L_new(d)=L(d;F_action,C_action)|Measured-vector likelihood stripped of imported GR posterior priors|Reweight an S8 posterior as if it were raw shear
Representation common information|Cov(xi,C_l)=H Cov(C_l) with finite windows|Matched-window real/harmonic information comparison|Multiply two representations of the same galaxies
Slip-sensitive external bridge|E_G proportional to lensing/(velocity divergence)|Conditional lensing–dynamics contrast with matching redshift weights|Claim no slip from shear amplitude alone
''')
program('joint_lss', r'''
Lensing-clustering source ratio|R(R)=DeltaSigma(R)/w_p(R)|Bias-cancelled source-response curve|Cancel bias without matching radial kernels
Velocity-lensing closure|E_G=laplacian(Phi+Psi)/(3H0^2 a^-1 theta)|Action-derived gravity consistency statistic|Insert the GR velocity law into a MONO test
Luminosity-dependent occupancy|n_g=integral n(M)N_g(M,Lcut)dM|Occupancy response for actual lens selection|Treat luminosity as a direct baryonic mass measurement
Satellite fraction response|P_gg=P_cc+2P_cs+P_ss|Satellite contamination of the inferred gate transition|Set all lenses at halo centers
Off-centering convolution|DeltaSigma_off=integral p(Roff)DeltaSigma_centered dRoff|Metric-profile offset kernel|Correct offsets after fitting a physical radius
Projected clustering depth|w_p(R)=2 integral_0^pimax xi(R,pi)dpi|Finite-depth velocity leakage correction|Replace finite projection with an infinite integral
Small-scale bias expansion|delta_g=b1 delta+b2(delta^2-variance)/2+bs s^2|Candidate-derived bias validity scale|Import GR bias coefficients as fixed microphysics
Halo emulator domain|epsilon(theta)=F_action-F_emulator|Observed-bin emulator transport discrepancy certificate|Call extrapolation beyond training range a validated prediction
Single-source photo-z leverage|partial DeltaSigma/partial nz versus partial xi/partial nz|Joint redshift identifiability rank|Use the same source-redshift prior as independent in both probes
Mass-sheet invariance|kappa'=lambda kappa+1-lambda; gamma'=lambda gamma|Unobservable source modes of joint data vector|Claim absolute potential normalization from shear alone
Galaxy stochasticity|P_gg=b^2P+P_epsilon|Stochastic-bias floor on source-ratio inference|Subtract Poisson noise as exact for all samples
Nonlinear cross-correlation|r_gW=P_gW/sqrt(P_gg P_WW)|Measured admissible correlation-coefficient band|Force r_gW=1 below nonlinear scales
Baryon-profile gate response|g_bar(r)=G_N M_b(<r)/r^2|Gate radius posterior conditional on measured baryon profiles|Infer baryons solely from a fitted dark halo
Assembly selection|P(N_g,env given M) differs from P(N_g given M)|Environment-dependent response bound|Randomize environment and call the result physical
Compensated lensing observable|Upsilon(R)=DeltaSigma(R)-(R0/R)^2DeltaSigma(R0)|Inner-profile-insensitive metric constraint|Ignore covariance of the common inner anchor
Redshift-bin cross covariance|Cov(d_i,d_j)=window overlap times connected response|Shared-source cross-bin covariance|Assume spectroscopic lens bins eliminate common source noise
Distance convention transport|R=D_A theta; DeltaSigma=Sigma_crit gamma_t|Reference-distance Jacobian|Refit distances without rescaling transverse radii
Source magnification correction|delta n_s=(5s-2)kappa|Lens-dependent source selection correction|Use random-source density measured away from all lenses
Shear-clustering consistency modes|v^T J_nuis=0|Data combinations isolating action mismatch|Select v after looking at residual sign
Large-scale recovery window|F_action/F_GR tends to 1 with derived conditions|Measured domain of high-acceleration recovery|Infer acceleration solely from Fourier wavelength
Vacuum-density conditional mode|J_rho=partial F/partial rho_Lambda|Joint vacuum-scale score after bias marginalization|Allow a0 and rho_Lambda to vary independently on fixed footing
Time-evolving occupation|partial_t N_g+transport terms=source-sink|Redshift evolution residual requiring formation physics|Interpret changing sample luminosity cuts as gravity evolution
Three-probe information gain|I_extra=I_joint-I_shear conditioned on covariance|Independent clustering contribution to MONO bounds|Add marginal Fisher matrices sharing galaxies
Source profile nonuniqueness|F[rho1]=F[rho2] on measured bins|Constructive profile degeneracy with positivity constraints|Certify a unique carrier profile from one best fit
Common-action residual intersection|intersection_i {theta: residual_i acceptable}|One parameter cell compatible with all three observables|Choose different kernels for lensing and clustering
''')
program('timing', r'''
Clock response to potential|delta nu/nu=delta Phi/c^2 plus endpoint and velocity terms|Pulsar timing clock-response operator|Retain only a potential at one endpoint
Timing-model projection|r=P_perp delta t; P_perp=I-M(M^T N^-1 M)^-1M^T N^-1|Gravity modes erased by fitted timing parameters|Search a mode already removed by spin fitting
Galactic acceleration residual|Pdot_obs/P=a_los/c+mu^2 d/c+Pdot_int/P|Line-of-sight acceleration estimator with nuisance hierarchy|Set intrinsic spin-down to zero
Binary orbital acceleration|Pbdot_obs=Pbdot_int+P_b a_los/c+Shklovskii|Binary acceleration consistency map|Treat kinematic period drift as radiation reaction
Shapiro propagation delay|Delta t=-(1/c^3)integral(Phi+Psi)dl|Derived timing delay kernel|Set both potentials equal without field equations
Annual parallax covariance|Delta t_par proportional to r_Earth_perp^2/(2cd)|Parallax–gravity degeneracy bound|Fix distance from a posterior using the same timing data
Proper-motion geometric drift|a_Shk=mu^2 d|Uncertainty-corrected acceleration floor|Replace expect[mu^2] by expect[mu]^2
Frequency-dependent dispersion|Delta t_DM=K DM/nu^2|Achromatic residual after dispersion projection|Call a nu^-2 residual a gravitational clock shift
Solar plasma seasonal mode|DM_solar=integral n_e dl|Solar-angle contamination bound on annual gravity modes|Assume solar-wind column is time independent
Backend phase jumps|r=r_phys+J b|Backend-invariant low-frequency response|Fit jumps independently at every observing epoch
Wideband-narrowband comparison|Delta r=r_wide-r_narrow; Cov includes shared photons|Reduction-dependent bias of acceleration estimands|Treat both reductions as independent data
Red timing noise curvature|S_r(f)=A^2(f/f0)^-gamma|Acceleration uncertainty after red-noise marginalization|Estimate secular gravity with white noise only
Ephemeris dipole projection|delta t_p=n_p dot delta r_SSB/c|Solar-system position error separated from gravity|Assign a dipole sky pattern to an isotropic background
Clock monopole projection|r_p(t)=s_clock(t)+s_p(t)|Shared-clock component and gravitational degeneracy|Count a common observatory clock twice
Binary inclination identifiability|mass function=(m_c sin i)^3/(m_p+m_c)^2|Inclination-conditioned timing-mass map|Equate timing mass posterior with theory-free mass
Periastron advance residual|omega_dot=omega_dot_action+omega_dot_kin|High-acceleration precession correction|Use the GR mass inference unchanged in the correction
Orbital eccentricity forcing|e_dot=F_action(e,g_ext,orientation)|Preferred-frame or external-field eccentricity response|Average orientation before computing the signal
Time-varying Newton coupling|Pbdot/P_b=K_G Gdot_N/G_N+other terms|Coupling-drift bound after stellar sensitivities are derived|Identify G_bare with the measured orbital coupling
Pulse profile evolution|TOA_bias=argmax correlation(template,profile(t))|Profile-evolution timing bias envelope|Assume a fixed template has no secular bias
Irregular-cadence spectral mixing|W(f,f')=sum_i w_i exp[2pi i(f-f')t_i]|Cadence-resolved response to a predicted metric transient|Use evenly sampled Fourier orthogonality
Event-like potential crossing|delta t(t)=integral delta nu(t)/nu dt|Template family for a derived localized carrier perturbation|Insert an arbitrary acceleration pulse unrelated to the action
Gravitational memory timing step|r(t)=B h_mem (t-t0)Theta(t-t0)|Projected tensor-memory response bound|Ignore timing-fit removal of the ramp
Vacuum-scale acceleration projection|a_los=hat n dot grad Phi[a0(rho_Lambda)]|Vacuum-linked Galactic timing response|Fit a separate a0 for each pulsar
Pulsar distance latent covariance|Cov(a_los)=J_d Cov(d) J_d^T|Distance-induced correlated acceleration uncertainty|Set distance and proper motion independent without evidence
Common-pulsar incremental baseline|L_new=L(all TOAs)/L(shared TOAs) only with joint noise|Information added by new timing epochs|Multiply releases containing identical arrival times
''')
program('pta', r'''
Tensor angular response|Gamma_ab(f)=integral dOmega F_a^A F_b^A* P_phase|Action-derived tensor overlap kernel|Assume the Hellings–Downs curve before deriving propagation
Clock-monopole separation|C_ab=S_h Gamma_ab+S_clock|Monopole-orthogonal tensor amplitude|Interpret any common red process as a tensor background
Ephemeris-dipole separation|C_ab includes n_a^i E_ij n_b^j|Dipole-orthogonal correlation statistic|Omit barycentric ephemeris uncertainty
Finite-distance pulsar terms|F_a includes 1-exp[-2pi if L_a(1+mu)/c]|Distance-dependent angular response|Drop pulsar terms uniformly near aligned sightlines
Short-baseline frequency window|C_obs(f)=integral W_T(f,f')C(f')df'|Window-corrected spectral curvature|Replace a measured narrow frequency response by a broadband amplitude
Irregular cadence pair weights|Gamma_eff=sum_ab W_ab Gamma_ab|Effective measured angular kernel|Use unweighted sky-pair counts
Close-pair leverage|h_ab=partial statistic/partial C_ab|Influence bound for near-coincident high-precision pulsars|Treat redundant angular pairs as independent modes
Common versus correlated power|S_auto=S_common+S_intrinsic; S_cross=Gamma S_tensor|Identified correlated-power fraction|Use auto-spectrum significance as angular-correlation significance
Noise-model mixture|p(S_h given d)=sum_m p(S_h given d,m)p(m given d)|Robust correlation interval over admissible noise models|Select only the noise model maximizing evidence
Chromatic covariance leakage|C_DM proportional to nu_a^-2 nu_b^-2|Achromatic correlation after dispersion marginalization|Fit dispersion independently despite shared plasma structures
Angular multipole content|Gamma(theta)=sum_l (2l+1)C_l P_l(cos theta)|Recoverable angular multipoles with mask resolution|Interpret a truncated angular fit as a complete sky spectrum
Anisotropy-response coupling|C_ab=integral I(Omega)F_a F_b* dOmega|Anisotropic tensor-intensity constraints|Infer isotropy from an isotropic-template fit alone
Circular polarization response|C_ab=I Gamma_I+iV Gamma_V|Parity-odd correlation sensitivity requiring derived tensor states|Introduce an extra polarization to fit a residual
Tensor speed phase response|phase=2pi f L(1+hat k dot n c/c_T)/c|Frequency-dependent tensor-speed response|Enforce a metric-cone test in place of criterion B
Dispersion without extra modes|omega^2=c_T^2 k^2+Delta_action(k)|Two-mode dispersive overlap correction|Use a massive-particle formula absent from the action
Timing-fit suppression|C_post=P_a C_pre P_b^T|Low-frequency transfer after spin and astrometry fitting|Compare unprojected theoretical power with fitted residuals
Finite-source non-Gaussianity|kappa4(r) differs from zero for few binaries|Fourth-cumulant discriminator of background realization|Assume Gaussianity because two-point fit succeeds
Environmental spectral turnover|df/dt=df_GW/dt+df_env/dt|Turnover degeneracy between source evolution and propagation|Attribute all spectral curvature to modified gravity
Energy-density conversion|rho_GW=derived tensor Hamiltonian averaged over modes|Strain-to-energy conversion for the measured band|Use the GR tensor normalization without deriving it
Cross-array shared pulsars|C_joint has common pulsar and clock blocks|Incremental array information with duplicate TOAs removed|Multiply PTA posteriors as independent
Time-stationarity contrast|C(t,t')=C(t-t')+Delta_nonstationary|Data-supported nonstationary tensor residual bound|Average away a coherent transient before testing it
Burst contamination|r=r_background+sum_k r_burst,k|Background-amplitude bias from sparse transients|Force every outlying residual into a power law
Solar-system gravitational bridge|delta t=integral(Phi+Psi)dl/c^3|Local-propagation contamination from the same metric|Insert a phenomenological Shapiro coefficient independent of the action
Vacuum-linked tensor damping|h''+(2H+nu_action)h'+c_T^2 k^2h=0|Conditional rho_Lambda response of the correlation spectrum|Infer rho_Lambda from strain without source-population assumptions
Positive covariance compatibility|C_action(theta) positive semidefinite on actual pulsars|Measured-array admissibility domain of candidate kernels|Accept an indefinite overlap covariance because its diagonal is positive
''')
program('supernova', r'''
Distance-modulus action map|mu=5log10(D_L/10pc)|Candidate luminosity-distance residual curve|Import a LambdaCDM distance posterior as raw photometry
Absolute-scale null space|m=M+5log10(D_L); M-H0 degeneracy|Uncalibrated distance combinations identifiable from this sample|Claim an absolute Hubble scale without a calibrator
Curvature-distance consistency|D_M=S_K(integral c dz/H)|Curvature-expansion degeneracy with finite redshift support|Set spatial curvature to zero as an observed fact
Vacuum-evolution reconstruction|rho_eff(z) from action-derived Friedmann equation|Distance-supported vacuum-density functional|Use the GR Friedmann equation as the candidate field equation
Acceleration-scale prediction|a0(z)=c sqrt(G_N rho_Lambda(z))/2|Conditional redshift-dependent MONO scale interval|Treat a fitted dark-energy equation of state as a derivation of the identity
Photometric classifier mixture|p(m)=p_Ia p_Ia(m)+(1-p_Ia)p_nonIa(m)|Classification-induced distance-bias envelope|Set all class probabilities to unity
Colour-luminosity transport|m_corr=m+alpha x1-beta c|Gravity residual orthogonal to colour standardization|Keep beta fixed when population colour changes
Host-population step|Delta M=gamma_H H(Mhost-Mcut)|Host-dependent residual with uncertain stellar mass|Declare the host step a universal gravity signal
Selection-normalized likelihood|p(d given detected)=p(d)S(d)/integral p(d)S(d)dd|Truncation-corrected distance likelihood|Omit the detection normalization
Survey calibration low-rank modes|Cov_cal=J_zp Cov_zp J_zp^T|Zero-point-orthogonal distance curvature|Treat shared standards as independent calibrations
Rest-frame spectral transport|F_obs(lambda)=L(lambda/(1+z))/(4pi D_L^2(1+z))|K-correction response to wavelength calibration|Shift wavelength labels without redshift Jacobians
Peculiar-velocity covariance|delta mu=(5/ln10) v_los/(cz) at low z|Low-redshift correlated-velocity correction|Count coherent flows as independent object noise
Lensing mean-flux conservation|expect[mu_lens]=1 under complete flux sampling|Selection-corrected mean magnification bias|Set mean magnitude shift to zero from mean-flux conservation
Intrinsic-scatter non-Gaussianity|p(residual)=convolution(p_intrinsic,p_lensing)|Tail-robust distance estimate|Force intrinsic scatter to absorb any redshift trend
Light-curve time dilation|t_rest=t_obs/(1+z)|Duration-distance consistency after selection|Fit rest-frame time using a cosmology-dependent redshift
Redshift-error nonlinear bias|expect[f(z)]-f(expect[z])=f'' Var(z)/2+...|Second-order redshift-bias bound|Evaluate distances only at mean redshift
Dust versus grey opacity|F=F0 exp[-tau(lambda,z)]|Chromaticity-conditioned opacity bound|Interpret dimming as expansion without opacity sensitivity
Distance duality test|eta=D_L/[(1+z)^2 D_A]|Conditional photon-conservation residual with external distances|Reuse a BAO distance calibrated by the same SN sample
Population-drift identifiability|J=[partial mu/partial cosmology,partial M/partial z]|Rank test separating luminosity evolution from expansion|Allow arbitrary M(z) then report a unique expansion history
Leave-survey-out transport|Delta mu_s=mu_all-mu_without_s|Survey-specific influence on vacuum inference|Treat leave-one-survey fits as independent measurements
Common-supernova release increment|C_delta=C_new+C_old-C_cross-C_cross^T|Information gained from recalibration versus new objects|Multiply compilations with repeated supernovae
Binned compression sufficiency|score_full minus E[score_full given bins]|Lost candidate-response information under binning|Assume published bins suffice for every gravity theory
Anchor-cosmology feedback|J_anchor=partial Mcal/partial theta_action|Calibration feedback on absolute expansion scale|Use a gravity-dependent stellar anchor as external truth
Jerk-sensitive distance combination|D_L=z c/H0[1+(1-q0)z/2+...]|Finite-redshift jerk functional with truncation bound|Extend a low-z series beyond its controlled domain
One-cell expansion compatibility|chi2(theta)=r^T C^-1 r with a0 tied to rho_Lambda|Shared-footing distance compatibility certificate|Retune the vacuum magnitude independently for each redshift bin
''')
program('bao', r'''
Anisotropic acoustic dilation|alpha_perp=(D_M/rd)/(D_M/rd)_fid; alpha_par=(D_H/rd)/(D_H/rd)_fid|Candidate transverse/radial distance map|Treat fitted dilation parameters as absolute distances
Sound-horizon calibration|rd=integral_zd^infinity cs(z)/H(z) dz|Action-derived acoustic-ruler calibration obligation|Import Planck rd as a measured theory-free length
Alcock–Paczynski ruler cancellation|F_AP=D_M H/c|Ruler-free anisotropy constraint|Use isotropic D_V alone to claim anisotropic geometry
Isotropic versus anisotropic information|D_V=[z D_M^2 D_H]^(1/3)|Information discarded by isotropic compression|Treat D_V and its parent anisotropic vector as independent
Reconstruction displacement response|s(k)=-ik delta(k)S(k)/(b k^2)|Candidate-dependent reconstruction shift|Assume the GR displacement field is exact under altered growth
Acoustic phase preservation|P_w(k)=A(k)sin[k rd+phi(k)]|Nonlinear phase shift induced by derived MONO growth|Absorb arbitrary oscillatory phase into a smooth broadband
Tracer-relative dilation|Delta alpha=alpha_LRG-alpha_ELG with cross covariance|Same-redshift tracer geometry contrast|Compare different effective redshifts without matching kernels
Quasar redshift smearing|P_obs(k,mu)=P(k,mu)exp[-k^2 mu^2 sigma_r^2]|Radial acoustic bias from redshift-error tails|Model all quasar redshift errors as a fixed Gaussian
Bright-sample local geometry|D_M(z) and D_H(z) integrated over low-z selection|Low-redshift vacuum response with velocity covariance|Neglect coherent velocities in the nearest tracer
Wide-redshift effective averaging|alpha_eff not generally alpha(z_eff)|Bias from finite-bin expansion curvature|Evaluate every object at a single effective redshift
Window-convolved acoustic response|P_obs_i=sum_j W_ij P_j|Survey-window transport of candidate oscillations|Apply the window to residuals after likelihood evaluation
Fiber assignment anisotropy|xi_obs=xi_true+Delta_xi_fiber|Acoustic shift from angular incompleteness|Set missing-pair probability equal to single-target completeness
Redshift-success selection|n_obs(z)=n(z)p_success(z,features)|Selection-induced acoustic distortion bound|Assume redshift failures are random in density
Broadband nuisance projection|P_perp=I-B(B^T C^-1B)^-1B^T C^-1|Oscillatory response retained after nuisance marginalization|Allow a nuisance basis containing the signal itself
Damping-growth degeneracy|P_w damped by exp[-k^2 Sigma^2(mu)/2]|Acoustic damping response to candidate transport|Interpret damping width as a distance shift
Transverse-radial covariance rotation|Cov_logD=J Cov_alpha J^T|Principal distance combinations for vacuum inference|Discard off-diagonal dilation covariance
Acoustic detection null|Delta chi2=chi2_no_wiggle-chi2_wiggle|Detection-calibrated geometry likelihood domain|Quote distances where the ruler is not identified
Reference cosmology transport|k_true=k_fid q(alpha_perp,alpha_par)|Fiducial-coordinate iteration error certificate|Change H(z) but keep the reference-coordinate Jacobian fixed
Curvature integral consistency|D_M=S_K(chi); chi'=D_H|Discrete curvature consistency residual|Differentiate noisy distance bins without covariance
Vacuum density finite differences|H^2(z)-source_action(z)=vacuum_action(z)|Conditional vacuum-evolution contrasts|Use a GR source term without deriving candidate cosmology
Two-footing distance prediction|rho_Lambda=4a0^2/(G_N c^2)|Distinct canonical/alternative distance trajectories|Mix scale normalization with a single fixed density
DR1–DR2 conditional improvement|C_2given1=C22-C21 C11^-1 C12|New-volume acoustic information after common modes removed|Treat the two releases as independent surveys
Tracer-combination redundancy|F_comb versus sum F_tracer with overlap blocks|Effective independent ruler count|Count cross-correlations as independent of both auto-correlations
BAO–SN relative-scale bridge|D_L=(1+z)D_M with photon conservation|Relative ruler/candle compatibility curve|Calibrate both probes with the same H0 prior twice
Shared-action distance envelope|min_theta distance residual under all fixed gate parameters|Action-specific expansion admissibility region|Fit arbitrary H(z) and call it the action prediction
''')
program('forest', r'''
Absorption-to-metric map|delta_F=b_delta delta+b_eta eta_v+nonlinear terms|Candidate-derived forest bias and velocity response|Identify absorption contrast with mass density
Auto versus cross geometry|xi_FF and xi_Fq share alpha_perp,alpha_par|Joint acoustic geometry with distinct bias amplitudes|Fit separate geometry to force each correlation to pass
Continuum projection kernel|delta_Fobs=P_cont delta_Ftrue|Acoustic mode loss from continuum fitting|Set the continuum projector to identity
Quasar redshift-offset asymmetry|xi_Fq(rpar)=xi0(rpar-Delta_r)|Odd cross-correlation displacement estimator|Attribute redshift calibration offsets to gravitational slip
Metal-line displaced correlations|rpar_metal from lambda_rest ratios|Metal-template projection onto the acoustic peak|Treat metal absorption as featureless noise
Damped-absorber masking response|xi_obs=W_DLA[xi_FF]|Acoustic shift from absorber selection and wings|Delete absorbers without adjusting the survey response
Sky-subtraction angular mode|delta_F includes s(lambda_obs,plate)|Observed-wavelength contamination null space|Interpret an instrumental wavelength feature as a comoving ruler
Resolution-window deconvolution|P_obs=P_F abs(R(kpar))^2+N|Line-spread response error on radial geometry|Use a constant resolution for heterogeneous spectra
Pixel-noise heteroscedasticity|Cov_FF depends on sigma_pixel(lambda)^2|Noise-weighted acoustic estimator with flux dependence|Assign identical noise to every forest pixel
Mean-transmission evolution|Fbar(z)=exp[-tau_eff(z)]|Transmission-evolution-induced distance bias|Freeze the mean flux across the whole sample
Thermal smoothing versus gravity filter|P_F includes exp[-kpar^2 b_th^2] times source response|Separability of gas temperature and heat-filter scale|Equate thermal line broadening with the MONO filter
Pressure smoothing transverse response|P_gas(k)=T_pressure(k)^2 P_source(k)|Gas-pressure nuisance envelope for acoustic geometry|Ignore transverse smoothing because spectra are one-dimensional
Ionizing-background correlations|delta_F includes b_Gamma delta_Gamma|Radiation-background contamination of large-scale correlations|Assign all long-range absorption correlations to matter
Velocity-gradient nonlinear response|tau proportional to n_HI/(H+dvpar/drpar)|Controlled redshift-space mapping before shell crossing|Linearize through a zero velocity-gradient denominator
Forest length integral constraint|sum_pixels w delta_F=0 on fitted modes|Finite-sightline correction to correlation monopole|Use unrestricted periodic forest modes
Cross-bin continuum covariance|Cov_ij includes shared fitted continua|Redshift-bin covariance from common quasars|Treat disjoint pixel-redshift bins as independent quasars
Broad absorption selection|p_keep depends on quasar spectral features|Selection-conditioned acoustic estimator|Assume removed quasars trace the same environment unconditionally
Anisotropic BAO systematic floor|Cov_total=Cov_stat+Cov_shift|Theory-shift uncertainty propagated to vacuum evolution|Reduce a published systematic component as extra sample size grows
High-redshift expansion anchor|D_H=c/H; D_M=integral geometry|Action-specific high-z distance functional|Extrapolate local MOND force directly into H(z)
Acoustic-ruler early-time bridge|rd=integral cs/H dz|Early-universe ruler prerequisite for forest geometry|Use a fitted rd to claim parameter-free acceleration-scale prediction
DR2 incremental sightline information|I_new=I_joint-I_DR1 with shared continua|New-sightline versus reprocessing information split|Count re-extracted old spectra as new independent observations
Angular calibration anisotropy|xi(r,mu)=sum_l xi_l(r)P_l(mu)|Calibration-induced quadrupole bound|Take any quadrupole as a redshift-space gravitational effect
Rest-wavelength standard uncertainty|delta rpar=(c/H)delta lambda/lambda|Wavelength-scale floor on radial distance|Treat laboratory wavelength uncertainty as zero by convention
Gas conservation compatibility|partial_t rho_g+div(rho_g v_g)=sources|Absorption prediction respecting ordinary-matter conservation|Add unaccounted gas sources to fit the mean transmission
Vacuum-linked forest residual|a0(z)=c sqrt(G_N rho_Lambda(z))/2 in derived gas dynamics|Coupled geometry/gas residual for one parameter cell|Use different vacuum histories for absorption and distance
''')
program('clustering', r'''
Redshift-space action map|s=x+vpar/(aH)n|Derived density-velocity observation operator|Import Kaiser growth without deriving the Euler equation
Multipole velocity decomposition|P_s(k,mu)=P_dd+2mu^2P_dtheta+mu^4P_thetatheta|Density/velocity spectra constrained by measured multipoles|Set all three spectra proportional before testing the theory
Scale-dependent growth score|f(k,a)=partial ln D(k,a)/partial ln a|Measured growth-shape response to the heat filter|Compress scale-dependent growth into one f sigma8 without checking loss
Bias-gravity degeneracy|J=[partial P/partial b1,partial P/partial gate]|Identifiable gate component after tracer bias projection|Fix tracer bias using the same candidate residual
Effective-stress correction|P_ct=-2 c_s2 k^2 P_lin|Candidate-allowed effective-stress envelope|Use a nuisance counterterm to cancel arbitrary oscillations
Finger-of-God moment expansion|D_FoG=1-kpar^2 sigma_v^2/2+...|Velocity-tail truncation error on growth inference|Use a Gaussian damping law as an exact theorem
Alcock–Paczynski multipole mixing|P_lobs=sum_lprime M_llprime(alpha)P_lprime|Geometry-growth mixing matrix|Fit geometry after fixing the growth anisotropy
Window-coupled multipoles|P_lobs(k)=sum_lprime integral W_llprime P_lprime|Survey-window likelihood for candidate spectra|Apply only a scalar window to all multipoles
Integral-constraint offset|delta_obs=delta-delta_window|Large-scale missing-mode response|Interpret the enforced zero survey mean as a physical homogeneous constraint
Shot-noise non-Poisson moment|P_epsilon=P0+P2 k^2+...|Stochasticity bounds from tracer occupancy|Set P0=1/n exactly for weighted selected tracers
Multi-tracer cancellation|ratio delta_g1/delta_g2 with correlated stochasticity|Cosmic-variance cancellation domain for gravity response|Assume zero cross-shot noise
Reconstructed BAO conditional likelihood|p(P_full,alpha_BAO) with cross covariance|Growth information conditional on same-sample acoustic distances|Multiply full-shape and BAO likelihoods without covariance
Equality-scale versus vacuum response|J_eq and J_a0 in broadband spectrum|Separable early-time and late-time scale combinations|Identify a broadband turnover with a0 directly
Neutrino-like suppression degeneracy|Delta P_source(k) compared to fixed-known-species response|Gravity suppression distinguishability without adding species|Introduce new particles to rescue a poor fit
Nonlinear mode-coupling kernel|delta2(k)=integral F2_action(q,k-q)delta1delta1|Candidate second-order clustering correction|Use GR F2 for a changed force law
Infrared displacement resummation|P_w,resum=exp[-k_i k_j A_ij/2]P_w|Acoustic smearing derived from candidate long modes|Change short-scale forces while freezing long displacement response
Wide-angle correction|xi(s,d,mu)=xi_plane+O(s/d)|Observer-geometry bias in lowest-redshift multipoles|Apply plane-parallel theory to every pair
Relativistic number-count terms|Delta_g=b delta+RSD+Doppler+lensing+potential|Large-scale metric corrections and gauge cancellation|Keep a potential term without its gauge partners
Magnification of spectroscopic targets|Delta_g includes (5s-2)kappa|Selection slope contribution to anisotropic clustering|Treat apparent-magnitude selection as volume limited
Redshift-dependent bin averaging|P_eff=integral dz W(z)P(k,z)|Growth-curvature bias from effective-redshift compression|Use a single redshift despite strongly varying response
Selection-function radial mode|n_hat(z)=n_true(z)+delta n(z)|Radial-selection projection on growth multipoles|Estimate selection from the same modes without propagating loss
GR recovery in measured domain|norm(P_action-P_GR) after derived high-field matching|Finite-scale recovery certificate|Use high k as a substitute for demonstrated high acceleration
Common-source covariance with lensing|Cov(P_gg,C_gk) includes shared large-scale modes|Incremental lensing bridge with consistent tracer weighting|Assume another instrument means independent cosmic variance
Vacuum-coupling ratio inference|Lambda_eff=32pi(G_E/G_N)a0^2/c^4|Joint expansion/growth constraint retaining coupling ratio|Set G_cosmo=G_N by symbol reuse
Perturbative validity frontier|P_1loop/P_tree and neglected-order bound|Observed-bin domain where candidate calculation is controlled|Retain bins solely because their statistical error is small
''')
program('clusters', r'''
Count-rate selection integral|lambda(C,z)=integral n(M,z)p(C given M,z)S(C,z)dM dV/dz|Candidate expected count-rate distribution|Use a GR mass function as measured counts
Collapse barrier derivation|delta_c(M,z) from candidate spherical-collapse boundary problem|Action-derived mass-dependent collapse threshold|Insert the GR collapse threshold unchanged
Non-spherical collapse correction|B=delta_c+beta sigma^gamma with coefficients derived or bounded|Tidal correction uncertainty on abundance|Fit an arbitrary barrier independently in each mass bin
Vacuum-volume response|dV/dz dOmega=c D_M^2/H|Geometrical count response distinct from growth|Attribute all count changes to structure growth
Baryon-defined mass conversion|M_Delta=(4pi/3)Delta rho_ref R_Delta^3|Metric/baryon mass convention dictionary|Treat a GR overdensity mass as direct baryonic mass
X-ray count-temperature kernel|C=integral R_E Lambda_E(T,Z)n_e^2 dV/(4pi D_L^2)|Instrument-folded gas-to-count map|Convert count rate to mass without gas physics
Hydrostatic departure|dP/dr=-rho_g g+rho_g a_nonthermal|Nonthermal-support envelope for source reconstruction|Assume hydrostatic equilibrium for disturbed systems
Observable-scatter selection bias|p(M given C,selected) proportional to n(M)p(C given M)S|Eddington correction retaining steep abundance slope|Use inverse mean scaling as an unbiased mass estimate
Count-rate and shear covariance|Cov(lnC,gamma_t given M) nonzero|Selection-conditioned lensing mass calibration|Assume gas orientation cannot correlate with lensing
Extent-selection response|S=S(C,theta_extent,z,exposure)|Surface-brightness-dependent completeness operator|Model selection as a sharp flux cut only
Optical confirmation impurity|lambda_obs=lambda_cluster+lambda_false|Contamination-marginalized abundance|Treat all confirmed candidates as certainly genuine
Photometric redshift migration|N_iobs=sum_j R_ij N_jtrue|Redshift-bin migration correction|Evaluate all objects at their most likely redshift
AGN blending term|C_obs=C_ICM+C_AGN|Cluster-count response to unresolved nuclear flux|Assign point-source photons to hot gas
Sky exposure modulation|lambda(nhat)=S(exposure,background)lambda_cosmic|Exposure-correlated abundance null|Interpret exposure pattern as cosmic anisotropy
Mass calibration cross-survey mode|Mcal_s=Mtrue exp(b_s)|Relative DES/KiDS/HSC calibration direction|Count common calibration galaxies independently
Super-survey count covariance|Cov_N=diag(N)+b_i b_j N_iN_j sigma_window^2|Sample-variance correction for the actual footprint|Use pure Poisson counts in a correlated density field
Merger-state selection|p(C given M)=sum_state p_state p(C given M,state)|Dynamical-state-dependent selection bias|Assume merging and relaxed clusters share identical gas observables
Baryon-fraction conservation|Mgas+Mstars+M_otherb=M_b,total|Baryon inventory consistency with required source strength|Introduce an unobserved mass component without declaring it
Carrier evacuation boundary|Mcarrier(<r)=integral rho_carrier dV from derived transport|Cluster clearing requirement from counts and profiles|Specify removal by hand with no conserved destination
Gate-environment dependence|p(occupation given M,env) enters n_selected|Environmental selection of the same source gate|Tune one gate threshold per cluster
Redshift evolution of scaling|ln C=A+B ln M+gamma ln E(z)+delta(z)|Identifiable evolution beyond imposed self-similarity|Fix gamma to GR while testing altered equilibrium
Rare-tail likelihood calibration|p(N_tail given theta)=Poisson(lambda_tail) with nuisance integration|High-count-tail exclusion with exact discreteness|Use Gaussian error bars for nearly empty bins
Joint count-calibration information|L=L_counts L_shear conditional on latent masses|Proper joint likelihood without reused mass posteriors|Multiply a mass posterior and the shear data that generated it
Mass-function universality audit|f(sigma,M,z) versus f(sigma) on candidate solutions|Testable non-universality functional|Assume universal f solely because it fits GR simulations
One-cell cluster abundance witness|min_theta residual of rate-redshift-extent vector|Common-action cluster-count compatibility certificate|Retune carrier occupation after seeing each observable
''')
program('cluster_lensing', r'''
Shear-space mass calibration|gamma_t(theta)=derived integral of transverse derivatives(Phi+Psi)|Cluster metric-response calibration in native shear units|Use published GR masses as theory-independent input
Reduced shear profile|g_t=gamma_t/(1-kappa)|High-convergence profile correction|Replace reduced shear by shear at all radii
Miscentering marginalization|g_off(R)=integral p(Roff)g_centered(abs(R-Roff))dRoff|X-ray-center offset impact on source gate|Use angular offsets as fixed physical distances
Cluster-member dilution|g_obs=(1-f_member)g_background|Contamination-corrected metric profile|Set member contamination to zero near the cluster center
Boost-factor magnification coupling|n_obs/n_random=(1-f_member)^-1 mu^(2.5s-1)|Separated dilution and magnification corrections|Attribute all excess source counts to cluster members
Source-redshift efficiency|beta=expect[D_ls/D_s]|Redshift-efficiency uncertainty in metric normalization|Evaluate efficiency at the mean source redshift
Profile shape versus normalization|g_t(R)=A f(R/r_s,gate)|Gate-shape information after amplitude marginalization|Interpret normalization-only change as a measured transition radius
Mass-sheet response null|g invariant under kappa'=lambda kappa+1-lambda|Unidentifiable cluster potential modes|Claim absolute convergence from reduced shear alone
Triaxial orientation selection|p(g,C given orientation) integrated over selected orientations|X-ray-selected orientation bias|Average random orientations before selection
Foreground structure covariance|g_obs=g_cluster+g_LSS|Correlated line-of-sight shear uncertainty|Subtract a fixed background profile from every cluster
Radial-bin covariance|Cov(g_i,g_j) includes reused source shapes|Effective independent profile degrees of freedom|Treat the same source in overlapping apertures independently
Cluster redshift-size transport|R=D_A(z)theta|Geometry-induced change in inferred gate radius|Change cosmology without recomputing physical radii
X-ray luminosity conditional stacks|expect[g given C] not g(expect[M given C])|Scatter-aware stacked profile prediction|Evaluate nonlinear profiles only at mean mass
Tangential-cross parity test|gamma_cross should vanish under parity-symmetric scalar ensemble|Cross-shear contamination bound|Use cross shear as a second positive lensing detection
Random-center subtraction|g_corr=g_cluster-g_random|Survey-additive correction with joint covariance|Subtract random centers as noiseless data
Inner-baryon response|g_bar=G_N(Mstars+Mgas)/r^2|Conditional baryon-profile map into MONO lensing|Fit an arbitrary halo as the missing baryonic input
Outer-boundary response|Phi_boundary changes projected deflection across aperture|Finite-domain uncertainty on outskirts lensing|Extend a logarithmic potential to infinity without matching
Heat-filter profile convolution|source=S*div[(nu-1)grad Su]|Exact filtered-source shear profile|Smooth a final unfiltered shear curve and call it equivalent
Gate occupation versus slip|J=[partial g/partial occupation,partial g/partial eta]|Rank certificate separating source strength from potential slip|Set slip to zero to force a unique occupation
Selection-conditioned shear covariance|Cov(g given selected C) differs from unconditional Cov(g)|Calibration uncertainty conditional on X-ray selection|Use unselected mock clusters for the selected likelihood
Photometric blending response|m=m(surface_brightness,neighbor density)|Radial shear-calibration bias from cluster light|Use field-galaxy calibration unchanged in crowded centers
Concentration nuisance transport|partial g/partial concentration versus partial g/partial xi|Profile-scale degeneracy under candidate density families|Import an NFW concentration relation as exact physics
Baryon-census external bridge|g_lens versus g_bar from independent gas and light|Measured metric enhancement profile conditional on census|Derive both axes from the same GR lensing mass
Abundance calibration reuse|p(counts,shear given theta,Mlatent)|Information passed to counts without posterior double use|Treat mass-calibration summary and raw shear as independent
Vacuum-footing profile comparison|a0_can and a0_alt yield separate g_t(R)|Data-weighted two-normalization profile discriminator|Fit a normalization per stack instead of testing common values
''')
program('gw_phase', r'''
Stationary-phase action map|d2Psi/df2=2pi/(df/dt)|Inspiral phase from derived binding energy and flux|Import GR energy balance with an unrelated correction
Dipole-order coefficient bridge|DeltaPsi=beta_minus2 v^-7 with v=(pi GMf/c^3)^(1/3)|Allowed negative-PN phase coefficient of the pinned action|Add a radiating scalar solely to realize the template
Chirp-mass degeneracy|partial Psi/partial Mc overlaps v^-5 coefficient|Identifiable 0PN combination|Treat fitted chirp mass as independent of the tested phase
Tidal-phase projection|DeltaPsi_tidal proportional to Lambda_tilde v^5|Tidal-orthogonal gravity response|Set neutron-star tidal deformability to zero by convenience
Spin-orbit phase ambiguity|Psi_SO=beta_spin v^-2 within stated convention|Spin-conditioned deviation bound|Fix spins from a GR-only posterior
Higher-mode consistency|h=sum_lm h_lm spinY_lm|Mode-dependent phase correction with common source parameters|Fit independent binary masses to each harmonic
Eccentricity residual|DeltaPsi_e proportional to e0^2 f^-34/9 at leading approximation|Eccentricity versus gravity identifiability|Declare circularity exact without a residual test
Calibration phase basis|h_obs=h_true exp[i delta_phi_cal(f)]|Calibration-orthogonal phase score|Let an unconstrained calibration spline cancel any deviation
Noise-spectrum estimation|inner(a,b)=4Re integral a*b/Sn df|PSD uncertainty on low-frequency deviation coefficients|Estimate noise from signal-contaminated data as fixed truth
Waveform-family transport|DeltaPsi_models=Psi_A-Psi_B|Model-discrepancy envelope on gravity coefficients|Select the waveform with tightest bound after comparing results
Finite-frequency validity|epsilon(f)=abs(next PN term/current term)|Frequency domain with controlled candidate phasing|Extrapolate a low-velocity expansion into merger
Detector-time response|h_d=Fplus hplus+Fcross hcross shifted by delay|Detector-projected two-polarization phase likelihood|Treat one detector as measuring both polarizations independently
Distance-amplitude feedback|A(f) proportional to derived source amplitude/d_L_GW|Phase-amplitude consistency with common source masses|Hold distance fixed from a GR amplitude fit
Neutron-star sensitivity|s_A=-partial ln m_A/partial ln G_N under fixed baryon number|Compact-body response needed for coupling constraints|Use point-particle masses independent of self-gravity
Radiation-reaction conservation|dE_orbit/dt=-F_tensor-F_allowedmatter|Energy-consistent phase correction|Add a phase term without an energy channel
High-acceleration matching|G_orbit and G_radiative from same action|Measured-Newton normalization in the phase map|Set bare, orbital and radiative couplings equal by notation
Propagation-generation separation|DeltaPsi=DeltaPsi_emit+DeltaPsi_prop|Identified combination of source and travel effects|Assign all phase deviation to emission
Local vacuum curvature correction|dimensionless epsilon_L=Lambda_eff r_orbit^2|Bounded vacuum-curvature contribution to phasing|Insert a0 as an unsuppressed constant orbital acceleration
Filter-scale strong-field domain|xi/r_orbit enters full field solution|Candidate filter applicability certificate at binary separations|Apply quasistatic MONO directly to a relativistic merger
Binary environment acceleration|Delta f/f=-a_los t/c to leading order|Environmental Doppler contamination of low-order phase|Interpret host acceleration as dipole radiation
Tidal heating absorption|dE_H/dt from derived horizon or surface boundary|Absorption-phase bound conditional on remnant boundary|Assume a horizon when the candidate has not derived one
Coalescence-time projection|Psi contains 2pi f tc-phic|Deviation subspace after time/phase marginalization|Count constant and linear phase shifts as physical violations
Joint deviation prior geometry|p(beta_vector) transforms with Jacobian|Parameterization-invariant likelihood summary|Compare Bayes factors with unmatched prior volumes
Same-event reuse accounting|L_GRtest derived from same strain as L_source|Conditional information beyond source-property release|Multiply source posterior by its generating strain likelihood
Canonical-alternative phase difference|DeltaPsi_footing=Psi(a0_alt)-Psi(a0_can)|Observable normalization contrast or upper bound below sensitivity|Amplify an undetectable correction by freely rescaling a0
''')
program('map_stats', r'''
Peak-count source response|N_peak(nu)=count local maxima of kappa/sigma_noise|Candidate peak-height distribution|Use GR peak emulator as observed peak counts
Aperture-mass third moment|expect[Map^3]=integral U1 U2 U3 B_kappa|Bispectrum-weighted MONO response|Infer third moments solely from the power spectrum
Convergence skewness|S3=expect[kappa^3]/expect[kappa^2]^2|Redshift-resolved non-Gaussian growth functional|Assume Gaussian maps preserve measured skewness
Minkowski area curve|V0(nu)=area{kappa>nu}/area_total|Threshold-area response with mask correction|Count masked pixels as zero convergence
Minkowski boundary length|V1(nu) proportional to integral delta(kappa-nu)abs(grad kappa)|Gradient-sensitive filter constraint|Use pixel-count perimeter without resolution correction
Euler characteristic density|V2(nu)=number_components-number_holes per area|Topology response to occupied-source morphology|Identify every peak with an independent halo
Wavelet scale coupling|S2(j1,j2)=expect[abs(abs(kappa*psi_j1)*psi_j2)]|Nonlinear cross-scale source statistic|Replace second-order scattering by a product of first orders
CNN score transport|score_action=partial ln p(summary given theta_action)/partial theta|Transportability certificate for trained compression|Treat a GR-trained posterior as a candidate likelihood
Simulation-support distance|d_support=distance(summary_data,training manifold)|Data-driven out-of-distribution boundary|Extrapolate a neural density estimator without coverage tests
Conditional peak information|I(peaks given power)=I(peaks,power)-I(power)|Higher-order gravity information beyond two-point data|Multiply peak and power likelihoods as independent
Shape-noise non-Gaussianity|p(e)=measured ellipticity distribution convolved with shear|Noise-induced peak-tail correction|Replace all ellipticity noise by Gaussian draws
Mask-edge topology response|Delta V_k=V_k(masked field)-response_corrected V_k|Boundary leakage on topology statistics|Compare unequal masks without correcting boundaries
Source-clustering map bias|kappa_hat from density-weighted shear sampling|Galaxy-sampling modulation of non-Gaussian statistics|Place sources uniformly while claiming survey realism
Photo-z migration of peaks|N_peak^i=sum_j R_ij N_peak,true^j plus cross terms|Tomographic peak migration operator|Treat redshift errors as a global amplitude only
Baryon feedback morphology|delta rho conserves mass; delta peaks need not vanish|Conservation-controlled small-scale morphology envelope|Alter total mass to obtain the desired peak count
Intrinsic alignment morphology|e_obs=gamma+e_IA+noise|Alignment-induced false peaks with tidal correlations|Add independent white alignment noise
Smoothing-kernel commutator|Map[S source] differs from S_map Map[source]|Observable failure of source/map smoothing equivalence|Apply the theory filter only after reconstructing the map
Carrier-void topology|V_void(threshold) from solved occupied-source field|Under-dense morphology constraint on carrier evacuation|Treat negative reconstructed convergence as negative physical mass
Map reconstruction null space|kappa_hat=A gamma with kernel(A)|Unobservable modes of map-level inference|Claim an absolute mass sheet from reconstructed maps
Spatially varying calibration|gamma_obs(n)=(1+m(n))gamma(n)+c(n)|Calibration-induced spatial morphology bound|Use one survey-wide calibration to remove a spatial mode
Super-sample non-Gaussian response|partial N_peak/partial delta_b|Survey-background covariance of peak and topology vectors|Use independent small boxes lacking long modes
Neural posterior calibration|rank(theta_true in posterior) uniform under generated truth|Candidate-specific coverage certificate|Validate only on the same simulations used for training
Summary-level information loss|F_full-F_summary positive semidefinite under valid compression|Lost candidate direction under released summary compression|Claim sufficiency from GR parameter recovery alone
Redshift evolution of non-Gaussianity|partial_z S3_action versus measured bins|Growth-history test beyond amplitude rescaling|Fit a separate nonlinear amplitude in each source bin
One-action map ensemble|p(kappa maps given fixed action,initial conditions)|Joint map-statistic compatibility witness|Mix GR map morphology with MONO two-point amplitude
''')
program('sn_lensing', r'''
Magnification PDF from metric|mu=1/det(A); A from null-geodesic Jacobi map|Candidate luminosity magnification distribution|Use a GR compact-lens PDF as theory-free data
Magnitude-flux nonlinear mapping|Delta m=-2.5log10(mu)|Correct transformed probability density with Jacobian|Treat magnitude and flux residuals as Gaussian equivalents
Flux conservation under selection|expect[mu given selected] differs from 1|Detected-sample mean magnification correction|Enforce unity mean after a magnitude cut
High-magnification optical depth|tau(mu>mu0)=integral n_lens sigma_mu dV|Derived strong-tail probability|Insert a compact-object abundance absent from the theory
Smooth-source caustic structure|det(A)=0 for candidate metric lens|Caustic contribution from smooth carrier structures|Assume every magnification tail requires point particles
Finite-source cutoff|mu_ext=integral I_source mu_point/integral I_source|Supernova photosphere suppression of caustic tails|Use divergent point-source magnification as a finite prediction
Lens mass-spectrum identifiability|p(mu)=integral p(mu given M)p(M)dM|Identifiable moments of allowed ordinary compact lenses|Report a unique mass function from one tail statistic
Intrinsic luminosity convolution|p(dm)=integral p_int(dm+2.5log10mu)p_lens(mu)dmu|Intrinsic/lensing tail separation|Attribute all positive skewness to gravity
Dust-tail discrimination|dm_dust(lambda) versus dm_lens achromatic|Colour-conditioned gravitational tail bound|Ignore colour information when fitting extinction
Outlier rejection response|p_kept(dm)=p(dm)S_clip(dm)/Z|Lensing constraints after analysis clipping|Treat removed bright events as unobserved random omissions
Redshift scaling of skewness|kappa3(dm,z)=kappa3_intrinsic+kappa3_lens(z)|Path-length-dependent lensing statistic|Use one redshift-independent lensing PDF
Host-environment correlation|p(mu given host,foreground) differs from marginal p(mu)|Environment-selected magnification correction|Assume supernova locations sample sightlines uniformly
Foreground galaxy cross-correlation|expect[dm delta_g(theta)]|Independent lensing-origin check for magnitude tails|Correlate residuals with their own host only
Weak-strong matching|p(mu) matched across mu_match with normalization|Continuous magnification likelihood over regimes|Splice PDFs without probability conservation
Microlensing time dependence|mu(t)=mu[x_source(t),R_photo(t)]|Light-curve distortion sensitivity distinct from mean brightness|Assume all lensing is constant over an expanding photosphere
Multiple-image time delays|Delta t=(1+z_l)D_Delta/c times Fermat difference|Unresolved-image temporal contamination bound|Sum delayed light curves as simultaneous flux
Wave-optics applicability|w=4G_N M omega/c^3|Domain where geometric magnification is valid|Apply ray optics below the relevant wavelength scale
Compact-fraction prior transport|alpha=rho_compact/rho_total with candidate mass definition|Theory-consistent ordinary compact fraction bound|Reuse a GR total-matter denominator unchanged
Baryonic census consistency|rho_compact <= rho_stars+rho_remnants+allowed ordinary matter|Compact-lensing abundance compatibility with independent census|Create extra particles to satisfy the lensing distribution
Heat-filter lens cross-section|sigma_mu(xi)=area{mu_action(xi)>mu0}|Filter-induced caustic cross-section response|Smooth the observed PDF instead of deriving the metric
Source-gate environmental cutoff|sigma_mu depends on occupation and g_bar/a0|Gate-dependent magnification tail|Use a separate gate for each lens mass
Calibration-tail common mode|dm_i=dm_phys_i+z_survey(i)|Tail likelihood with shared zero-point uncertainty|Count a survey offset as many independent outliers
Counts of extreme events|N_tail follows selected correlated point process|Discrete tail bound robust to empty bins|Use asymptotic Gaussian errors for zero tail events
Distance-and-lensing joint reuse|p(mean residuals,shape residuals) with common SNe|Extra distribution-shape information conditional on distances|Multiply a distance fit and magnification fit independently
Vacuum-scale tail contrast|p(mu;a0_can) versus p(mu;a0_alt)|Two-footing distinguishability in the observed residual distribution|Fit arbitrary tail amplitude independently of a0
''')
program('cmb', r'''
Acoustic peak phase|C_l^XY=4pi integral P_R Delta_l^X Delta_l^Y dlnk|Candidate acoustic-phase residual|Import GR transfer functions with relabelled densities
Odd-even peak loading|R_b=3rho_b/(4rho_gamma)|Baryon-loading constraint with derived gravitational driving|Treat fitted cold-dark-matter density as a directly measured species
Polarization acoustic coherence|r_l=C_l^TE/sqrt(C_l^TT C_l^EE)|Temperature-polarization coherence response|Fit independent primordial phases to each spectrum
Sound-horizon angular scale|theta_star=rs(zstar)/D_M(zstar)|Early/late geometry degeneracy certificate|Infer a0 directly from theta_star without recombination dynamics
Diffusion damping ratio|theta_D/theta_star=r_D/r_s|Damping-to-acoustic ratio within candidate expansion|Tune recombination independently to force a fit
Early integrated Sachs–Wolfe term|Delta_T includes integral(Phi'+Psi')deta|Potential-decay driving of the first acoustic peaks|Assume constant potentials during radiation–matter transition
Late integrated potential term|Delta_Tlate=integral(Phi'+Psi')deta|Large-angle vacuum-response envelope|Set homogeneous expansion to zero to remove the term
Lensing smoothing consistency|C_l,lensed=remap[C_l,unlensed,C_L^phiphi]|Two-point smoothing versus reconstructed-lensing constraint|Fit unrelated lensing amplitudes to the same action
Polarization calibration angle|E_obs=Ecos2alpha-Bsin2alpha|Rotation-induced TE/EE bias|Assign instrument rotation to a new propagating mode
Polarization efficiency|EE_obs=p^2 EE; TE_obs=p TE|Efficiency-orthogonal acoustic combination|Use independently fitted p values for TE and EE
Temperature gain null|TT_obs=g^2 TT; TE_obs=gp TE|Gain-free spectrum consistency statistic|Treat common gain as independent in every multipole
Beam-eigenmode response|delta C_l=2C_l sum_a b_a e_a(l)|Beam-error projection onto damping features|Discard beam uncertainty where damping is strongest
Bandpass foreground mixing|C_l^ij=C_CMB+sum_fg f_i f_j C_fg|Frequency-cleaned acoustic response|Subtract foregrounds using delta-function bandpasses without error
Atmospheric filtering transfer|C_obs=T_l C_sky|Low-multipole transfer correction|Assume all sky modes survive time-stream filtering
TE sign-change localization|C_l^TE=0 defines acoustic-node positions|Node-based phase constraints robust to amplitude|Use absolute TE values and erase their sign
Peak-width growth response|width_l from recombination thickness and lensing|Distinct broadening components under one action|Assign all broadening to lensing
Reionization-amplitude degeneracy|high-l amplitude proportional to A_s exp(-2tau)|Identifiable primordial amplitude combination|Claim A_s separately without an optical-depth constraint
Primordial-tilt versus filter shape|J_ns compared with J_xi over TT TE EE|Filter-shape direction independent of a power-law tilt|Fit arbitrary primordial spectrum then claim a unique filter bound
Known-neutrino stress response|Phi-Psi from derived anisotropic stress|Phase-sensitive stress constraint with no new species|Set all slip to zero before solving radiation perturbations
Curvature-lensing coupling|D_A(K) changes acoustic and lensing kernels|Curvature-vacuum degeneracy beyond a single peak scale|Fix curvature using the same data twice
Foreground-clean spectral residual|r=d_CMB-m_action after joint foreground marginalization|Candidate CMB residual with foreground uncertainty|Treat cleaned spectra as exact noiseless foreground removal
Shared-sky cross-experiment covariance|Cov(C_ACT,C_SPT) includes common CMB modes|Independent information added by the second experiment|Add inverse variances as if the skies were different
Seasonal incremental modes|C_crossseason signal with uncorrelated instrumental noise|New-season information distinct from repeated sky signal|Count common cosmic variance independently by season
Coupling-ratio acoustic response|G_cosmo/G_N retained in H and perturbation equations|Measured acoustic constraint on coupling matching|Identify measured Newton coupling with cosmological coupling by fiat
Vacuum-linked full-spectrum cell|rho_Lambda=4a0^2/(G_N c^2); F_action predicts TT TE EE|Single-cell three-spectrum compatibility witness|Retune a0 separately for temperature and polarization
''')
program('foreground', r'''
Thermal SZ pressure map|y=(sigma_T/m_e c^2)integral P_e dl|Candidate pressure-power prediction in actual frequency bands|Treat a thermal SZ template as a measured pressure field
Kinetic SZ momentum map|Delta T/T=-(sigma_T/c)integral n_e v_los dl|Velocity-weighted gas response without dark-halo insertion|Equate kSZ amplitude directly with matter power
Relativistic SZ spectral curvature|Delta I=sum_n Y_n(nu)integral n_e theta_e^(n+1)dl|Temperature-moment bias on gravity-sensitive SZ power|Use nonrelativistic spectral weights at all temperatures
Thermal-kinetic SZ separation|C_nunu'=f_tSZ(nu)f_tSZ(nu')C_tSZ+C_kSZ|Identifiable gas-pressure and velocity-power combinations|Assign all frequency-independent excess to kSZ
CIB emissivity projection|I_nu=integral dz j_nu(z) geometric weight|CIB source-window uncertainty on CMB cleaning|Assume one redshift for all infrared emission
CIB–SZ correlation|C_tSZ,CIB=r sqrt(C_tSZ C_CIB)|Correlated-foreground bias in inferred gas support|Set cross correlation to zero without a bound
Radio Poisson source tail|C_l^radio=integral_0^Scut S^2 dN/dS dS|Flux-cut-dependent radio contamination envelope|Use source counts below threshold without completeness
Clustered dusty-source spectrum|C_l^CIB=projection[b_j^2 P+shot]|Clustering versus shot-noise separation|Fit all dusty power as white noise
Frequency decorrelation|r_ij=C_ij/sqrt(C_ii C_jj)|Observable decorrelation matrix with positivity|Allow pairwise correlations that form an indefinite covariance
Bandpass integration uncertainty|f_i=integral R_i(nu)f(nu)dnu|Bandpass-error bias on SZ spectral null|Replace measured band response by central frequency exactly
Galactic dust morphology|C_l,dust depends on sky mask and polarization|Dust-mask dependence of gravity residuals|Assume dust amplitude scales only with retained area
Galactic synchrotron curvature|I_nu proportional to nu^(beta+c lnnu)|Curvature-induced residual in multifrequency cleaning|Assume a fixed power law across all bands
Foreground trispectrum covariance|Cov_C includes connected four-point foreground term|Non-Gaussian uncertainty in small-scale residuals|Use Gaussian covariance despite bright unresolved sources
Gas-temperature support bridge|grad P_e plus other support=-rho_g grad Phi|Pressure constraints on the dynamical potential|Infer gravity from electron pressure without ion/nonthermal terms
Carrier clearing versus SZ suppression|Delta C_tSZ from solved gas redistribution under carrier transport|Cluster-clearing imprint in pressure spectrum|Delete cluster gas to mimic carrier evacuation
Redshift decomposition nonuniqueness|C_l=integral W^2(z)P(l/chi,z)dz|Null family of pressure histories sharing the same spectrum|Claim a unique redshift distribution from integrated power
Reionization duration inversion|C_kSZ,patchy=F[x_e(z),bubble field,v]|Conditional duration constraint requiring ionization morphology|Map one kSZ number to duration independent of bubble physics
Late-time kSZ floor|C_kSZ,total=C_patchy+C_homogeneous|Reionization bound marginalized over candidate late-time momentum|Fix the homogeneous floor to a GR simulation
Optical-depth normalization|tau=sigma_T integral n_e dl|Electron-column consistency with pressure and velocity moments|Fit gas density independently in each SZ observable
Baryon conservation spectral sum|integral rho_b dV fixed under redistribution|Large-scale pressure/momentum change allowed by baryon accounting|Treat spectral suppression as disappearance of baryonic mass
Foreground-primary information overlap|p(C_primary,C_fg) joint covariance|Conditional foreground gravity information|Multiply primary and foreground posteriors from the same spectra
Template-shape misfit direction|r_perp=P_perp,templates(d-F_action)|Foreground-orthogonal candidate response|Let templates span arbitrary oscillatory CMB features
Filter versus feedback scale|J_xi and J_feedback in tSZ/kSZ spectra|Separability of gravitational filtering and gas heating|Identify equal power suppression with equal mechanisms
Same-frequency cross-season null|D_l=C_l(seasonA)-C_l(seasonB) with shared sky|Instrument-stability bound on foreground evolution claims|Interpret stationary sky differences as cosmological time evolution
Vacuum-footing gas prediction|a0 tied to rho_Lambda in equilibrium and transport|Two-footing pressure/momentum compatibility region|Choose unrelated normalization for gas and lensing sectors
''')
program('shear_contrasts', r'''
Colour-split lensing contrast|Delta C=C_red/W_red-C_blue/W_blue after matched kernels|Colour-dependent residual beyond common metric lensing|Match only mean redshift while ignoring full kernels
Low-high redshift closure|Delta=F_low^-1 d_low-F_high^-1 d_high in identified modes|Growth-evolution contrast of one action|Fit independent acceleration scales to redshift halves
North-south common-mode subtraction|Delta d=d_N-d_S; Cov includes shared calibrators|Sky-region gravity consistency after calibration sharing|Treat hemispheric calibration standards as independent
Small-large angle response ratio|R=C_small/C_large with nonlinear covariance|Scale-dependent filter contrast|Declare nonlinear feedback irrelevant by fixing it
E/B difference transport|Delta_EB=E-P_model(B contamination)|Metric-compatible parity contrast|Interpret any B-mode as extra gravitational radiation
Correlation-versus-bandpower contrast|d_xi-H d_Cl with exact finite windows|Representation-consistency residual|Use an infinite-range Hankel transform on finite cuts
Old-new footprint comparison|Delta=C_newarea-C_oldarea after selection matching|Independent-area increment in inferred growth|Count the old footprint twice
Calibration-update counterfactual|Delta d_cal=F(nz_new)-F(nz_old) at fixed images|Redshift-recalibration contribution to parameter shift|Call a reduction change new sky information
Depth-selection contrast|Delta C=F(zmax_high)-F(zmax_low) conditional on shared galaxies|Additional-depth information with overlap removed|Treat nested source selections as independent samples
Alignment-type contrast|C_GI^red-C_GI^blue with common Weyl field|Type-dependent intrinsic-alignment response|Assign different metric potentials to galaxy colours
PSF-quality split|Delta C=C_goodseeing-C_poorseeing with matched populations|Seeing-dependent bias bound|Ignore selection-induced population differences
Magnitude-split magnification response|Delta C controlled by difference in (5s-2)|Magnification-selection contrast isolating photon mapping|Assume magnitude cuts change only number density
Source-size split calibration|m(size) induces predictable cross-bin response|Size-dependent shear response null|Interpret size-dependent calibration as source-gate physics
Redshift-calibrator field removal|Delta nz_minusfield changes all source bins jointly|Influence of a shared calibration field|Treat removal fits as independent posterior draws
Adjacent-bin exchange symmetry|C_ij=C_ji after consistent kernels|Implementation-level reciprocity of measured shear response|Use inconsistent distance units in opposite bin orderings
Tomographic residual rank|rank of whitened residual across bin pairs|Minimum physical response components needed by data|Assign one unconstrained nuisance per residual entry
Conditional external-survey contrast|d_KiDS-E[d_KiDS given d_DES]|Extra shear information beyond overlapping external data|Compare marginal S8 differences as independent normals
Prior-volume sensitivity|posterior mode versus marginal mean under transformed coordinates|Data-likelihood contrast separated from parameter-volume shifts|Treat a mean shift as a changed measurement automatically
Shared-baryon uncertainty cancellation|u^T J_feedback=0|Feedback-insensitive interscale contrast|Choose u using the observed anomaly sign
Source-gate environment split|Delta C conditioned on independently defined foreground density|Environmental MONO response contrast|Define environments using the same shear residual under test
Long-mode region coupling|Cov_regions includes common super-survey modes|Spatial contrast covariance with shared background|Assume disjoint masks imply zero cosmological covariance
Calibration-cosmology joint rank|rank([J_cal,J_grav]) in split-vector space|Identified common-action modes across all splits|Fix calibration before evaluating identifiability
Vacuum-history split test|a0(z) tied to rho_Lambda(z) across source kernels|Relative vacuum-history response of source subsets|Interpret each source-bin a0 fit as parameter-free prediction
Release-reduction symmetry|same objects and selection, altered pipeline only|Reduction-induced gravity shift with matched-object covariance|Mix object additions into a pure calibration contrast
Global contrast maximum statistic|max_j abs(Delta_j/sigma_j) with joint null distribution|Multiplicity-corrected inconsistency certificate|Quote the most discrepant split without search correction
''')
program('gw_catalog', r'''
Catalog selection intensity|lambda(theta)=R(theta)VT(theta)|Action-dependent detection population likelihood|Use a GR selection function for altered waveforms
Source-frame mass conversion|m_det=(1+z)m_source|Mass-redshift degeneracy under candidate distances|Treat detector-frame masses as source-frame masses
Waveform-prior removal|L(theta) proportional to posterior(theta)/prior(theta)|Recoverable event likelihood and support limits|Reweight into regions never sampled by the original posterior
Astrophysical-probability mixture|p(d)=p_astro p_signal+(1-p_astro)p_noise|Candidate-event contamination marginalization|Set every catalog entry to certain astrophysical origin
Threshold-selection bias|p(theta given detected) proportional to p_det(theta)p(theta)|Detection-biased phase-deviation distribution|Average detected deviations without efficiency correction
O4a incremental likelihood|L_total=L_old times L_new conditional on shared calibration|New-run tensor information with event deduplication|Count reanalysed old events as new detections
Mass-dependent GR recovery|DeltaPsi(M,f) from common action|Mass-scaled recovery residual across events|Allow one free modification coefficient per event without hierarchy
Spin-population phase nuisance|p(chi,m,z) enters waveform deviations|Population spin uncertainty on gravity inference|Fix spin distribution from the same GR-only catalog
Inclination-polarization ambiguity|h_d=Fplus Aplus(i)+Fcross Across(i)|Two-polarization population consistency|Treat orientation priors as measured inclinations
Distance-calibration common mode|d_L,inferred=d_L,true(1+delta_gain)|Run-correlated distance-systematics floor|Treat calibration errors as independent by event
Merger-rate evolution|R(z) dV/dz/(1+z)|Rate-corrected cosmological detection distribution|Omit observer/source time dilation
Host-environment acceleration|DeltaPsi_env depends on a_los and signal duration|Population bound on environmental phase contamination|Attribute all low-frequency phase curvature to gravity
High-mass waveform truncation|information_f weighted by abs(h)^2/Sn|Event-specific inspiral validity and merger dependence|Apply an inspiral-only approximation to merger-dominated events
Low-mass tidal population|p(Lambda_tidal given m,EOS)|Matter-response uncertainty in gravity tests|Classify compact objects using masses inferred under an untested waveform
Eccentric population subcomponent|p(e)=f_e p_e+(1-f_e)delta(e)|Eccentricity-induced false deviation bound|Force all systems circular to tighten constraints
Hierarchical deviation scatter|beta_i drawn from p(beta given common action,source)|Predicted source dependence versus unexplained scatter|Fit arbitrary scatter and call consistency a mechanism
Lensing magnification selection|d_GW,obs=d_GW/sqrt(mu)|Magnification-induced mass-distance bias|Assume magnification changes phase-derived mass directly
Repeated-image catalog duplication|p(d_i,d_j given same source,lens)|Duplicate-source impact on population evidence|Count strongly lensed images as independent progenitors
Sky-exposure tensor anisotropy|p_det(nhat,polarization,t)|Exposure-corrected directional deviation test|Infer anisotropy from raw sky counts
Noise-glitch phase contamination|d=h_action+g_glitch+n|Robust event-level gravity scores under glitch uncertainty|Absorb a localized glitch into a universal phase coefficient
Tail-event influence bound|Delta logL_i=logL_all-logL_without_i|Maximum event influence on common-action exclusion|Report a population bound driven by one unchecked event
Mass-gap classification transport|p(class given strain,action,EOS)|Candidate-dependent classification without fixed GR labels|Use the catalog classification as an immutable physical fact
Tensor energy normalization|E_GW=integral flux_action dA dt|Catalog radiated-energy consistency for derived G_tensor|Reuse GR energy posteriors with a changed kinetic coefficient
Vacuum scale source hierarchy|beta_i=beta_action(m_i,z_i,a0(rho_Lambda))|Shared-footing prediction across event masses and distances|Fit a0 separately for each binary
Joint likelihood portability frontier|effective reweighting sample size and support intersection|Which catalog events can test the candidate without strain refits|Trust a reweighted posterior with effectively one sample
''')
program('gw_distance', r'''
Tensor friction distance law|d_L^GW/d_L^EM=exp[0.5 integral nu_action(z)/(1+z) dz]|Action-derived gravitational luminosity-distance ratio|Adopt an arbitrary propagation parameter as a derivation
Population-redshift identifiability|p(m_det,d_L)=integral p(m_source,z)delta(m_det-(1+z)m_source)|Distance-law degeneracy with mass evolution|Treat spectral-siren redshifts as direct measurements
Galaxy-host mixture|p(z given localization)=sum_g w_g p(z_g)+p_missing|Catalog-completeness-corrected host redshift distribution|Assume every possible host is catalogued
Luminosity-weighted host bias|w_g proportional to selection and merger-host model|Host-weight uncertainty on propagation inference|Fix luminosity weights without testing source-population dependence
Distance-selection normalization|alpha(theta)=integral p_det p_population dsource|Selection correction for modified amplitude decay|Use the GR horizon distance for every propagation model
Mass-feature drift|m_peak(z)=m0+delta m(z)|Evolution bound preventing false propagation signal|Assume a universal mass feature while fitting a changing distance law
Hubble-friction degeneracy|J=[partial d_GW/partial H0,partial d_GW/partial nu]|Identifiable expansion/damping combinations|Claim two separately measured parameters from one rank-deficient direction
Low-redshift propagation expansion|Xi(z)=1+xi1 z+xi2 z^2+...|Local damping coefficient with truncation error|Extend a low-z series unboundedly to all sources
High-redshift saturation assumption|Xi(z)=Xi0+(1-Xi0)/(1+z)^n as diagnostic only|Sensitivity to phenomenological asymptotic shape|Identify Xi0 with a fundamental coupling without derivation
Inclination-distance covariance|p(d_L,i given strain) retained jointly|Orientation-marginalized propagation likelihood|Replace the distance-inclination banana by independent normals
Calibration-amplitude drift|h_obs=(1+g_run)h_true|Run-common systematic mode in d_GW/d_EM|Average away calibration uncertainty as number of events grows
Weak-lensing distance scatter|d_obs=d_true mu^-1/2|Magnification-marginalized propagation constraint|Set median and mean magnification corrections equal
Peculiar-velocity redshift correction|z_obs=z_cos+(1+z_cos)v_los/c|Nearby-host velocity floor on H0|Treat host redshift as pure cosmological expansion
Host photometric-redshift tails|p(z_g) multimodal with outlier component|Catastrophic-redshift effect on distance law|Use a single Gaussian for every host
Host catalog angular mask|p_missing(z,nhat) follows completeness map|Sky-dependent completeness bias in propagation|Assume a uniform missing-host fraction
Source-rate expansion coupling|dN/dz=R(z)dV/dz/(1+z)|Rate-distance consistency of the same cosmology|Fit event counts using a different H(z) than amplitudes
Electromagnetic-anchor reuse|L_joint avoids repeated GW170817 likelihood|Incremental dark-siren information beyond bright anchors|Multiply published combinations that share the same bright siren
Propagation-generation amplitude split|h_obs=A_emit_action/d_GW|Separate emission normalization from travel damping|Attribute changed source amplitude entirely to propagation
Tensor kinetic positivity|Q_T>0 and nu_action=partial ln Q_T/partial ln a where applicable|Distance-law parameter domain compatible with healthy tensor action|Permit damping parameters requiring negative kinetic energy
Tensor-speed timing bridge|c_T=c derived while amplitude damping varies|Amplitude constraints consistent with measured arrival-time sector|Infer superluminal pathology solely from amplitude damping
Coupling-ratio inference|Q_T tied to G_tensor distinct from G_N,G_E|Observable coupling matching from distance transport|Set all Newton symbols equal before fitting
Vacuum-linked damping history|nu_action[rho_Lambda,a0,background]|Propagation prediction on canonical and alternative footings|Change vacuum scale without solving the background
Population-likelihood prior transport|p_new/p_old includes source-frame Jacobians|Reusable likelihood domain of released posterior samples|Omit redshift-mass Jacobians in reweighting
Redshift-binned residual monotonicity|Delta_i=ln(d_GW/d_EM)_i|Data-supported damping-shape test with correlated bins|Enforce monotonicity solely because a chosen template has it
Common-action multimessenger cell|intersection of expansion,amplitude and source-generation constraints|One-cell GW distance compatibility certificate|Choose different action parameters for emission and propagation
''')
program('ringdown', r'''
Complex mode eigenvalue map|L_action(omega)psi=0 with ingoing/outgoing boundaries|Candidate quasinormal spectrum in observed mode sector|Use Kerr frequencies as a derived prediction of another action
Fundamental frequency residual|delta omega_220=omega_meas-omega_action(Mf,af)|Mass-spin-marginalized fundamental-mode deviation|Fix remnant mass from the same GR ringdown fit
Damping-time positivity|Im(omega)<0 in exp(-i omega t) convention|Measured damping compatible with candidate stability|Use the wrong Fourier sign to label growth as decay
Overtone identifiability|h=A0 exp(-iomega0t)+A1 exp(-iomega1t)|Resolved overtone amplitude after nuisance marginalization|Treat a second damped basis function as proof of a physical mode
Start-time stability|omega_hat(t0) with shared-data covariance|Time-window validity of linear ringdown inference|Count overlapping start-time fits as independent detections
Nonlinear merger leakage|h=h_linear+h_secondorder+h_transient|Bound on mode shifts caused by residual merger dynamics|Assume linear perturbation theory starts exactly at the peak
Higher-harmonic frequency ratio|omega_440/omega_220 cancels mass scale under stated metric|Dimensionless spectral ratio test|Fit unrelated remnant masses to separate harmonics
Mode mixing from spheroidal basis|spheroidalY=sum_l c_l sphericalY_lm|Angular-basis mixing correction|Compare spherical-mode amplitudes directly with spheroidal predictions
Remnant spin degeneracy|J=[partial omega/partial Mf,partial omega/partial af,partial omega/partial gate]|Identifiable gravity combination across complex modes|Report all three parameters from one complex frequency
Detector-coherent ringdown|h_d(t)=F_d^A h_A(t-t_d)|Coherent two-detector mode likelihood|Assign independent physical mode frequencies to detectors
Calibration phase near merger|h_obs=h exp[i phi_cal(f)]|Calibration bias on spectral phase and damping|Set calibration errors to zero because the event is loud
Noise-window covariance|Cov(t,t') from measured PSD and taper|Finite-window ringdown covariance|Use diagonal time-domain noise after spectral whitening errors
Peak-time uncertainty|p(t_peak) marginalized in mode amplitudes|Timing-induced overtone significance correction|Condition on a noisy peak time as exact
Echo boundary diagnostic|h_echo(t)=sum_n R_n h(t-n Delta t)|Boundary-reflection response permitted by derived candidate solution|Add echoes without a physical inner boundary
Horizon-flux balance|Mf=Mi-E_rad/c^2; Jf=Ji-J_rad|Independent remnant balance check|Use inconsistent energy flux and mode normalization
Area-growth conditional test|A(Mf,af) compared with initial areas only if horizons derived|Scope-correct horizon-area inference|Apply Kerr area formula to an unproved non-Kerr metric
Strong-field filter asymptotics|xi/r_g enters L_action|Controlled small-filter expansion of mode shifts|Use weak-field spatial convolution inside a relativistic horizon problem
Vacuum curvature mode correction|epsilon=Lambda_eff r_g^2|Bounded vacuum-induced spectral displacement|Replace curvature suppression with an arbitrary a0 force term
Carrier occupation near remnant|rho_carrier and perturbations solved with horizon boundary|Environmental-source mode correction|Assume a vacuum exterior while retaining an occupied carrier force
Matter-mode contamination|L_total couples metric and allowed matter perturbations|Classification of measured modes without adding gravitational DOF|Count an allowed matter mode as a third graviton automatically
Criterion-B characteristic compatibility|global time increases along every characteristic of perturbed solution|Causal interpretation of mode spectrum with preferred foliation|Demand every auxiliary channel lie inside the metric light cone
Mode-excitation source map|A_lmn=overlap(initial perturbation,adjoint mode)|Excitation-amplitude consistency with measured merger geometry|Fit arbitrary amplitudes then claim the merger mechanism was derived
Non-normal transient growth|norm(exp(tA)) can grow despite Im(omega)<0|Transient-energy bound over measured ringdown interval|Infer full stability from decaying eigenfrequencies alone
Inspiral-ringdown common-cell test|theta_inspiral and theta_ring share action and remnant balance|Combined strong-field compatibility with cross covariance|Multiply source posteriors extracted from overlapping strain segments
Two-footing observability ceiling|Delta omega=omega(a0_alt)-omega(a0_can)|Measured sensitivity ceiling for vacuum-scale normalization|Claim normalization discrimination below controlled waveform uncertainty
''')

program('shear_harmonic', r'''
Spin-two mask transport|C_tilde_l^EE=sum_L(M_lL^EE C_L^EE+M_lL^EB C_L^BB)|Full E/B mixing operator for the HSC harmonic window|Use a scalar-field mask coupling for spin-two shear
Pure-E boundary construction|W=grad W=0 at boundary removes specified ambiguous modes|Pure-E response and lost-mode rank|Assume apodization alone removes every ambiguous mode
Pixel window anisotropy|gamma_pixel=A_pixel gamma; Cobs=A C A^T|Pixelization-induced anisotropic shear response|Apply one isotropic pixel factor to an anisotropic sampling grid
Position-weighted noise subtraction|N_l from sum_g w_g^2 sigma_e,g^2/(sum_g w_g)^2 with angular response|Weighted shape-noise spectrum under the actual sampling|Use 1/n without shape weights or response factors
Mask cross-bin asymmetry|M_ij from W_i(nhat)W_j(nhat)|Tomographic cross-mask coupling matrix|Reuse one auto-mask matrix for every cross spectrum
E/B leakage covariance|Cov(C_E,C_B) from common masked modes|Residual B-mode calibration of E-mode uncertainty|Treat leaked B modes as statistically independent
Finite-angle excluded-mode operator|K_excluded=I-H_cut^+ H_cut on band-limited spectra|Harmonic gravity modes absent from the real-space cuts|Claim full equivalence of finite-angle and harmonic data vectors
Hankel closure residual|R=xi_measured-H_cut C_reconstructed|Correlated real/harmonic reconstruction residual|Multiply the two representations as separate surveys
Multipole-bin curvature correction|C_b=integral W_b(l)C_l dl differs from C_lcenter|Bandpower-center bias for a curved MONO response|Evaluate every spectrum only at the bin center
Apodization derivative commutator|grad(W gamma)-W grad(gamma)=(grad W)gamma|Boundary-gradient leakage into filter-scale inference|Drop derivatives of the apodization window
Disconnected-footprint mixing|M=M_N+M_S+M_cross on joint geometry|Cross-patch low-mode response|Set cross-patch cosmological covariance to zero by separation
Catalog rotation convention|gamma' =exp(-2i psi)gamma|Coordinate-invariant E/B spectrum check|Rotate sky coordinates without rotating the spin basis
Multiplicative calibration convolution|gamma_obs(n)=[1+m(n)]gamma(n)|Off-diagonal harmonic calibration response|Model spatial calibration as a diagonal amplitude
PSF cross-spectrum phase|C_gamma,PSF complex spin cross spectrum|Parity-resolved PSF contamination bound|Discard the imaginary/parity-odd cross response
Window inversion singular vectors|M=U Sigma V^T; small Sigma modes require bounded regularization|Identifiable harmonic subspace with regularization bias|Invert arbitrarily small singular values without error growth
Nonuniform galaxy sampling alias|gamma_sample(n)=sum_g w_g gamma_g delta(n-n_g)|Aliasing kernel for the measured source positions|Assume sources lie on a complete uniform grid
Tomographic harmonic noise cross term|N_l^ij from shared/migrating source membership|Noise covariance between probabilistic redshift bins|Set cross noise to zero when galaxies have shared bin weights
Pseudo-spectrum likelihood skew|p(C_tilde) departs from Gaussian at finite mode count|Likelihood-shape effect on large-scale gravity response|Use Gaussianity solely because the underlying shear is Gaussian
Mask-mode super-sample response|partial C_tilde/partial delta_b=M partial C/partial delta_b|Footprint-projected long-mode covariance|Apply a sky-fraction rescaling to every covariance term
Harmonic filter commutation domain|M F_xi differs from F_xi M for nonconstant angular response|Mask/filter commutator bound|Filter the observed pseudo-spectrum as if it were unmasked
Cross-estimator duplicate information|rank Cov(C_pseudo,C_pure,C_xi)|Effective number of independent representations|Add all estimator Fisher matrices without shared modes
Response-corrected B-mode upper bound|B_phys bounded after E-to-B leakage and additive response|Metric-compatible parity residual in measured multipole support|Subtract a best-fit leakage estimate with zero uncertainty
Band-limited source reconstruction|argmin_rho norm(M F_action[rho]-d)^2 subject to rho_b>=0|Source-profile null family under harmonic band limits|Claim unique spatial source recovery from finite bandpowers
Angular-to-physical scale mixture|p(k given l) proportional to source weights at chi=l/k|Physical-scale support of each measured harmonic bin|Identify one angular multipole with one physical acceleration
Harmonic-only vacuum information|F_cond=F_joint(C_l,xi)-F_xi using shared covariance|Vacuum-response information absent from real-space cuts|Interpret all harmonic precision as independent confirmation
''')
CONFIG['Y2023S09']['program']='shear_harmonic'

# These observation maps are obligations, not claims of already derived field equations.
DOMAIN={
'cmb_lensing':('Vary the pinned action for Phi and Psi separately, solve their unequal-time response, integrate null-geodesic deviation to convergence, and fold the actual reconstruction/mask response.','Released lensing bandpowers or maps, estimator response, multipole windows, noise biases, foreground templates, mask and their joint covariance; ancillary availability must be verified.','3, 8, 10, 13','Compare direct ray-displacement reconstruction with harmonic projection on an identical controlled potential; curl and frequency nulls must remain consistent.','an independently calibrated galaxy-shear or spectroscopic-velocity data vector with matched redshift weights'),
'shear':('Derive both metric potentials from the same filtered-MONO action; derive the Jacobi map, the source-redshift-weighted shear response and ellipticity measurement operator before fitting.','Measured shear correlations/bandpowers and windows, source-redshift distributions, shear/PSF calibration, intrinsic-alignment information and full bin covariance; do not start from S8 posteriors.','1, 3, 5, 8, 13','Compare real-space integration and harmonic projection of the same finite-window shear fixture, including a nonzero known calibration error.','independent CMB lensing or velocity measurements using the same physical redshift kernel'),
'joint_lss':('Derive ordinary-matter continuity/Euler equations and both metric potentials, then derive selected-galaxy clustering, projected lensing and their common-source covariance.','Published clustering and shear vectors with lens/source selections, redshift distributions, radial windows, occupancy/calibration ingredients and joint covariance; masses inferred under GR are derived products.','1, 3, 5, 8, 10, 13','Recover a known selected-tracer fixture by independent pair-count and Fourier projection, holding source occupation fixed.','spectroscopic velocity information or an independent gas/stellar baryon census'),
'timing':('Derive pulsar-clock proper time, endpoint Doppler terms and photon propagation from the same metric, followed by the measured timing-model projection and instrumental response.','Arrival times, observing frequencies, ephemerides, timing design matrices, backend flags, noise model and independent distance information where available; verify all archive fields first.','3, 4, 5, 6, 10, 11, 13','Compare integrated proper-time delays against direct differentiation into fractional-frequency shifts on an injected metric fixture.','independent astrometric distances or Galactic stellar accelerations'),
'pta':('Derive the two tensor propagating modes and their positive kinetic normalization, propagate them on the solved background, and integrate each pulsar photon path before timing-fit projection.','Measured timing residuals or released correlation likelihood, pulsar sky positions/distances, cadence, noise and timing-fit operators; obtain covariance rather than using one strain-amplitude posterior.','2, 6, 7, 8, 11, 13','Inject a known two-tensor correlated process and independent clock/dipole contaminant through the actual cadence; test recovery without changing the noise fit.','another pulsar array with shared arrival times/pulsars identified and common clocks modelled'),
'supernova':('Derive expanding-background dynamics and photon number/flux transport from the pinned action; map redshift and emitted luminosity into measured flux and light-curve observables.','Light-curve fluxes or released distance likelihood with redshifts, classification probabilities, selection model, calibration covariance and standardization population model; source access limits remain explicit.','5, 8, 10, 11, 13','Recover a controlled luminosity-distance fixture using both flux-space and Jacobian-corrected magnitude-space likelihoods.','ruler-free acoustic anisotropy or an independently calibrated distance anchor'),
'bao':('Derive the early-time acoustic ruler and late-time expanding geometry from the same action, then derive tracer displacements, redshift coordinates and the reconstruction/window observation map.','Acoustic correlation/multipole vector or dilation likelihood, tracer/redshift weights, reconstruction prescription, reference cosmology, window and covariance; imported rd priors require independent justification.','5, 8, 10, 13','Recover the same imposed anisotropic dilation from configuration-space and Fourier-space controlled acoustic fixtures.','relative supernova distances or an independently derived early-time acoustic calibration'),
'forest':('Derive gas conservation, thermal/ionization response and velocity gradients in the candidate metric, then photon absorption, continuum projection and acoustic redshift-space geometry.','Forest auto/cross-correlation vectors, sightline and quasar selection, continuum distortion matrices, absorber masks, wavelength/resolution calibration and full covariance.','5, 8, 10, 11, 13','Recover injected radial/transverse acoustic shifts with independent pixel-space and correlation-space forward models containing known continuum loss.','low-redshift galaxy BAO or independently measured gas-temperature/ionization constraints'),
'clustering':('Derive density and velocity perturbation kernels from the common action and conserved ordinary matter, then derive the selected tracer redshift-space statistics with the actual survey window.','Measured power-spectrum multipoles, tracer masks/weights, redshift-error model, window matrix, covariance and same-sample reconstructed BAO cross covariance if used.','1, 5, 7, 8, 10, 13','Verify a controlled displacement field by both particle transport and analytic redshift-space mapping; compare multipole conventions explicitly.','galaxy–galaxy lensing with matched tracer selection and shared-source covariance'),
'clusters':('Derive collapse, source occupation, gas support and metric-dependent photon counts from the action; construct a selection-normalized point-process likelihood in observed count-rate/redshift space.','Cluster count rates, extents, redshifts, exposure/selection and contamination functions, gas observables and shear calibration data with their correlations; do not regard GR cluster masses as raw input.','1, 3, 5, 8, 10, 13','Check a controlled selected Poisson-plus-correlated count fixture against direct integration of the observation intensity and preserve number/mass accounting.','independent thermal SZ pressure or resolved gas/stellar baryon measurements'),
'cluster_lensing':('Vary both potentials and solve the selected cluster-source field, then derive null-geodesic lensing, reduced shear and the crowding/redshift measurement response.','Cluster-centered tangential/cross shear, radial/source weights, X-ray selection and centers, source redshift/shape calibration and joint stack covariance; published mass summaries remain theory-conditioned.','1, 3, 5, 10, 13','Compare direct projected-potential shear with independent ray tracing of a controlled cluster and known centering offsets.','independently measured gas pressure and stellar light with hydrostatic assumptions explicitly tested'),
'gw_phase':('Derive compact-body motion, conserved binding energy, radiation flux, detector response and propagation from one action, with allowed matter sensitivities counted and no added radiating particle.','Calibrated event strain and noise spectrum, waveform likelihood/prior, detector calibration, frequency cuts and tidal/spin information; released GR posteriors are only conditional starting points.','2, 4, 5, 6, 7, 10, 11, 13','Compare time-domain energy-balance evolution with stationary-phase frequency prediction on the same controlled binary and detector noise.','independent radio-binary timing or another compact-binary event with comparable source structure'),
'map_stats':('Derive the nonlinear source/metric evolution and null-geodesic shear map, then reproduce map reconstruction, source sampling and the stated nonlinear statistic using the survey mask.','Measured lensing maps or summary vectors, masks, redshift/shape calibration, reconstruction response and training/validation metadata; GR simulation-trained posteriors cannot be treated as raw candidate evidence.','1, 3, 5, 7, 8, 13','Compare the statistic on direct noiseless potential projection and independently reconstructed shear maps, then add measured-like non-Gaussian shape noise.','an independently acquired lensing map or spectroscopic environmental tracer'),
'sn_lensing':('Derive the candidate metric lens map, flux transport and source-size/time response, and convolve the magnification distribution with selected intrinsic supernova luminosity and measurement errors.','Supernova brightness/colour/redshift residuals or their likelihood, outlier cuts, detection efficiency, intrinsic-scatter/calibration model and any verified foreground catalog; GR compact-fraction posteriors are not raw data.','1, 3, 5, 10, 11, 13','Verify flux/Jacobian normalization and extended-source ray tracing on the same controlled lens population before evaluating any tail statistic.','foreground galaxy/shear maps or independent stellar/remnant baryon inventories'),
'cmb':('Derive background, baryon/radiation perturbations and both potentials from the action, solve photon transport/recombination with stated ordinary matter, then fold lensing, bandpass, beam and mask response.','Measured TT/TE/EE cross spectra, multipole windows, calibration/beam/foreground nuisance likelihood and covariance; the reported LambdaCDM parameter posterior is not the input observable.','2, 3, 5, 6, 7, 8, 10, 13','Compare an independent transfer-function integration with direct evolution of a controlled acoustic mode, then project through the same spectral windows.','independent CMB lensing or acoustic-distance data with shared CMB/sky covariance retained'),
'foreground':('Derive gas pressure, electron momentum and photon scattering/emission response in the same metric; keep thermodynamic/astrophysical source laws as separately justified inputs and integrate real bandpasses.','Measured multifrequency spectra, foreground likelihood/covariance, flux cuts, bandpasses, beams, calibration and source/cluster masks; no uninspected template coefficient is asserted measured here.','1, 3, 5, 8, 10, 13','Recover known thermal and kinematic SZ signals through independent spectral integration and band-averaged matrix mixing, including a controlled correlated CIB component.','resolved X-ray/SZ gas profiles or independently selected cluster lensing'),
'shear_contrasts':('Derive one metric/shear operator, then apply each actual source selection and calibration operator; contrast only common physical modes and carry covariance of every shared galaxy/calibrator.','Published subset shear vectors or sufficient catalog selections, source-redshift distributions, masks, calibration and all cross-subset covariance; extract split definitions before computation.','1, 3, 5, 8, 13','Generate one sky realization with a known shared calibration shift, apply both selections and recover the predicted contrast with zero duplicate information.','independent survey shear or a foreground velocity/environment map'),
'gw_catalog':('Derive emitted tensor waveform, propagation and detector selection from the same action; construct a source-population point process without treating waveform-conditioned masses as direct observations.','Event strain likelihoods or supported posterior/prior samples, calibration, detection injections, observing time and candidate probabilities; raw-data/injection access has not yet been verified.','2, 5, 6, 7, 8, 10, 11, 13','Recover a selected synthetic source population using both event-level integration and injection-weighted rate normalization.','independent radio binaries or electromagnetic host/population observations'),
'gw_distance':('Derive tensor kinetic normalization and background propagation together with the source amplitude; derive photon distances separately from the same metric and preserve population/selection Jacobians.','Event distance–mass–orientation likelihoods, priors, selection injections, host redshift/completeness information and common calibration; source redshifts inferred statistically remain latent.','2, 5, 6, 7, 8, 10, 11, 13','Recover a known damping history through direct tensor propagation and luminosity-distance integration using an independently generated selected population.','supernova or BAO geometry with independent calibration and deduplicated bright-siren anchors'),
'ringdown':('Derive the remnant spacetime, allowed matter state and full perturbation operator with boundary conditions from one action, then derive mode excitation and detector-projected strain.','Calibrated event strain/noise, detector response, time windows, peak-time uncertainty and mode likelihood; extract any released posterior prior before reuse and distinguish GR remnant labels.','2, 5, 6, 7, 9, 10, 11, 13','Compare spectral eigenvalues with independent time-domain evolution of the identical controlled remnant and sign convention; preserve transient growth as well as asymptotic decay.','inspiral-derived remnant balance or another resolved black-hole mode event')
}

DOMAIN['shear_harmonic']=('Derive the same-action two-potential shear map, then the spin-two catalog sampling, pixelization and masked harmonic estimator; derive its joint response with the finite-angle real-space estimator.','HSC harmonic shear bandpowers, spin-two masks, source positions/weights, calibration and redshift selection, multipole windows, and joint covariance with the same-catalog correlation functions; fetch missing cross covariance or return a bounded dependency.','1, 3, 5, 8, 13','Compare direct spherical spin-two transformation and an independent finite-pixel estimator for identical injected E/B fields and the actual mask.','an independently acquired shear catalog or matched spectroscopic velocity map')

# Repeated observable domains receive a different estimand, not a changed label.
# q denotes the particular row's physical quantity, with its equation derived first.
VARIANTS={
'Y2023S02':('Frequency-differenced reconstruction response','Delta q_nu=q[95GHz TT]-q[150GHz TT]; C_Delta=C95+C150-C95,150-C150,95','frequency-contrast bias of','Use the two temperature reconstructions and their common-sky covariance; establish whether foreground response, rather than a changed Weyl field, produces the task-specific difference. Obtain channel products or explicitly stop that measured contrast.'),
'Y2023S08':('Finite-angle support functional','q_cut=O_q[H_cut C_l]; delta q_boundary=O_q[H_cut C_l]-O_q[H_extended C_l] with bounded unmeasured-angle completion','finite-angle completion bound on','Use the actual different xi-plus and xi-minus angular support. Optimize over admissible unmeasured-angle completions rather than pretend the truncated correlations determine the full harmonic field.'),
'Y2023S06':('Discrete-band correlation response','q_k=O_q[W_k C_ab W_k^T]; leakage_k=sum_j_not_k O_q[W_k C_j W_k^T]','discrete-frequency window and leakage contribution to','Use the CPTA reported discrete-frequency estimator and FAST cadence. Resolve the measurement-band response separately from broadband spectral extrapolation and calibrate adjacent-band leakage.'),
'Y2024S04':('Photometric-classification sensitivity','Delta q_class=q[p_Ia(d),S_host(z)]-q[p_Ia=1,S_host(z)]; propagate common light curves in Cov(Delta q_class)','classification-conditioned bias and identifiable remainder of','Build the photometric-class mixture and host-redshift selection into the DES-only likelihood, then estimate how uncertainty in those probabilities changes the specific physical quantity; the all-Ia counterfactual is a bias diagnostic, not a valid baseline.'),
'Y2024S07':('Close-pair noise-model influence','Delta q_close,m=q_m[all pairs]-q_m[pairs with a predeclared small-angle cut]; p(q)=sum_m p(q given m)p(m)','close-pair leverage and noise-model stability of','Predeclare the angular cut from geometry/noise rather than observed significance, retain covariance of nested pair sets, and compare the allowed noise models. This tests the measured MeerKAT sensitivity of correlation evidence to nearby precise pulsars.'),
'Y2025S03':('Conditional DR2 galaxy increment','e_q=q_DR2-C21 C11^-1 q_DR1; Cov(e_q)=C22-C21 C11^-1 C12 in a justified local linearization','DR2-only acoustic innovation in','Cross-match DR1/DR2 targets and disentangle new volume from reprocessing. For nonlinear q, derive the full conditional expectation before using this linear innovation; do not subtract independently estimated posteriors.'),
'Y2025S04':('Conditional DR2 forest increment','e_q=q_forestDR2-E[q_forestDR2 given DR1 sightlines]; V_q=Var(q_forestDR2 given DR1 sightlines)','new-sightline and revised-absorber contribution to','Separate new spectra, repeat spectra and absorber/continuum revisions. Carry the DR2 statistical plus theoretical-shift component and derive a conditional forest likelihood instead of multiplying two releases.'),
'Y2025S05':('Area-depth-calibration decomposition','Delta q=Delta q_newarea+Delta q_depth+Delta q_cal+Delta q_interaction; each contrast uses matched-object cross covariance','KiDS-Legacy area/depth/calibration decomposition of','Construct counterfactual reductions on the matched old footprint and nested redshift selections. If the archive does not permit a factor to be isolated, report the identifiable combined contrast and its precise missing-data dependency.'),
'Y2025S07':('Polarization-conditional acoustic information','q_polgivenT=O_q[d_TE,EE-E(d_TE,EE given d_TT)]; C_polgivenT=Cpp-CpT CTT^-1 CTp','SPT polarization-only conditional contribution to','Condition TE/EE on TT with the full common-sky covariance and then compare observing seasons; this isolates the additional deep-polarization response rather than rerunning the ACT all-spectrum estimand.')
}

OVERLAP_LINKS={
'Y2023S01':'Y2025S01 and Y2025S02 reuse ACT DR6 maps; lensing versus primary/foreground statistics require common-realization covariance.',
'Y2023S02':'Y2025S07 uses later SPT seasons on common sky; instrumental-noise increments are distinct from shared cosmic variance.',
'Y2023S03':'Shares DES Y3 with Y2024S06/Y2024S09 and KiDS ancestors with Y2025S05/Y2025S06; component data are not independent of the hybrid combination.',
'Y2023S04':'Y2023S05 uses the same NANOGrav observing realization; timing observables and background correlations are correlated summaries.',
'Y2023S05':'Y2023S04 is the companion arrival-time release; do not multiply its fitted timing likelihood with this background likelihood blindly.',
'Y2023S07':'Y2023S08/Y2023S09 share HSC galaxies; SDSS tracer additions permit only covariance-conditioned extra information.',
'Y2023S08':'Y2023S09 is harmonic analysis of the same HSC galaxies, and Y2023S07 reuses source shapes; finite-angle completion is this task family’s distinctive output.',
'Y2023S09':'Y2023S08 and Y2023S07 share HSC shapes; harmonic masks, ambiguous modes and conditional information are the dedicated outputs here.',
'Y2023S10':'Cross-match individual SNe against DES, Pantheon and any external distance compilation before combining; overlap is unknown until identifiers are inspected.',
'Y2024S01':'Y2024S03 measures broadband structure of the same DESI DR1 targets; Y2025S03 is a nested later release.',
'Y2024S02':'Y2025S04 reuses DR1 forest sightlines and shares quasar tracers with the galaxy BAO program.',
'Y2024S03':'Shares DR1 targets with Y2024S01 and the ancestor footprint of Y2025S03; BAO/full-shape covariance is required.',
'Y2024S04':'Y2024S10 uses the same DES five-year light curves; distance means and magnification-distribution shapes are conditional statistics.',
'Y2024S05':'Y2024S06 calibrates the same eRASS1 cluster selection with DES shear; count and calibration likelihoods share latent objects.',
'Y2024S06':'Shares selected clusters with Y2024S05 and DES source shapes with Y2023S03/Y2024S09.',
'Y2024S08':'GW230529 appears in Y2025S08 and potentially the selected propagation subset Y2025S09; event reuse must be checked by event identifier.',
'Y2024S09':'Reuses DES Y3 shapes also used in Y2023S03 and Y2024S06; non-Gaussian information is conditional on the two-point vector.',
'Y2024S10':'Shares SNe and calibration with Y2024S04; do not multiply residual-PDF and distance likelihoods independently.',
'Y2025S01':'Y2023S01 lensing and Y2025S02 foreground constraints share ACT sky/calibration; use one joint spectral model.',
'Y2025S02':'Same multifrequency spectra as Y2025S01, with overlap with Y2023S01 lensing maps; foreground parameters are not a new sky realization.',
'Y2025S03':'Nested DESI DR1 galaxy data Y2024S01/Y2024S03; all work orders here target conditional innovations.',
'Y2025S04':'Nested DESI DR1 forest Y2024S02; revisions and new sightlines are separated explicitly.',
'Y2025S05':'KiDS ancestors overlap Y2023S03; identical final galaxies underlie Y2025S06 subset contrasts.',
'Y2025S06':'Shares the entire final catalog with Y2025S05 and earlier KiDS area with Y2023S03; use matched-source contrasts.',
'Y2025S07':'Shares sky with Y2023S02 and potentially ACT footprints Y2025S01; condition on common CMB modes while retaining distinct observing-season noise.',
'Y2025S08':'Source catalog for Y2025S09, includes GW230529 from Y2024S08 and older GWTC events; keep an event registry.',
'Y2025S09':'Reuses selected events from Y2025S08 and includes a GW170817 anchor in the reported combination; remove repeated bright-siren likelihood factors.'
}

FOOTING=('Use a0=(c/2)sqrt(G_N rho_Lambda) with mass-density rho_Lambda; kappa=1/2, vacuum magnitude and filter are adopted inputs unless explicitly derived. '
         'Carry canonical 9.3619e-11 and alternative 1.1279e-10 m/s^2 separately. Keep G_N, G_E, G_bare and G_cosmo distinct until matching is derived; '
         'Lambda_eff=32pi(G_E/G_N)a0^2/c^4. Pin action revision, ordinary-matter coupling, S=exp[(xi^2/2)Delta], S* measure/domain/boundary, source gate and occupation. '
         'Filtered nu_mono is operative; Q/RAR/MU2 are comparisons only until a bridge is proved. No added particle species or per-object rescue parameters.')

# The source focus makes shared mathematical methods new measurement applications:
# outputs differ by the observing operator and the conditional/incremental data asked for.
# No claim is made that an abstract supplied a full executable likelihood.
TASKS=[]
for s in SOURCES:
    cfg=CONFIG[s['source_id']]
    name=cfg['program']
    mechanism,inputs,gates,positive,external=DOMAIN[name]
    rows=PROGRAMS[name]
    for j,(target,equation,output,mutation) in enumerate(rows):
        if s['source_id'] in VARIANTS:
            vtitle,veq,voutput,vscope=VARIANTS[s['source_id']]
            original_target,original_output=target,output
            target=f'{vtitle}: {original_target.lower()}'
            equation=f'Base physical quantity q: {equation}. Distinct measured estimand: {veq}'
            output=f'{voutput} {original_output.lower()}'
            # Retain both physical mutation and the variant-specific wrong independence premise.
            mutation=f'{mutation}; additionally, treat the correlated contrast/conditional components as independent'
        k=sum(t['year']==s['year'] for t in TASKS)+1
        tid=f'MY{s["year"]}-{k:03d}'
        nxt=rows[(j+1)%25]
        title=f'{cfg["label"]}: {target.lower()}'
        scoped=f'{output} for {cfg["label"]}, using its actual measured selection/windows and source-specific covariance'
        task=dict(
            id=tid,year=s['year'],source_id=s['source_id'],title=title,
            principle=f'{target} tests a distinct observable implication of a single gravity model. {cfg["focus"]} The proposed new result is {scoped}; the cited authors are not claimed to have performed this calculation.',
            math=f'{equation}. Define every symbol and domain in the derivation, derive this observation/estimand relation from the pinned action where physical, and audit its approximation order; a schematic relation here is a work obligation, not a completed theorem. Target: {scoped}.',
            measurement_input=f'Anchor {s["identifier"]}, first report {s["report_date"]}. {inputs} For {target.lower()}, extract the measured quantities entering {equation} and their correlated uncertainties. {s["data_access"]} If the necessary payload is unavailable, return an exact extraction dependency plus valid symbolic progress; never fabricate rows or covariance.',
            deliverable=f'{scoped}. Deliver a derivation, a machine-readable estimand/response definition, a covariance-aware measured constraint or explicitly conditional bound, and the controlled failure witness for the specified mutation. Record units, conventions, data hashes, model premises and whether an inference was executable. A missing action-to-observable map is a named unresolved implication, not an empirical success.',
            steps=[
                f'Pin {s["identifier"]}, the report/revision distinction, the common action and both acceleration footings. Extract the release fields needed for {target.lower()}, independently checking units, prior content, selection and shared observations; list unavailable payloads before numerical inference.',
                f'{mechanism} Derive the task-specific relation {equation}; identify each boundary, source-population and regularity premise needed for {output.lower()}.',
                f'Construct {scoped}. {cfg["focus"]} Identify the observable and nuisance directions mathematically; derive the conditioning/projection or likelihood normalization needed for this particular estimand, retaining a finite-data uncertainty or explicit nonidentifiability witness.',
                f'Implement the intentionally wrong control: {mutation}. Require a measurable rejection or explain why the available data cannot distinguish it. Independently check: {positive} Use a bounded analytic fixture or small reproducible prototype before any larger inference; a synthetic recovery is not observed evidence.',
                f'Write {tid} results to its own run directory when executed, with the exact {output.lower()}, covariance treatment, tested range and surviving assumptions. Separate theory derivation, numerical fixture and measured inference. State the precise input this supplies to gates {gates} and leave every unproved closure implication open.'
            ],
            controls=[f'Negative control (deliberately wrong; must fail): {mutation}.',positive,f'For {target.lower()}, compare the direct defining observable with the equation-based compressed result using identical input realizations; quantify disagreement and approximation error rather than reporting only a pass flag.'],
            first_principles=f'{mechanism} Specific obligation: establish {equation} in the measurement convention that yields {output.lower()}. {FOOTING} Published GR/LambdaCDM posteriors are conditional summaries, not theory-independent raw observations.',
            closure_bridge=f'This result can supply the observable implication {output.lower()} to amended thirteen-gate requirements {gates}, only for the identical action/parameter cell used elsewhere. Derive the observation map before any empirical closure claim. Count exactly two gravitational propagating degrees of freedom and any healthy allowed matter separately where relevant; stability uses criterion B (global preferred time, no backward-time paths, well-posed mixed problem). Neither a good fit nor classical consistency supplies a quantum completion or earns closure.',
            new_information=f'New measured-result objective: {scoped}. {cfg["focus"]} This is an application seeking this release-specific quantitative response/constraint, beyond generic old-AS methodological seeds; it does not claim a new universal mathematical method. The 2000-task manifest and AS1736 calibration seed were consulted for scope. The exact equation/output pair and source-conditioned inference, not merely the report label, define this obligation.',
            overlap_handling=f'Family {s["overlap_family"]}. {cfg["focus"]} These 25 work orders reuse one report and are not 25 independent datasets. Build an object/event/pixel/epoch overlap map before combining any related release; retain cross-covariance or use a conditional innovation likelihood, and exclude duplicate observations. Different summaries of identical samples are representation or conditional-information tests, not independent confirmation. Audit external-anchor reuse separately.',
            continuation=[
                f'Promising extension: combine the derived {output.lower()} with the distinct estimand {nxt[2].lower()} ({nxt[1]}) under a joint covariance, and determine which additional physical direction becomes identifiable. This is a new joint implication, not a second run of the same marginal fit.',
                f'Independent bridge: test the surviving {target.lower()} implication using {external}; derive the cross-observation map and common-data covariance before asserting agreement.',
                f'Failed-route repair: if the control "{mutation}" cannot be rejected, construct the exact nuisance/physical null direction that hides {output.lower()}, then specify the minimal independent calibration or missing field equation required to break it; preserve the original failure and do not change branches silently.'
            ],depends_on=[],priority='P0' if j in (0,1,11,24) else ('P2' if j in (15,16,20) else 'P1'),kind='derivation' if j in (0,1,3,10,23) else ('audit' if j in (6,13,18,22) else ('computation' if j in (7,8,9,16,19) else 'inference')))
        if s['source_id'] in VARIANTS:
            task['steps'][2]+=' '+vscope
            task['new_information']+=' Distinct estimand, not a report-name substitution: '+veq+'. '+vscope
            task['measurement_input']+=' Additional required extraction: '+vscope
            task['controls'].append('Contrast control: hold the physical sky/events fixed and alter only the explicitly isolated response/selection; the inferred physical component must remain invariant while the bias/innovation term changes as derived.')
        task['overlap_handling']+=' Known cross-source links: '+OVERLAP_LINKS.get(s['source_id'],'Check pulsar/event/object matches and shared calibrators against all external data before asserting independence.')
        TASKS.append(task)

required_source={'source_id','year','title','authors_or_collaboration','primary_url','identifier','report_date','date_precision','date_basis','version','observation_epoch','measurement','data_access','verification','source_locator','overlap_family','search_queries','checked_on'}
required_task={'id','year','source_id','title','principle','math','measurement_input','deliverable','steps','controls','first_principles','closure_bridge','new_information','overlap_handling','continuation','depends_on','priority','kind'}
assert set(DOMAIN)==set(PROGRAMS)
assert len(SOURCES)==30 and len(TASKS)==750
assert len({t['title'] for t in TASKS})==750
assert len({t['math'] for t in TASKS})==750
assert len({t['deliverable'] for t in TASKS})==750
for year in (2023,2024,2025):
    ss=[s for s in SOURCES if s['year']==year]
    tt=[t for t in TASKS if t['year']==year]
    assert len(ss)==10 and len(tt)==250
    assert len({s['primary_url'] for s in ss})==10
    assert [t['id'] for t in tt]==[f'MY{year}-{i:03d}' for i in range(1,251)]
    for s in ss:
        assert set(s)==required_source
        assert s['report_date'].startswith(str(year)) and s['report_date']<='2026-09-27'
        # Record the actual direct-page lookup, rather than inventing exact search text.
        s['search_queries']=[f'Direct primary-page lookup: {s["primary_url"]}']
    for t in tt:
        assert set(t)==required_task
        assert 4<=len(t['steps'])<=6 and len(t['continuation'])==3
        assert t['controls'][0].startswith('Negative control')
        assert t['source_id'] in {s['source_id'] for s in ss}
    (ROOT/f'{year}_sources.json').write_text(json.dumps(ss,ensure_ascii=False,indent=2)+'\n')
    (ROOT/f'{year}_tasks.json').write_text(json.dumps(tt,ensure_ascii=False,indent=2)+'\n')
    print(f'{year}: {len(ss)} authenticated source records, {len(tt)} proposed work orders')
print(f'{len(PROGRAMS)} domain-specific programs; {sum(len(r) for r in PROGRAMS.values())} distinct authored equation/output/control rows, applied to 30 report-specific observation operators')
