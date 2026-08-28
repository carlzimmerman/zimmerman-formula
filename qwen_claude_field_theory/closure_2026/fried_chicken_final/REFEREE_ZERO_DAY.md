# REFEREE_ZERO_DAY — Hostile Objections to the FC-FINAL Verdict

Winner under attack: **A = AeST (Skordis–Zlosnik, 6 DOF) + frozen J_10**, adjudged CONDITIONALLY-VIABLE;
program verdict **INCONCLUSIVE**. Each objection: **CLAIM** (hostile), **EQUATION/BASIS**, **RESPONSE**,
**RESIDUAL** (what honestly survives). No objection is answered by asserting a PASS. Where an objection lands,
it is booked OPEN/FAILED, not spun.

Basis labels: THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED.

---

### A. Covariance, foliation, preferred frame

**O1. "AeST has a preferred foliation; it is not generally covariant, so PPN preferred-frame effects are fatal."**
- EQ: unit aether A_μA^μ=−1 picks a timelike congruence; α_1=−4K_B, α_2=α_2(K_B,K2,Q0)≠0 generically.
- RESPONSE: True that a preferred frame exists — that is WHY α_1, α_2 are the sharp tests, not γ. α_1=−4K_B is
  DERIVED (fc_ctensor_map_2026.py) ⇒ LLR forces K_B<2.5e-5, a bound not a kill.
- RESIDUAL: **α_2 coefficient OPEN** (Gate 10). If α_2~K_B/2, LLR pushes K_B<4e-8 — tighter but still a bound.
  Only FAILS if α_2 is O(1) independent of K_B, which the c123=0 regularisation theorem argues against but
  does not yet compute. Booked OPEN-adverse.

**O2. "The action is diffeomorphism-covariant only formally; the aether breaks boost invariance, so 'A retains
H_perp' is sleight of hand."**
- RESPONSE: The Hamiltonian constraint H_perp is present as a first-class generator of the *full* 4-diff
  algebra of the covariant action; the aether is a dynamical field, not a fixed background structure, so
  boosts act on it. This is categorically different from B/C, where H_perp is DELETED and replaced by a
  source-free spatial-scalar constraint (fc_no_go_Hperp_unsources_Phi.py).
- RESIDUAL: none for the DOF-counting claim; the boost-violation shows up physically as α_1,α_2 (O1), not as a
  lost constraint.

**O3. "A preferred foliation with a superluminal scalar (Gate 5) means the theory has closed timelike curves
or an ill-posed Cauchy problem."**
- EQ: c_s²∝1/K_B → ~3c at the K_B ceiling.
- RESPONSE: A preferred foliation can be causally consistent IF a global time function exists whose level
  sets all characteristic cones respect (Khronometric/Hořava logic). AeST plausibly has one.
- RESIDUAL: **OPEN, real liability.** We have NOT derived the global-time causal-structure argument; asserting
  it would violate the rules. Gate 5 stays PARTIAL/adverse. HOST (K2/aether), kernel-blind.

---

### B. Degrees of freedom, ghosts, Legendre

**O4. "The 6-DOF count is EXTERNAL-INPUT, not re-derived; you are trusting PRD 110.044015."**
- RESPONSE: Correct and disclosed — Gate 2 is labelled EXTERNAL-INPUT, not PASS-derived. FC's Y>0 branch is
  shown byte-in-class (F_QQ=2K2≠0, F_YQ=0, F_YY>0), so the published general-F theorem applies.
- RESIDUAL: independent in-repo re-derivation of the full constraint algebra is OPEN. Not a claimed pass.

**O5. "The frozen J_10 adds a new propagating ghost through the sharp n=10 kernel."**
- EQ: δ²S_MOND with F_M=(2/3a0)Y^{3/2}+…; the Y^{3/2} start means δ²F_M=0.
- RESPONSE: THEOREM (fc_A_certificate.py CERT2, exit 0): δ²S_MOND=0 for ARBITRARY admissible prefactor J ⇒
  J_10 adds NO quadratic mode ⇒ no new ghost. The −(2−K_B)Y kinetic seed keeps the Y=0 gradient sector
  positive (bare AQUAL would strong-couple; AeST does not).
