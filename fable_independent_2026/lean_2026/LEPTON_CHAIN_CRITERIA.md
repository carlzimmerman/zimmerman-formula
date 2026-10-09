# LEPTON_CHAIN: Lean certificate of the conditional lepton sector (frozen before any Lean)

**Owner's request (2026-10-09): "we need a Lean certificate on how particle physics works."**
Lean cannot certify that nature works a given way. It can certify which conclusions follow from stated assumptions, and which
assumptions are mutually or observationally incompatible. This file certifies the logic of atomos FS16 (TM1 + Dirac +
m_lightest = rho_Lambda^(1/4)) and of the record's kill results. It does not certify that the assumptions are true.

**Theorems to certify. Each must be proved with zero sorry and only the standard axioms.**
- L1 `tm1_s12_rule`: |U_e1|^2 = c12^2 c13^2 = 2/3 implies s12^2 = 1 - 2/(3(1 - s13^2)).
- L2 `tm1_s12_window`: TM1 with s13^2 in [0.020, 0.025] gives s12^2 in [0.3162, 0.3197]. The interval is a kill line: a 3 sigma
  s12^2 bound outside it excludes TM1.
- L3 `tm2_s12_floor`: TM2 (|U_e2|^2 = s12^2 c13^2 = 1/3) gives s12^2 >= 1/3.
- L4 `tm1_octant_decides_delta`, the main theorem. Take the PDG parametrisation with the first column built as complex numbers
  (U_mu1 = -s12 c23 - c12 s23 s13 e^{i delta}, U_tau1 = s12 s23 - c12 c23 s13 e^{i delta}), TM1 (|U_e1|^2 = 2/3,
  |U_mu1|^2 = |U_tau1|^2 = 1/6), all angles in (0, pi/2), and s13^2 < 1/5. Then sign(cos delta) = sign(s23^2 - 1/2): the upper
  octant forces cos delta > 0, the lower forces cos delta < 0, and maximal mixing forces cos delta = 0. The 1/5 is the
  (1 - 5 s13^2) factor.
- L5 `spectrum_sum_window`: m1 = 2.24e-3 eV, Dm21 in [7.38e-5, 7.62e-5] and Dm31 in [2.49e-3, 2.56e-3] give
  0.0609 < sum < 0.0620, which is below DESI DR2's 0.0642.
- L6 `mbeta_bound`: the same inputs with TM1's |U_e1|^2 = 2/3 and s13^2 <= 0.0228 give m_beta < 0.0095 eV. That is below
  Project 8's stated ~0.04 eV goal, so this output is not testable.
- L7 `mlight_scaling`: if a0 = kappa c sqrt(G rho) and m^4 = K rho with K > 0, then m^4 = K a0^2 / (kappa^2 c^2 G). For two footings,
  (m2/m1)^4 = (a0_2/a0_1)^2, so the lightest mass scales as sqrt(a0) at fixed kappa.
- L8 `dirac_no_0nubb`: definitional. If the Majorana mass matrix is zero, m_bb = |sum U_ei^2 m_i^Maj| = 0. It is labelled
  definitional, and it is not physics content.

**MUTATE (all must FAIL):**
- M1: L4 with s13^2 < 1/4 in place of 1/5.
- M2: L2's lower edge raised to 0.3190.
- M3: L5 with sum < 0.0605.

**Not certified, stated in the file header:**
- TM1 itself;
- that neutrinos are Dirac (FS11 rests on the unproven non-SUSY AdS conjecture and on numerics);
- m_lightest = rho_Lambda^(1/4) (a coincidence on its own);
- kappa = 1/2 (FITTED);
- the numerical delta values 262/285 deg (FS16 Python);
- the Delta(3n^2)/Delta(6n^2) no-residual-symmetry scans (FS01/FS03, Python);
- the experimental numbers, which are quoted inputs.

**Statement match:** after the build, an independent reviewer compares each docstring with its Lean statement (as in ChainCert).
Any mismatch is fixed in the docstring before commit.
