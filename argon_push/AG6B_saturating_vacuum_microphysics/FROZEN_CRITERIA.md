# AG6B: what microscopic medium saturates at u → a₀/n, and does physics pick n? (frozen criteria, committed alone)

Written 2026-10-20, before any AG6B script, run or number. κ = ½ FITTED; both footings (9.3603e-11 / 1.1312e-10), never
pooled; no dark-matter particle species; not theory closed. Small jobs only (OMP_NUM_THREADS=1, nice -n 10, < 1 GB, minutes)
beside the live 1024³ run.

**Disclosure.** The candidate list below was drawn up after hand algebra on the two family members, for example that n=1 is
rational in g and n=2 is a hyperbola in g. No script was run and no number was computed before this file. Expected outcomes are
not written here.

## 1. The object being explained
PAPER49 (DOI 10.5281/zenodo.23501949) gives the action L = −|∇Φ−KP|²/(2K) − ρ_bΦ − W_rem(u) − (γ/2)|∇P|², with K = 4πG and
u = K|P|. At rest (γ → 0):
- g_N = R(u), with R ≡ K W_rem′(u);
- g = g_N + u, with g = |∇Φ|.

So the medium's constitutive law is the polarization response u = U(g), equivalently R(u) = U⁻¹(u) − u. The capacity family is
R_n(u) = u²/(a₀ − n u): n = 1 is the action's law (simple μ), and n = 2 is the quadratic a₀-line, which is Milgrom 1999 eq. 9
(equation book, 07-16).

## 2. Admissibility (applied identically to every candidate)
- **A1, criticality:** U′(0) = 1, i.e. R has no linear term. This is inherited from the action's self-gravity cancellation
  (PAPER49 §3). It is imposed on every candidate as one shared condition and is not counted against naturalness.
- **A2, deep law:** lim g_N/(g²/a₀) = 1 as g → 0. The candidate's one internal scale must be fixable by this. If the leading
  small-g behaviour is g_N ∝ g^p with p ≠ 2, A2 FAILS, and p is reported together with the rotation-curve slope.
- **A3, finite capacity:** u_max = U(∞) < ∞. Define n_cap ≡ a₀/u_max.
- **A4, stability:** R′(u) > 0 on (0, u_max).
- **A5, data (CFG4 H2 C2 line):** rms ≤ 0.110 dex with Υ_disk in 0.50–0.80 on **both** footings, on raw SPARC with the CFG4
  statistic, through a read-only import of CFG4_common, exactly as in CFG695 S2.
  - An in-family n=1 candidate inherits CFG695's PASS. It is re-run here as control K1.
  - An in-family n=2 candidate uses this lane's own run of the AG4b K1 global scan, as control K3.
  - Out-of-family candidates are scored by this lane.
  - A candidate whose a₀ is fixed by Λ is scored at that a₀.

## 3. Classification of a candidate's law
For each candidate, write R(u) = (u²/a₀)·f(u/a₀) and report:
- n₁ ≡ f′(0);
- n_cap;
- the wall type at u_max (simple pole / other pole / log / finite-field hard saturation);
- **in-family** iff R(u)·(a₀ − n_cap u) − u² ≡ 0 symbolically (sympy simplify). Numerically, the condition is a relative residual
  < 1e-10 on 200 points in (0, 0.999 u_max).

## 4. "Natural" (frozen)
A candidate is **natural** iff all of the following hold:
1. Its response follows from one microscopic rule taken from a named physics domain and stated without reference to the target law.
2. It has exactly one dimensional scale beyond the field, and A2 fixes that scale.
3. It has no free function.
4. Every discrete modelling choice is listed below in advance.

A candidate is **by construction** (never a derivation) if a function, or a mixing shape, was chosen to hit the family. Free
choices are counted and printed for every candidate.

## 5. Candidates (microscopic rules frozen here)
**Class A: analytic equilibrium media.** Isotropic, with free energy analytic in the vector field at zero.
- A-1 Langevin classical dipoles: u = u_s L(g/g_T), L = coth − 1/x.
- A-2 Brillouin spin-J: B_J for J = ½ (thermal two-level, tanh), J = 1 and J = 3/2.
- A-3 Landau para/ferroelectric at criticality: R = b u³ (+ c u⁵).
- A-4 Born–Infeld vacuum, both identifications:
  - (i) g ↔ E with u = D(E) − E (sign-flipped to anti-screen);
  - (ii) the field-limited branch u = E(D) with D ↔ g.