- RESIDUAL: none at quadratic order. Nonlinear/interacting-vacuum ghost concern folds into Gate 14 (O16).

**O6. "detC→0 at Y=0 is a Legendre breakdown — the theory is singular where MOND matters most (deep field)."**
- EQ: detC_aux ∝ K2/(2a0√Y) → ∞... actually →0 in the aux chart as Y→0.
- RESPONSE: The Y=0 zero is a singularity of the AUXILIARY Legendre chart, not the physics: the physical
  gradient Hessian H_phys(Y=0)=2(2−K_B)I>0 (y0_physical_hessian.py, 5/5). Deep-MOND (small g, but Y grows
  with the potential gradient) is not the Y=0 point.
- RESIDUAL: **all-branches covariant Dirac regularity theorem OPEN** (Gate 3). Referee-vulnerable on the
  singular boundary, but no known pathology. Booked PARTIAL.

**O7. "Y=0 is exactly the cosmological background (isotropy ⇒ spatial gradients vanish), so your fragile point
IS the background you must live on."**
- RESPONSE: Yes — on FLRW Y=0 and J_10 drops out entirely (Gate 7, flrw_fc8.py). The background physics is
  carried by K(Q), not the MOND sector. H_phys(Y=0)>0 keeps the gradient sector healthy.
- RESIDUAL: the fragility on the background is NOT the Legendre point — it is the IR scalar mode (Gate 14, O16).

---

### C. k=0 / homogeneous sector, dark energy, numerology

**O8. "w=−1 is asserted, not derived; K(Q) is tuned to give dS."**
- RESPONSE: Correct and flagged. K(Q) generic near its minimum is DUST-like (shift charge K_Q∝a⁻³, the nbody
  obstruction). −K(Q)=ρ_DE holds only AS AN IDENTIFICATION at the dS minimum. w=−1 EXACT and a0 CONSTANT hold
  only there; an evolving a0(z)∝√ρ_DE is NOT derived (open inverse-K(Q) problem).
- RESIDUAL: MODEL-ASSUMPTION, disclosed. Not used as a pass anywhere.

**O9. "a0²=κ²c²Gρ_Λ and Λ=32πa0²/c⁴ are pure numerology — that is your whole 'result'."**
- RESPONSE: Explicitly labelled TARGET/phenomenological INPUT and MODEL-ASSUMPTION throughout; κ=½, Z≈21 are
  FITTED. The closure filter does NOT rest on the numerology — a0 is carried as a constant input; the winner's
  physics (c_T, γ_PPN, lensing, DOF) is a0-magnitude-independent.
- RESIDUAL: the numerology remains unexplained. It is the one place CONDITIONALLY-CLOSED could have applied —
  but it does NOT, because unresolved *consistency* conditions (O16, O1, O3) sit above it. Booked as the
  program's genuine phenomenological input, not a derivation.

**O10. "The dust-like shift charge K_Q∝a⁻³ means your 'dark energy' field is really dark matter — you have
double-dipped."**
- EQ: a³K'(Q0)=−2K2C=const ⇒ Q0=q_m−C/a³.
- RESPONSE: This is the KNOWN dark-sector tension (MEMORY: DE triumph and galaxy problem = same property). The
  filter does not claim the K(Q) sector supplies galaxy-scale dark matter; MOND (Y-sector) does the galaxies,
  K(Q) does the background. The a⁻³ piece is background-only (cannot cluster at linear order without the IR
  mode of O16).
- RESIDUAL: whether K(Q) can be BOTH dS-attractor AND acceptable early-density is the open inverse-K(Q)
  problem. OPEN, disclosed.

---

### D. Matter coupling

**O11. "Show matter conservation survives — B fails it at Newtonian order; why not A?"**
- EQ (B): ∇_μT^{μi}=−ρD^iX (gate_matter_conservation_derivation.py, FAIL).
- RESPONSE: A couples matter minimally to g_μν only (Gate 8). Bianchi ⇒ ∇_μT^{μν}=0 identically; there is no
  constraint-architecture deletion sourcing an anomaly. This is exactly the structural difference from B/C.
- RESIDUAL: none at the level of the coupling. (Fifth-force/Cassini enters through the field EOM, O30, not
  through non-conservation.)

