# TP05 canonical gravity: frozen handoff

Stopped at the user's immediate commit/push handoff request. No further science or Git actions were performed by this owner. Only this directory was written; TP01--04 and microscopic_vacuum_2026_10_28 remain immutable inputs.

## Completed

`CONTRACT.md` and `DERIVATION.md` record the exact canonical microscopic K,W+W0 action, its real D-flat tree SUGRA potential, the Euler-identity tadpole and the leading light-mode normalization. The linear-W0 term is -4fW0ReX/Mp²; all cubic terms cancel, so the heavy a,b normals have no source at that order. This cancellation and the Cartesian sigma-phase-phase cubic were independently reconstructed by the protected-gravity reviewer/coordinator.

The first finite experiment is **completed**: `shape.py`, `shape_contract.json`, and `run_shape/{manifest.json,result.json,stdout.txt,stderr.txt}`. All6 controls pass. The supplied v2 manifest validator was rerun immediately before this freeze and reports valid evidence with completed status. Runtime1.312seconds, observed RSS116.2MB, one numerical thread. No process remains running from this owner.

This run is the exact rigid one-loop CW shape plus the **leading tuned-W0 tilt**, with actual finite-splitting gaugino threshold masses sampled on that curve. It is not the full finite SUGRA calculation. At e=.003:

- Reference minimum t=R/R_CW=1.
- First phase-pair closure t=1.131962249924207.
- First restoring-force fold t=1.266739867062245.
- Fold mu=600578.1442GeV; photino at the fold26.131896keV.
- The old1MeV,e=.003 benchmark requires30.2553times the maximum restoring force and has no local vacuum on this sampled small-field branch.
- Actual phase-open and phase-closed point tables for e=.001,.003,.005,.01 are in result.json. At e=.003,t=1.160043920237347: mu=544147.7121GeV,R=84904313.4961GeV,m_sigma=.00644688626GeV,m_phase=.00397441389GeV,m_chi=.0000258434153GeV,m_3/2=1.26093638e-8GeV. This is a leading-tilt candidate input, not a certified full-SUGRA vacuum.

The threshold row's phase_open boolean and tiny nonzero width are numerical root-roundoff artifacts at exact equality; interpret the exact closure as zero two-body width. On either side the classification is resolved.

The actual canonical cubic is g_sigma_aa=(m_sigma²-m_a²)/(sqrt2R), giving Gamma=m_sigma³(1-m_a²/m_sigma²)²sqrt(1-4m_a²/m_sigma²)/(64piR²). Both gravity potential and polar kinetic vertices are required; the old massless width times phase space alone is insufficient. These equations and the available table have been communicated to the production owner.

## First unresolved step

Implement and verify the **finite completion** already specified in the contract: exact W0 tuning and microscopic heavy-normal stationarity, full finite TP03 two-loop reduced potential without double-counting CW heavy relaxation, and actual radial/angular metric corrections. Then recheck fold, phase threshold and admitted physical mass points. No numerical exact-SUGRA heavy-normal solve or finite V2 completion has been run here.

Also unfinished: full transverse SUGRA spectrum/super-Higgs normalization; finite gravitational/anomaly-mediated gaugino corrections with threshold decoupling; exact physical gravitino phase space; the separate canonical Planck-radius Polonyi regime; and final connection to production. The one-loop small-field table must not be promoted to these claims. Canonical matter plus Einstein SUGRA does not derive the repository's V3 khronon/P action, J(Y), preferred foliation or fitted kappa.

Raw F-energy=DE and tuned net gravitational energy=DE remain distinct. W0 cancellation is an input/tuning; it does not derive the observed DE scale or acceleration coefficient. The net residual needs enormous tuning and higher uncomputed corrections must be retuned, rather than interpreted as a DE prediction.

## Source read

The primary Kitano author PDF, *Gravitational Gauge Mediation*, hep-ph/0607090, August2006, was read through the web tool at https://inspirehep.net/files/18e90457969d0002c8c1e1de1a40dc2b ; equation(4), section2 provides the SUGRA potential and discusses the constant superpotential/R breaking. Its model's vacuum is not imported into this SU5 calculation. Direct arXiv PDF/HTML fetches failed; no full external source was downloaded or copied. Prior model/source records remain in microscopic_vacuum_2026_10_28.

Frozen files: this STATUS, CONTRACT, DERIVATION, shape.py, shape_contract.json and run_shape/. No further writes are planned from this owner for the handoff.