- A-5 Euler–Heisenberg weak field (massive loops): energy E²/2 + ζE⁴.
- A-6 Ginzburg–Landau superfluid depairing: j = ρ_s v(1 − v²/v_c²), current ↔ u, flow ↔ g.
- A-7 freely-jointed polymer chain (inverse-Langevin spring), extension ↔ u, force ↔ g.
- **General theorem T-A (sympy):** any U(g) = χ(g²)g with χ analytic has g − U = O(g³) once A1 holds. Report the deep exponent
  and V(r).

**Class B: scale-free non-analytic power media.** W ∝ |u|^q, so R ∝ u^{q−1}.
- B-1 degenerate Fermi carriers in d dimensions: E ∝ n^{1+2/d}, u ∝ n; d = 1, 2, 3.
- B-2 massless Euler–Heisenberg in D spacetime dimensions: L ∝ |eE|^{D/2} by dimensional analysis; D = 4 (log), 5, 6.
- B-3 thermal bosonic zero-mode cubic −(T/12π)(m²)^{3/2} with m² = λ|P|²: report the sign.
- Report which q gives A2 (CFG690: q = 3). Scale-free media have no capacity, so A3 fails unless a band supplies one (Class D).

**Class C: kinetic, driven single-occupancy cells.**
- C-1 Langmuir / Michaelis–Menten / incoherently pumped two-level saturation: the fill rate is α|g|^p(1−θ), the emptying rate is
  βθ, and u = u_m θ_ss. Frozen choice p = 1 (an incoherent thermal pump with rate ∝ T_U ∝ |g| in the high-occupation limit).
  Report what A1 forces on p.
- C-2 Hill-cooperative form θ = y^h/(1+y^h) for h = ½, 2.
- C-3 Caughey–Thomas velocity saturation, 1/U^β = 1/g^β + 1/u_m^β with β free: report what A2 forces.
- C-4 coherent (Rabi) pump, s ∝ g².
- C-5 Unruh–Langmuir scale tie: the C-1 saturation field equals the horizon acceleration a_H. On the canonical footing
  a_H = cH_Λ = Z·a₀; on the alt footing a_H = cH₀ = Z·a₀_alt, with Z = √(32π/3). A5 is scored at that a₀.

**Class D: lattice Pauli capacity.**
- D-1 spinless fermions in 1D tight-binding channels along the field. Filling n ≤ 1/a, u ∝ n, and R ∝ the band's chemical-potential
  rise. The model has two scales, the hopping t and the capacity. Report the continuum limit, the wall type and whether n is fixed.

**Class E: relativistic / Deser–Levin quadrature.**
- E-1 g_N = √(g² + m²) − m: the Milgrom 1999 ΔT ansatz, equivalent to the mass-action law n_e(n_e + 2g) = m². A2 fixes m.
- E-2 the dS tie m = a_H (Milgrom's literal scale). A5 is scored at a₀ = 2a_H on each footing. The equation book already records
  this as excluded; it is re-run here as a control, not as a new result.

**Class F: reversible finite-capacity cell ensembles.** Critical "clipping" cells u_c(g) = min(g, c) with a capacity spectrum
p(c), as for hard-axis Stoner–Wohlfarth-type cells.
- **T-F1 representation (sympy):** U = ∫min(g,c)p(c)dc ⇔ p = −U″. Report p for n=1 and n=2. A2 ⇔ p(0) = 2/a₀, and
  n_cap = 2/(p(0)⟨c⟩).
- **T-F2 bound:** p with non-decreasing hazard (IFR, which includes every log-concave p) ⇒ n_cap ≥ 2, with equality iff p is
  exponential. Proved symbolically and checked numerically on 6 spectra.
- Natural spectra, scored on A1–A5:
  - F-1 exponential (MaxEnt at fixed ⟨c⟩);
  - F-2 half-normal (MaxEnt at fixed ⟨c²⟩);
  - F-3 uniform on [0, c_max];
  - F-4 identical cells (a delta spectrum).
- F-5 the in-family spectra written as superstatistics (an exponential with a Gamma-distributed rate; a half-normal with a
  Gamma-distributed precision). Pre-classified **by construction**: the mixing shape is chosen to hit the family.

**Closed doors (cited, not re-run).** Berezhiani–Khoury X^{3/2} superfluid (condensate μ-pincer, superfluid route G2), the v9 DBI
dark sector, Verlinde (CFG117), Born screening (CFG665), CFG690's SI law ν = 1 + y^{−1/2}, CFG695 (the saturation itself,
post hoc), the dS-Unruh kernel (MI_KERNEL_FROM_DSUNRUH 06-19) and the equation book's M99 ↔ n=2 scale failure. Information-capacity
"bit cells" are mapped onto C-1 (kinetic) or onto a thermal Fermi cell (scored as C-6 below). They are not a separate class.
- C-6 thermal Fermi single cell, θ = 1/(1 + e^{(ε₀ − d|g|)/T}): A1/A3 as computed.