**O12. "The scalar couples to matter through the disformal/aether sector and generates a fifth force in the
solar system."**
- RESPONSE: In AeST the scalar couples to matter only gravitationally (through g_μν); the MOND force is the
  metric response. In the deep-Newtonian regime μ_10→1 (F_M→linear), so the extra scalar stress decouples;
  γ_PPN=1 (Gate 11) is the certificate that no anomalous slip/force appears at 1PN.
- RESIDUAL: α_2 (O1) is the surviving 1PN preferred-frame residue; β (2PN) OPEN-benign.

---

### E. GW speed, tensor sector

**O13. "GW170817 requires |c_T−1|<1e-15; your c_T=1 is only tree-level / Minkowski."**
- EQ: c1+c3=0 ⇒ c_T²=1; certified by fc_ctensor_map_2026.py map (c1,c2,c3,c4)=(K_B,0,−K_B,0).
- RESPONSE: c_T²=1 is EXACT and K_B-/kernel-independent because the TT sector reduces to Einstein–Hilbert
  (F_μν=J=Y=0 on the background) — not a tuned cancellation. Holds on FLRW (fc_flrw_quadratic_gate.py).
- RESIDUAL: none for A. (Contrast D: c_T²−1=+3.9e-2 for the DW-khronon chassis, O37.)

**O14. "The aether kinetic F_{μν}F^{μν} generically shifts c_T; you must have tuned c1+c3=0."**
- RESPONSE: c1+c3=0 is FORCED by the specific AeST kinetic structure (−(K_B/2)F_{μν}F^{μν} maps to
  (c1,c3)=(K_B,−K_B)), an identity, not a tuning (fc_ctensor_map_2026.py: simplify(c1+c3)==0). This is a
  designed feature of the SZ action, inherited by FC.
- RESIDUAL: none.

---

### F. Superluminal scalar / hyperbolicity (the real liability)

**O15. "c_s²~1/K_B → ~3c is a superluminal scalar — GW170817-class kill for the scalar characteristic."**
- RESPONSE: GW170817 constrains the TENSOR speed (c_T=1 exact, O13), not the scalar. A superluminal scalar
  characteristic is NOT automatically excluded in a theory with a preferred foliation (it can be causal w.r.t.
  a global time). BUT we have not derived that argument.
- RESIDUAL: **OPEN, real (Gate 5).** Adverse. HOST (K2), kernel-blind. Honestly the sharpest live liability
  after O16. Not spun to a pass.

---

### G. IR mode / FLRW perturbations (DECISIVE)

**O16. "AeST's low-k Hamiltonian is unbounded below (arXiv 2109.13287) — a cosmological ghost. Fatal."**
- EQ: H unbounded for k<k_*, k_*²=(1+λ_s)/λ_s·μ², μ²=2K2Q0²/(2−K_B).
- RESPONSE: This is the DECISIVE gate (14), and it is booked OPEN, not resolved. The closure lane
  (fc_flrw_ir_sign_certificate.py, 20/20) PROVED the **k→0 limit is rescued** on the dS attractor: shift
  symmetry ⇒ exact flat direction; on dS the a³ measure + 3H friction give χ̇~a⁻³, χ→finite const (bounded),
  energy E~a⁻³→0 (Minkowski control: χ=(Π/K0)t secular, E const — reproduces 2109.13287). The negative energy
  is diluted, the secular growth cut off — **at k→0 only.**
- RESIDUAL: **finite-k band H≪k_phys<k_* (≳1 Mpc) UNCOMPUTED.** Dichotomy: (a) nondynamical/constraint
  throughout ⇒ rescue ⇒ PASS; (b) dynamical ω²<0, |ω|~k_phys≫H ⇒ Mpc-runaway ⇒ FAIL. Deciding it needs the
  full S^(2)_FLRW scalar action incl. k⁴ terms regulating the K_eff=0 strong-coupling crossing. **This single
  number promotes A to VIABLE or kills it.** Kernel-blind (δ²J_10=0, HOST).

**O17. "Even if k→0 is bounded, the K_eff=0 crossing at k=k_* is a strong-coupling / infinite-coupling point —
the EFT breaks down there."**
- RESPONSE: Correct — K_eff→0 at k_* means the quadratic kinetic term vanishes and higher-gradient (k⁴) terms
  take over; the effective description is strongly coupled at that scale. This is exactly the residual open of
  Gate 14 (P6 in fc_flrw_ir_sign_certificate.py, labelled OPEN).
- RESIDUAL: **OPEN.** The k_* strong-coupling scale is the same object RESULTS.md lists as "μ far-field /
  strong-coupling scale". Not resolved.

**O18. "The mode is 'secular' — linear-in-t growth is still growth; you cannot call that stable."**
- RESPONSE: On Minkowski, yes (χ=(Π/K0)t). On the EXPANDING background the a³ redshift converts secular growth
  to χ→finite const (O16). Secular-on-Minkowski ≠ secular-on-FLRW. That IS the content of the k→0 rescue.
- RESIDUAL: only established at k→0; finite-k (O16) open.

**O19. "You need CMB/growth confrontation (S8, ISW); you have none."**
- RESPONSE: True. Linear perturbation confrontation requires closing Gate 14 first (the scalar sector's sign
  and dynamical status). Until then CLASS/Boltzmann is not runnable for FC-FINAL at the level needed.
- RESIDUAL: **OPEN.** No S8/ISW claim is made. (MEMORY: S8 neutral-by-theorem for the GDM degeneracy, but that
  is the fluid-not-particle statement, not a growth computation for this action.)

**O20. "Interacting quantum vacuum with any K_eff<0 patch decays catastrophically (Cline-Jeon-Moore)."**
- RESPONSE: The classical rescue (O16) dilutes the negative-energy mode; the quantum-vacuum concern dissolves
  IF branch (a) holds (mode nondynamical for k<k_*). If branch (b) holds it is a genuine additional problem.
- RESIDUAL: **OPEN, contingent on O16.** Disclosed.

---

### H. Lensing, clusters

**O21. "Modified gravity generically gives Φ≠Ψ (slip); your KiDS fit is a coincidence."**
- EQ: d_id_j(Ψ−Φ)=8πG̃(T_ij)_{i≠j}; pressureless matter ⇒ no off-diagonal stress.
- RESPONSE: DERIVATION (fc_nonspherical_lensing_slip_2026.py, 14/14, exit 0): for a GENERIC non-spherical weak
  source every AeST-field off-diagonal stress is O(ε²) (Y-sector prefactor, aether Maxwell O(ε²), mixing
  killed by A^μA_μ=0 unit-norm identity, Q-sector isotropic) ⇒ Φ=Ψ, |γ−1|=O((v/c)²)~1e-6, kernel-independent.
  Not a coincidence — a HOST property of minimal+derivative coupling; shift symmetry forbids the φR term that
  would give O(1) slip.
- RESIDUAL: O(ε²) slip magnitude/sign uncomputed (~1e-6 completeness); full nonlinear covariant BVP OPEN.

**O22. "Lensing mass ≠ dynamical mass in MOND ⇒ Bullet Cluster kills you."**
- RESPONSE: Because Φ=Ψ exact and the deflection uses the SAME g_obs=μ_10 as dynamics (Part 4), lensing mass =
  dynamical mass — there is no dark-lensing lever to over/under-produce, hence no Bullet-type offset kill.
- RESIDUAL: the standard-MOND cluster residual η(R500)~2.0 is INHERITED (not new, not cured). Booked as
  inherited liability, not a fresh fail.

**O23. "η(R500)~2 means you still need dark matter in clusters — the theory fails clusters."**
- RESPONSE: True and disclosed — the kernel removes 74–89% of cluster DM, leaves 11–26%; the residual is the
  live a0-bump candidate front, not claimed solved. This is an INHERITED standard-MOND problem, orthogonal to
  the A-vs-B/C/D adjudication.
- RESIDUAL: **OPEN** (cluster residual), does not change the winner selection.

**O24. "Canonical a0 'fits better' — you cheated by freezing Υ."**
- RESPONSE: Explicitly NOT claimed. KiDS χ²/dof=0.640 at canonical a0 vs 0.24 at fitted a0=1.35e-10; anchoring
  is CHEAPER (fewer free params), NOT better (MEMORY rule). Disclosed in Gate 12.