## 6. Second predictions (computed for every candidate passing A1–A4)
- **S-a capacity:** u_max/a₀ and Σ̄_max = u_max/(πG) in M☉/pc², on both footings.
- **S-b high-field tail:** (u_max − U)/a₀ at x = g/a₀ = 3, 10, together with its functional form (power or exponential).
- **S-c conservative P-wave gap:** ω₀²/(4πGρ_c) = R′(U(g)) at x = 0.1, 1, 10. This is the medium's own small-oscillation gap with
  the PAPER49 inertia |Ṗ|²/2ρ_c (longitudinal: δA = 0, so only W_rem″ restores).
- **S-d kinetic relaxation rate:** Γ(x)/Γ(0) for the kinetic realisations (C-1; and E-1 read as mass action with recombination).
- **S-e above-capacity behaviour:** the wall type (pole / log / finite-field saturation), and g_N at which u reaches 99% of u_max.
- **S-f scale:** only C-5 and E-2 fix a₀ from Λ. Report the predicted/footing ratio.
- **Discriminator rule (frozen):** for each pair of candidates passing A1–A5, report the S-quantity with the largest ratio between
  them. Also report the largest |Δlog g| between their static laws over x ∈ [0.01, 100], after a free a₀ rescale. Label a
  discriminator TESTABLE-NOW only if the data needed are public and on disk. Otherwise label it NOT TESTABLE NOW and name the data.

## 7. Verdict (frozen)
- **DERIVATION** iff exactly one natural candidate passes A1–A5 and lies in the family (so n is fixed), every other natural
  candidate fails, **and** it carries a second prediction with no new constant.
- **CANDIDATE** iff at least one natural candidate passes A1–A5, but n is not unique across the natural passers, or the second
  prediction needs a free constant or timescale.
- **SCOPED NO-GO** iff no natural candidate passes A1–A5 (scoped to classes A–F).
- **NOT DIAGNOSTIC** iff admissibility cannot be computed.
- Attached statements, which do not change the class:
  - the Class A theorem, as a scoped no-go on analytic dielectric saturation;
  - the T-F2 bound.

## 8. Controls (exit 1 if any fails)
- **K1:** this lane's numerical-inversion SPARC solver, fed U₁(g) = a₀g/(a₀+g), reproduces cfg695_results.json S2: rms within
  1e-6 and Υ exact, on both footings.
- **K2:** CFG4 ν_mono H2 is reproduced (rms within 1e-6, Υ exact), from CFG4_galaxy_law_results.json.
- **K3:** the n=2 global scan reproduces AG4b `controls/K1_n2_reported` (0.10827 @ 0.70 / 0.10355 @ 0.65): rms within 5e-5 and
  Υ exact.

## 9. MUTATE (`AG6B_MUTATE=1`, writes `_MUTATE` outputs, exit 1 iff every tooth bites)
- **Mu1:** C-1 with the coherent pump p = 2 must fail A1 or A2.
- **Mu2:** E-1 with m = a₀ (not a₀/2) must fail A2, with coefficient ≠ 1.
- **Mu3:** the family test on C-1 at n_cap + 1 must return not-in-family.
- **Mu4:** the Class A analytic test applied to C-1 (non-analytic) must not fire.
- **Mu5:** SPARC with ν = 1 must give rms ≥ 0.25.
- **Mu6:** T-F1's n_cap computed from p₁ but checked against U₂ must mismatch.
- **Mu7:** T-F2 applied to the decreasing-hazard Lomax(2) spectrum must show n_cap < 2, so the bound is not vacuous.

## 10. Rules carried
- Every number comes from a committed-later script on disk with its output.
- Web facts are PROVISIONAL unless verified in the primary text.
- No file outside this folder is edited.
- Results are not committed by this lane. Only this file is committed, alone.