- RESIDUAL: none — the honesty guard is applied.

---

### I. Cassini / solar system

**O25. "Cassini γ−1=(2.1±2.3)e-5 kills any MOND completion."**
- RESPONSE: For A, γ_PPN=1 is DERIVED kernel-independent (Gate 11), so Cassini is PASSED, not fought. The
  43,479σ Cassini violation is B/C's (γ_PPN=0, gate_lensing_weakfield_derivation.py this session), and is one
  of the three no-go kills — NOT A's.
- RESIDUAL: none for A on γ. (α_2 is A's live solar-system residue, O1.)

**O26. "The α=1 exact law forces a constant a0/2 sunward anomaly, 1278× over the Earth/Mars bound."**
- RESPONSE: This is the sharpest OPEN ephemeris liability of the exact-law READING (MEMORY:
  project_alpha1_ephemeris_liability), costed as "withdraw 'exact', keep phenomenology". In FC-FINAL the MOND
  sector uses the frozen μ_10 with μ_10→1−(1/10)(a0/g)^10 in the Newton regime — the sunward anomaly is
  suppressed by (a0/g)^10 at solar-system g, NOT the α=1 exact-law constant a0/2. The sharp kernel is what
  buys the ephemeris safety.
- RESIDUAL: quantitative solar-system ephemeris bound for μ_10 specifically not re-run this session; relies on
  the n=10 suppression. Booked benign-but-unverified-this-session.

**O27. "Even μ_10→1 has a residual fifth force through the aether at 1PN — that is α_1=−4K_B, already at the
LLR edge."**
- RESPONSE: Yes: α_1=−4K_B ⇒ K_B<2.5e-5 (LLR), a real bound (Gate 9), DERIVED. Not a fail, a constraint on
  K_B.
- RESIDUAL: tightens if α_2 (O1) is adverse. OPEN-adverse on α_2, bound on α_1.

---

### J. The no-go and the losing branch

**O28. "Your H_perp no-go is architecture-specific hand-waving; it does not really eliminate B and C."**
- EQ: source-free −k²q̂=0 ⇒ q̂(k≠0)=0 ⇒ Φ=0 ⇒ γ_PPN=0 (fc_no_go_Hperp_unsources_Phi.py, 12/12).
- RESPONSE: It is a THEOREM with four independent sympy legs (GR baseline, source-free replacement,
  kernel-blindness dS_2/dμ≡0, Laplacian-blindness λ~−S0/k²). B and C are explicit instances; both re-fail
  γ_PPN=0 ~20σ this session (gate_lensing_weakfield_derivation.py, exit 0).
- RESIDUAL: the no-go is a "sharp obstruction with a named escape" (ρ-sourced D²q≈4πGρ), but that escape IS
  H_perp reintroduced and demands a full uncertified Dirac re-count. No certified escape exists.

**O29. "C's named repair S_2′=D²(q+lnN) restores γ_PPN=1 — so C is not dead."**
- RESPONSE: The repair restores γ but does NOT fix α_3=−1 (sourced by the elliptic C_M lapse response;
  d(α_3)/d(Laplacian mult)=0, ppn certificate S5) and requires re-running Dirac Gates 3/6/7/8 for the new
  bracket {π_N,S_2′}=−D²(·/N)≠0. That is a NEW architecture (call it C′), not C.
- RESIDUAL: C′ is a future program, uncertified. C as defined stays STRUCTURALLY-DEAD.

**O30. "B/C matter non-conservation is an artifact of your gauge, not physical."**
- EQ: ∇_μT^{μi}=−ρD^iX at Newtonian order; a=−∇(Ψ+X); 1 AU anomaly 1.62e11× Sereno-Jetzer.
- RESPONSE: The anomaly is in a diffeomorphism-scalar residual (the deleted H_perp sources μ_1); it is
  gauge-invariant at Newtonian order and kernel-blind (μ(∞)=1). Re-derived this session.
- RESIDUAL: none — the FAIL stands for B.

---

### K. Kernel-specific attacks

**O31. "You could have engineered any verdict by choosing the kernel; μ_10 is cherry-picked."**
- RESPONSE: The decisive results are PROVEN kernel-blind: A's Gate 14 IR spectrum (δ²J_10=0, CERT2), A's
  c_T=1, A's γ_PPN=1; B/C's three kills (dS_2/dμ≡0, <1e-19 for μ_5,μ_10). No verdict was tuned by the kernel.
- RESIDUAL: μ_10's specific virtue is solar-system suppression (O26) and deep-MOND fit (O24); it neither
  causes nor cures any structural kill.

**O32. "tanh or μ=1−e^{−y} would change the answer."**
- RESPONSE: MEMORY record: exact-exponential μ=1−e^{−y} is KILLED by Cassini Q2 (3.76×) in the MMG/FC-AeST
  exponential family; tanh worse (3.76× vs). For A the quadratic-order results are kernel-INDEPENDENT so the
  IR verdict is identical; only the far-field/solar-system phenomenology differs, and there μ_10 (sharp) is
  the one that passes.
- RESIDUAL: none — kernel-blindness is proven where it matters.

---

### L. Architecture D

**O33. "You dismissed BIMOND too fast; its DOF might be healthy."**
- RESPONSE: Boulware-Deser BD ghost is UNCHECKED (booked OPEN, quote-neither-way). D is eliminated not on DOF
  but on the parameter-free cosmology sum-rule (route6_bimond_twin_2026.py, 30/30): F_b+F_TM=1≠2, twin sector
  cannot carry Ω_dm to the CMB.
- RESIDUAL: DOF/BD genuinely OPEN for D, but irrelevant — D already dead at cosmology.

**O34. "The sum-rule F_b+F_TM=1 is your convention; fix it and D lives."**
- EQ: F_TM=1−ν≤0 everywhere; sum rule kernel-independent, parameter-free.
- RESPONSE: The sum rule follows from the two-metric twin structure, not a convention — it is a theorem-grade
  identity (30/30). Fixing it would mean a different host, not BIMOND.
- RESIDUAL: none for D.

**O35. "D's ephemeris pass (1-AU anomaly 1e-3458.7) is spectacular — surely that counts."**
- RESPONSE: Flagged interpolation-dependent, structural robustness UNVERIFIED (STANDING owed #3). A
  construction-level R1/R3 pass plus an unverified ephemeris number does not survive a dead cosmology sector.
- RESIDUAL: D stays dead; ephemeris robustness OPEN.

**O36. "D's c_T might be fine on the BIMOND background even though the DW chassis gives +3.9e-2."**
- RESPONSE: Possible — that is exactly why the D c_T cell is booked OPEN-ADVERSE, not FAILED. But a possible
  c_T=1 does not revive a dead cosmology sector.
- RESIDUAL: c_T transfer to BIMOND host UNPROVEN; does not change D's death.

---

### M. Meta / verdict-level

**O37. "You are protecting AeST — 'find the smallest theory that survives', and you crowned the biggest (6 DOF)."**
- RESPONSE: The 2-DOF architectures (B, C) are eliminated by a THEOREM, not by preference: you cannot have
  {2 DOF via source-free q-constraint} AND {γ_PPN=1}. A is the smallest that survives the *filter*, which is
  not the same as smallest DOF. The optimizer is the mathematics: the no-go forces the extra DOF.
- RESIDUAL: whether a 2-DOF ρ-sourced escape (C′) exists is OPEN; if one certifies, it would outrank A. None
  exists in the record.

**O38. "CONDITIONALLY-VIABLE is just a euphemism for 'we could not close it' — call it BURNED."**
- RESPONSE: BURNED-NO-VIABLE-THEORY requires NO survivor of the filter. A survives Tier 1 (which kills all
  others), c_T=1, γ_PPN=1, Φ=Ψ, KiDS χ²/dof=0.64, FLRW background. A survivor exists ⇒ not BURNED.
- RESIDUAL: A is un-CLOSED (O15, O16, O1). Hence program verdict INCONCLUSIVE, not CLOSED and not BURNED.

**O39. "Then declare CONDITIONALLY-CLOSED — the only input left is the a0 numerology."**
- RESPONSE: NO. CONDITIONALLY-CLOSED is licensed only when the sole remaining input is genuinely
  phenomenological AND hides no unresolved consistency condition. Here THREE genuine consistency conditions
  remain: Gate 14 finite-k IR sign (could be a real Mpc-scale ghost), α_2 coefficient (could violate LLR),
  c_s² superluminality (could be acausal). These are consistency conditions, not inputs. Label disallowed.
- RESIDUAL: the a0 numerology IS a phenomenological input (O9), but it is not the SOLE remaining item.

**O40. "The whole program is a NO-GO — no relativistic MOND closes."**
- RESPONSE: The proven no-go eliminates only the constraint-first 2-DOF branch (B, C). A escapes it by
  retaining H_perp. The program does not terminate in a universal impossibility — one architecture is
  conditionally alive. Hence INCONCLUSIVE, not NO-GO-THEOREM.
- RESIDUAL: a whole-program NO-GO would require ALSO killing A at Gate 14 (finite-k FAIL) or α_2/c_s². If the
  finite-k FLRW computation returns branch (b), the verdict would move toward BURNED/NO-GO. Not yet computed.

**O41. "You never ran a full CLASS/Boltzmann or an N-body — this is all quadratic-action toy math."**
- RESPONSE: Correct scope statement. The claims are at the classical linear-perturbation / PPN / weak-field
  level (same level as 2109.13287 and the task brief). No CMB-fit, no N-body claim is made.
- RESIDUAL: full nonlinear/cosmological confrontation is downstream of closing Gate 14. OPEN.

**O42. "α_2 machine literally fails its own consistency check (D1/D2) — that is a red flag you are hiding."**
- RESPONSE: Disclosed openly (Gate 10, FINAL_PPN.md): fc_alpha2_preferred_frame_2026.py reproduces γ=1 and the
  static sector but D1 (α_1≠−4K_B under isotropic ansatz) and D2 (two g00 extractions of α_2 disagree) FAIL
  because the aether sources anisotropic O(w²) stress the isotropic ansatz cannot carry. The extracted α_2 is
  therefore WITHHELD, not reported as a pass. The FAIL is the honest signal that α_2 is OPEN, needing the
  generic-metric solve.
- RESIDUAL: α_2 coefficient OPEN. The certified α_1=−4K_B comes from the independent c-tensor map
  (fc_ctensor_map_2026.py, ALL PASS), not the failing machine.

**O43. "shift symmetry is broken by K(Q) (a potential), so the k→0 flat-direction rescue of O16 is invalid."**
- RESPONSE: K(Q) depends on Q=A^μ∂_μφ, still only through a DERIVATIVE of φ — φ→φ+const leaves Q invariant, so
  shift symmetry is INTACT and the conserved shift charge exists (P2 in fc_flrw_ir_sign_certificate.py). The
  k→0 mode is genuinely a flat direction.
- RESIDUAL: none for the symmetry claim; finite-k (O16) still open independently.

**O44. "Even at k→0, E~a⁻³→0 only asymptotically; during matter domination a³ is small and the negative energy
is large."**
- RESPONSE: The mode is on the dS ATTRACTOR; the claim is asymptotic stability (bounded excursion Π/(3HK0),
  E→0). During earlier epochs the analysis is exactly the finite-k / non-dS regime that is booked OPEN. So
  this objection correctly points at the open band, not at the k→0-on-dS result.
- RESIDUAL: **OPEN** — pre-dS / finite-k evolution is the decisive uncomputed piece (O16). Honestly the same
  gap.

---

## Net referee assessment

Of 44 hostile objections: the winner cleanly answers the covariance/DOF/ghost/c_T/γ_PPN/lensing/matter-coupling
attacks with re-run certificates; the numerology and cluster-residual attacks are conceded as
disclosed-inputs / inherited-open; and **three attacks land as genuine unresolved consistency conditions** —
**O15/O16/O44 (finite-k FLRW IR sign, DECISIVE), O1/O42 (α_2 coefficient), O3/O15 (superluminal c_s²).**
Because these are consistency conditions rather than phenomenological inputs, the verdict is held at
**INCONCLUSIVE** (winner A conditionally-viable), not CONDITIONALLY-CLOSED, not CLOSED, not BURNED, not a
whole-program NO-GO. The one number that moves it: the finite-k sign of the low-k scalar Hamiltonian on the
FLRW background.
