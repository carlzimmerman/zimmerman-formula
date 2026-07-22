# Submission Package — Physical Review D

**Working title:** *A covariant, ghost-free modified-inertia completion of the horizon-tied acceleration scale $a_0 = cH_\Lambda/Z$, and a passivity obstruction to single-metric MOND lensing*

**Author:** Carl P. Zimmerman (independent; Briar Creek Tech) · carl@briarcreektech.com · ORCID 0009-0008-3508-7982

**Target section:** PRD — Gravitation and Cosmology (secondary: Particles, Fields, Gravitation, and Cosmology overlap for the field-theory content).

**Manuscript class:** REVTeX 4.2, `\documentclass[aps,prd,twocolumn,superscriptaddress,nofootinbib]{revtex4-2}`.

**Consolidates:** Zenodo `10.5281/zenodo.21403470` (MI Field Theory Results), concept `10.5281/zenodo.21253644` (covariant MI completion), `10.5281/zenodo.21418816` (passivity/lensing no-go), and `10.5281/zenodo.20973740` (the honest no-go paper that already passed an adversarial review).

---

## PART 1 — COVER LETTER TO THE EDITOR

Dear Editors,

Please consider the enclosed manuscript, *A covariant, ghost-free modified-inertia completion of the horizon-tied acceleration scale $a_0 = cH_\Lambda/Z$, and a passivity obstruction to single-metric MOND lensing*, for publication in Physical Review D.

**The single result.** The paper writes down a covariant, ghost-free field theory in which the MOND acceleration scale $a_0$ appears *only* as the horizon-floored argument of a passive vacuum-response kernel — a *modified-inertia* realization, with a passive unit-timelike frame carrying zero propagating degrees of freedom and the phenomenology living in the matter sector rather than in the gravitational field equations. Within that construction we prove an exact obstruction theorem: **conditional on kernel passivity, $\{a_0\text{ tied to the passive kernel}\}$ and $\{$single-metric, $c_\gamma = c_{\rm GW}\}$ together forbid single-metric MOND weak lensing** ($D \wedge S \Rightarrow \lnot L$; $\{D,S,L\}$ is the unique minimal unsatisfiable subset of $\{D,S,G,L\}$, with ghost-freedom $G$ entering no step). The mechanism is a passivity/amplification dichotomy: the property that ties $a_0$'s scale to the de Sitter horizon ($\sup K = 1$) is the same property that caps the kernel's dressing at suppression $\rho/\nu$, whereas MOND lensing requires enhancement to $\nu\rho$.

**Why PRD.** This is a gravitational field-theory result: a covariant action, its Hamiltonian degree-of-freedom count, a ghost/Ostrogradsky analysis, and an obstruction theorem relating the theory's stress tensor to a weak-lensing observable. It sits squarely in PRD's modified-gravity/modified-inertia field-theory literature — AeST (Skordis & Zlosnik, *PRL* 2021), the Deffayet–Esposito-Farèse–Woodard nonlocal-metric MOND completions (*PRD* 2011), and Bekenstein's TeVeS (*PRD* 2004) — to all of which the paper is explicitly positioned. The result is technical, reproducible, and falsifiable, not a phenomenological fit.

**Honest scope, stated up front.** I want to be transparent with the editors about what is and is not claimed, because the framework has a history I have publicly corrected. The value of $a_0$, the constant $Z = \sqrt{32\pi/3}$, and the coupling sign $s=-1$ are **postulated, not derived** — the theory is a *one-parameter effective field theory*, not a first-principles computation of $a_0$. The interpolating kernel $\nu(y)=\sqrt{1+1/y}$ is **Milgrom's** (1999); the framework's distinctive content is the $cH_\Lambda/Z$ coefficient (Milgrom's was $2cH_\Lambda$) and the covariant passive-frame completion. I explicitly retract, and do not re-assert, any earlier claims of a derived $a_0$, a Standard-Model bridge, or a "theory of everything." The paper's positive claims are confined to the construction and the obstruction theorem; every derived-versus-postulated element is flagged in a ledger.

**The obstruction cuts against the program's own most distinctive claim,** and I present it that way rather than as a victory: the completion of the lensing sector exists only by crossing into modified *gravity* with $a_0$ demoted to a free coupling. I believe a clean negative structural result of this kind — that a passive-kernel-derived $a_0$ and single-metric MOND lensing cannot coexist — is exactly the sort of load-bearing, falsifiable statement PRD readers in this area will want on the record, whichever way the underlying program ultimately goes.

**Reproducibility.** All symbolic and numerical checks (degree-of-freedom count, kernel positivity/measure, the stress tensor, the truth table underlying the theorem, and an independent adversarial re-derivation) are committed as runnable Python scripts (sympy/numpy, all exit 0) in the self-verifying public repository `github.com/carlzimmerman/zimmerman-formula`; the companion tool `a0kit` reproduces the phenomenology (Zenodo software DOI 10.5281/zenodo.21478981; ASCL submission pending editor review). Every $a_0$-valued number is reported on both cosmological footings ($9.36\times10^{-11}$ and $1.13\times10^{-10}\,\mathrm{m\,s^{-2}}$); the obstruction is footing-independent.

I am an independent researcher with no academic affiliation and no competing interests. This manuscript is not under consideration elsewhere. I have suggested potential referees below and would be glad to provide the verification scripts to the referees directly.

Thank you for your consideration.

Sincerely,
Carl P. Zimmerman
Briar Creek Tech · carl@briarcreektech.com · ORCID 0009-0008-3508-7982

*Suggested referees (modified-gravity/inertia field theory):* Constantinos Skordis; Richard Woodard; Luc Blanchet; Benoit Famaey; Tom Zlosnik. *(Editors to select independently; suggested for topical expertise only.)*

---

## PART 2 — REFEREE-ANTICIPATION MEMO

The hardest attacks a competent PRD referee will make, with the honest answer to each. Where the honest answer is "yes, that is a real limitation," it says so.

### A1. "This is just AeST / a MOND field theory relabeled. What is actually new?"
**Honest answer — substantive, and the paper's central positioning.** AeST (Skordis–Zlosnik) and the Deffayet–Esposito-Farèse–Woodard nonlocal completions are modified-*gravity*: the MOND phantom is real gravitating stress-energy sourced by new *propagating* gravitational structure, and $a_0$ enters as an independent Lagrangian coupling. The present theory is modified-*inertia*: a *passive* frame (zero propagating dof, machine-verified 2nd-class Dirac closure), the modification carried in the matter kinetic sector, and $a_0$ appearing *only* as the horizon-floored kernel argument $K(\Box_u/a_0^2)$ — not as a free coupling. That structural difference is not cosmetic: it is precisely what the obstruction theorem shows is *incompatible* with single-metric MOND lensing, whereas AeST reproduces lensing comfortably. So the novelty is (i) the passive-frame covariant construction and (ii) a theorem distinguishing the MI and MG classes on a physical observable.

### A2. "Is the completion genuinely ghost-free, or is the passive frame hiding an Ostrogradsky mode?"
**Honest answer — ghost-free for the local first-moment action, conditional on the passive-frame premise, with two named residuals.** The local action is first-order in every dynamical field; the classic modified-inertia Ostrogradsky trap (Lagrangians in $\ddot x$) is evaded because the acceleration enters as a *field gradient* $a^\mu = u^b\nabla_b u^\mu$, not a worldline $\ddot x$. The frame is 0-dof by a machine-verified Dirac constraint analysis (second-class pair, block determinant $\to 4$, no tertiary tower), and the nonlocal kernel is ghost-free by a Herglotz–Nevanlinna single-healthy-pole argument (positive measure, residue $+1$, $0 < K \le 1$). **The two honest limitations we flag ourselves:** (i) the whole 0-dof/no-ghost verdict *rests on* the passive/hypersurface-orthogonal frame premise — a dynamical khronon would reintroduce an Ostrogradsky concern, and we state this as the load-bearing hinge, not a proven theorem; (ii) the precise open lane in the nonlocal sector, precisely scoped: the auxiliary-tower Herglotz ghost check of $B[K(\Box_u)]$ **is** machine-verified (`mi_closure_pin/ostro_nonlocal_verify.py`, 13/13, with live negative controls that correctly flag a textbook $\ddot q^2$ ghost and a negative-measure kernel); what remains *asserted, not verified*, is the fully-coupled all-orders nonlocal Hamiltonian (and global $B<1$ off spherical symmetry). Both are stated as such in the manuscript's ledger — the disclosure is kept, neither buried nor overstated. Crucially, **the obstruction theorem does not depend on ghost-freedom** ($G$ enters no step), so these residuals do not affect the paper's central result.

### A3. "The no-go premises are too narrow. You have not exhausted all Lagrangians — you checked three term classes."
**Honest answer — correct, and stated explicitly in the paper.** The theorem's *rigor* lives in two universal lemmas (a nonlocality lemma using $S$; a boundedness lemma using passivity), not in the finite truth table, which is bookkeeping — modus ponens over the two lemmas across the examined term classes (frame–curvature, nonlocal-in-matter, frame/scalar carrier). It is **not** an exhaustion over all possible Lagrangians, and we say so. The result's strength is exactly the strength of the two lemmas as physics statements over those classes. A referee who exhibits a term class outside our lemmas' reach would genuinely extend the boundary — and we would welcome that, because the paper frames the theorem as a *conditional* obstruction, not a closure.

### A4. "$a_0 = cH_\Lambda/Z$ is not derived — you posit $Z$. So the whole 'derived scale' framing is empty."
**Honest answer — the value is not derived, and we never claim it is; but the *scale-tie* is a genuine structural constraint.** $Z=\sqrt{32\pi/3}$ and the sign $s=-1$ are postulates; $\kappa=1/2$ is provably unforceable from ghost-freedom + unitarity + holography. The theory is a one-parameter EFT. What "derived" means in this paper — and we define it narrowly ($D$: $a_0$ enters *solely* as the horizon-floored kernel argument, not as an independent coupling) — is the *scale-tie*, i.e. that passivity floors the response amplitude at $cH_\Lambda$. The obstruction theorem's whole point is that even this weaker, honest sense of "derived" is load-bearing: it is what is incompatible with single-metric lensing. If $a_0$ were a cosmetic relabeling one could keep it and add any lensing structure; the theorem shows one cannot.

### A5. "The $\nu(y)=\sqrt{1+1/y}$ kernel is Milgrom 1999. You are claiming his result."
**Honest answer — the kernel is Milgrom's, credited prominently, and the paper's claim is elsewhere.** Milgrom (1999, *Phys. Lett. A* **253**, 273, Eq. 9) wrote this exact interpolating modified-inertia kernel with coefficient $2cH_\Lambda$. We credit this in the abstract, introduction, and references, and state plainly that the kernel functional form is not original. The distinctive content is (i) the $cH_\Lambda/Z$ coefficient, (ii) the *covariant passive-frame field theory* realizing it (Milgrom's 1999 formulation was non-covariant/heuristic), and (iii) the obstruction theorem. We do not claim the shape.

### A6. "The stress tensor and the '$\rho/\nu$ suppression' are the crux. Is the bookkeeping right — could a frame-constraint leg secretly supply the enhancement?"
**Honest answer — checked, and the answer is no, for a stated reason.** In the composite-frame bookkeeping ($u = J^\mu/|J|$, $u\cdot u=-1$ identically), the frame-constraint leg $S_u$ vanishes and contributes zero stress, so the $1/\nu$ dressing comes entirely from the matter leg $\rho K$. The assembled tensor has a $uu$-coefficient $K=1/\nu \le 1$ (suppression) and an anisotropic slip term $2K'X/K = 1/(2y+1)$ that is bounded and tension-signed — it *reduces* lensing. There is no $O(\nu)$ structure anywhere in the passive tensor; that is Lemma 2 ($\sup K = 1$). This is verified symbolically (`nogo.py`, `verify_adversarial.py`) and re-derived independently.

### A7. "The disformal $\{D,L\}$ escape — why is GW170817 fatal rather than a constraint to be evaded?"
**Honest answer — it is an observational kill, and we present it as the reason $S$ is a non-redundant hypothesis.** A disformal second cone $\tilde g = g + B(\Box_u)\,u_\mu u_\nu$ keeps $a_0$ derived and evades the nonlocality lemma (the phantom becomes pure geometry, not stress-energy). But a $B$ large enough to carry the $O(\nu)$ lensing deflection splits the photon and graviton cones far above $|c_\gamma/c_{\rm GW}-1|\lesssim 10^{-15}$ (Abbott et al. 2017), while the GW-safe small-$B$ regime cannot source the deflection — the same passivity/amplification wedge on the disformal axis. So $\{D,L,\lnot S\}$ is a logically satisfiable field theory killed *observationally*. This is exactly why $S$ belongs in the minimal unsatisfiable subset and is not redundant.

### A8. "Weak lensing already excludes single-metric pure MI at high significance. What is left to prove?"
**Honest answer — the exclusion is the *motivation*; the theorem is the *completion* question.** That single-metric pure MI under-lenses (Brouwer et al. 2021, KiDS-1000; $\sim 27\sigma$ against the lensing-RAR $=$ dynamical-RAR equality, conservative rail, footing-independent) is the starting point, not the result. The paper's content is whether the $\nu^2$ wedge can be closed by *adding structure* while keeping the program distinctive — and the theorem says: not without crossing into MG and freeing $a_0$. That is a statement about the theory space, not a re-derivation of the data tension.

### A9. "You keep two values of $a_0$. Is the theory even predictive?"
**Honest answer — the footing fork is a genuine open choice, but the obstruction is footing-independent.** The two footings ($\rho_{\rm DE}/cH_\Lambda \Rightarrow 9.36\times10^{-11}$; $\rho_{\rm total}/cH_0 \Rightarrow 1.13\times10^{-10}$) reflect a real ambiguity in which cosmological input feeds the scale-tie, and we carry both. The theorem's dimensionless content (the shortfall $\nu^2-1 = 1/y$, mass-blindness $\sqrt{M_2/M_1}$) is invariant under $(a_0, g_{\rm bar}) \to \lambda(a_0, g_{\rm bar})$, so the verdict does not depend on resolving the fork. For phenomenology the SPARC RAR is convention-compatible and non-diagnostic between the two — which we state rather than hide.

### A10. "Where can MI still be distinguished from MG observationally, if lensing is now shared?"
**Honest answer — one underpowered channel, honestly labeled as such.** Once the only lensing-reproducing completions are MG, weak lensing can no longer discriminate MI from MG. The clean modified-gravity-*impossible* discriminant that remains is the non-adiabatic **relational velocity-dispersion spread** ($\sim 6$–$13\%$ in MI from frame-history-dependent inertia; *exactly zero* in MG) — a one-line pointer in this paper, cited to Zenodo 10.5281/zenodo.21421896 (the held-back companion that develops it; strategy §1.4 firewall). It is currently underpowered, and any MG completion also inherits the AeST Solar-System $Q_2$-quadrupole caveat (Desmond–Hees–Famaey 2024; Park et al. 2026). We do not oversell this channel; we flag it as where discrimination effort should go.

---

## PART 3 — SHARPENED NOVELTY STATEMENT (2–3 sentences)

> The interpolating law $\nu(y)=\sqrt{1+1/y}$ is Milgrom's modified-inertia kernel (1999), and the $a_0 \propto \sqrt{\rho_{\rm DE}}$ scale-tie is the Limbach–Psaltis–Özel (2008) horizon-scaling idea — neither is claimed here. What is new is (i) a **covariant, ghost-free field-theory realization** of that kernel built on a *passive* unit-timelike frame with **zero propagating degrees of freedom**, in which $a_0=cH_\Lambda/Z$ enters solely as the horizon-floored kernel argument rather than (as in AeST/Skordis–Zlosnik and the Deffayet–Esposito-Farèse–Woodard nonlocal completions) a free gravitational coupling; and (ii) an **exact obstruction theorem** — conditional on kernel passivity — that this modified-*inertia* construction and single-metric MOND weak lensing cannot coexist, via a passivity/amplification dichotomy in which the property that ties $a_0$ to the de Sitter horizon is the property that forbids the lensing phantom.

---

## PART 4 — CALIBRATED ABSTRACT (PRD-appropriate)

> The de Sitter–Unruh modified-inertia (MI) program reproduces galaxy dynamics through a passive vacuum-response kernel $K(\Box_u/a_0^2)$ that ties the MOND acceleration scale to the cosmological horizon, $a_0=cH_\Lambda/Z$ with $Z=\sqrt{32\pi/3}$. We present a single covariant action realizing this program — Einstein–Hilbert gravity, a passive unit-timelike frame $u^\mu$ fixed by a Lagrange constraint (zero propagating degrees of freedom), and a matter sector dressed by a bounded, causal, positive-measure (Herglotz–Nevanlinna) kernel — and show that the coupled system is ghost-free and well-posed (2 graviton + matter degrees of freedom; a machine-verified second-class Dirac closure keeping the frame non-propagating even after the matter coupling), conditional on the passive-frame premise. The construction is *modified inertia*: unlike AeST (Skordis & Zlosnik 2021) and the Deffayet–Esposito-Farèse–Woodard nonlocal-metric completions, the modification lives in the matter sector and $a_0$ enters only as the horizon-floored kernel argument, not as a free coupling. The interpolating kernel $\nu=\sqrt{1+1/y}$ is Milgrom's (1999) and the $a_0\propto\sqrt{\rho_{\rm DE}}$ scaling is Limbach–Psaltis–Özel's (2008); the distinctive content is the $cH_\Lambda/Z$ coefficient and the covariant passive-frame completion. Within this theory we prove an obstruction: conditional on kernel passivity, a horizon-tied $a_0$ ($D$) and single-metric propagation with $c_\gamma=c_{\rm GW}$ ($S$) forbid single-metric MOND weak lensing ($L$); i.e. $D\wedge S\Rightarrow\lnot L$, with $\{D,S,L\}$ the unique minimal unsatisfiable subset of $\{D,S,G,L\}$ and ghost-freedom $G$ entering no step. The mechanism is a passivity/amplification dichotomy — a passive kernel ($\sup K=1$) can only suppress a source to $\rho/\nu$, whereas the MOND-lensing phantom demands enhancement to $\nu\rho$ — reinforced by a nonlocality lemma turning any mass-correct lensing carrier into a propagating degree of freedom whose acceleration scale is a free coupling. Completions that do reproduce lensing exist, but only as modified gravity with $a_0$ demoted to a free coupling. We are explicit that the value of $a_0$, the constant $Z$, and the sign $s=-1$ are postulated, not derived; that the theorem is conditional on the passivity premise; and that all $a_0$-valued quantities are reported on both cosmological footings ($9.36\times10^{-11}$ and $1.13\times10^{-10}\,\mathrm{m\,s^{-2}}$), the obstruction being footing-independent. All symbolic and numerical checks are provided as runnable scripts.

*(PhySH — APS retired PACS in 2016: modified gravity; dark matter; alternatives to general relativity; gravitational lensing. As drafted above this runs ~340 words; the submission kit's `kit_prd/manuscript.tex` carries the trimmed ~230-word version — use that one.)*

---

## PART 5 — REFORMATTING / CONSOLIDATION PLAN

### 5.1 Which Zenodo sources map to which manuscript sections

| Zenodo source | Role in the PRD manuscript |
|---|---|
| **21403470** — MI Field Theory Results (+ erratum 21415677) | Sections II–IV: the single action, the passive-frame Dirac/dof analysis, the Herglotz kernel, the stress tensor, ghost-freedom & well-posedness. The consolidated `MI_FIELD_THEORY.md` is the backbone. |
| **21253644** (concept) — covariant MI completion | Feeds Section II (derivation of the worldline law via the first-moment identity $u\cdot\Box_u u=-|a|^2$) and the DERIVED/POSTULATED ledger. |
| **21418816** — passivity/lensing no-go | Sections V–VII: the completion problem, the two lemmas, the obstruction theorem, the candidate scorecard (C1/C2/C3), footing independence. This is the paper's climax. |
| **20973740** — honest no-go paper (adversarially reviewed) | Section I framing (what is forced vs postulated), the a₀ reframing algebra, and the honest-scope discipline throughout; source of the "less claimed" calibration. ⚠️ **Supersession flag (must appear in the manuscript's related-work note):** 20973740's abstract asserts "no covariant modified-inertia completion exists in three exhaustive cases" (its item iii) — that no-go is **superseded by the present construction**: the strong-coupling obstruction assumed a *propagating* aether and does not apply to the passive frame (zero propagating modes; correction recorded in DOI 10.5281/zenodo.21263846). Only its honest-scope ledger and reframing algebra are consolidated. |

### 5.2 Consolidation strategy
Fold all four into **one** manuscript with the field-theory construction first (the positive result) and the obstruction second (the sharp negative result) — the two halves are one story: *here is the covariant MI theory; here is exactly the observable it cannot reach single-metric.* Do **not** submit the four separately; PRD will (rightly) see overlap. The adversarially-reviewed no-go (20973740) is not a separate paper here — its role is to supply the honest-scope scaffolding and the reframing algebra, cited to the Zenodo record.

### 5.3 Proposed section skeleton
1. **Introduction** — the coincidence, the MI-vs-MG distinction, honest scope ledger, statement of both results. Includes the mandatory **"Related work by the author"** note (strategy §1.4): names the JCAP companion (the $a_0(z)$ pre-registered test; deposits 20737162 / 21440407 / 21478568) and the MNRAS companion (the SPARC $a_0$-line measurement; deposit 21419735) with their distinct results — *"the companions treat the phenomenology; the present paper is confined to the field-theory construction and the obstruction theorem"* — cites the four consolidated deposits as the author's own timestamped preprint record, and carries the 20973740 supersession sentence (see §5.1).
2. **The covariant action** — $S_{\rm EH}+S_u+S_{\rm matter}$; passive frame; kernel; first-moment reduction to $\nu(y)=\sqrt{1+1/y}$.
3. **Degrees of freedom and ghost-freedom** — Dirac constraint analysis; Herglotz single-pole; well-posedness; the passive-frame premise stated as the hinge.
4. **The stress tensor** — assembly, conservation ($\nabla_\mu T^{\mu\nu}=0$), the $\rho/\nu$ suppression, no-slip in the UV limit.
5. **The completion problem** — desiderata $D,S,G,L$; the $\nu^2$ wedge.
6. **The obstruction theorem** — Lemmas 1–2; $D\wedge S\Rightarrow\lnot L$; minimal unsatisfiable subset; candidate witnesses C1/C2/C3 (condense the scorecard to one table).
7. **The passivity/amplification dichotomy** — the physical crux.
8. **Scope, conditionality, and the open pump door** — both-ways honesty; footing independence; the relational $\sigma$-spread as the surviving MI≠MG discriminant — **one-line pointer only, cited to Zenodo 10.5281/zenodo.21421896** (strategy §1.4 firewall: never develop its phenomenology here).
9. **Conclusion.**
- **Data & Code Availability** — the repository `github.com/carlzimmerman/zimmerman-formula` is self-verifying (every load-bearing number traces to a committed exit-0 script), citing `a0kit` at Zenodo DOI 10.5281/zenodo.21478981 (ASCL submission pending editor review); one-line echo in the cover letter.
- **Appendix A** — verification scripts (list + one-line description each; repository link).
- **Appendix B** — the DERIVED/POSTULATED ledger (D1–D15, P1–P9), lightly condensed.

### 5.4 Length, class, figures
- **Length target:** 16–20 PRD two-column pages (within the requested 15–25). The field-theory half is equation-dense; the no-go half is compact once the lemmas carry it.
- **REVTeX class:** `revtex4-2`, options `[aps,prd,twocolumn,superscriptaddress,nofootinbib,longbibliography]`. Single author, single affiliation.
- **Figures (3, all reproducible from committed scripts):**
  1. The $\nu^2$ wedge: needed $\nu\rho$ vs sourced $\rho/\nu$ as a function of $y=g_{\rm bar}/a_0$, both footings overlaid (shows footing-independence of the dimensionless gap).
  2. The candidate-mechanism map: a $\{D,S,G,L\}$ corner diagram locating pure MI, C1, C2/C3b (AeST/DEW class), and the GW-dead disformal $\{D,L\}$ witness.
  3. SPARC RAR fit at $\Upsilon=0.70$ (0.108 dex) with the MI kernel, for phenomenological grounding — cite `a0kit`.
- **Tables (2):** the DERIVED/POSTULATED ledger (condensed); the candidate scorecard (C1–C3b).
- **Supplemental Material:** the runnable verification scripts (`rederive_identity.py`, `closure_map.py`, `matter_coupling_Tmunu.py`, `wellposed.py`, `c1_frame_curvature.py`, `c2_nonlocal.py`, `c3_carrier.py`, `nogo.py`, `verify_adversarial.py`), each exit-0 on both footings, with a README pinning file:line provenance to the frozen repository.

### 5.5 Pre-submission checklist (banned-word / calibration sweep)
- [ ] No "proves/solved/confirms/definitive/theory of everything" anywhere. ("Theorem" and "obstruction theorem" are fine as mathematical objects; "no-go" is standard field-theory usage.)
- [ ] Milgrom 1983 **and** 1999, AeST/Skordis–Zlosnik 2021, DEW 2011, Bekenstein 2004, and Limbach–Psaltis–Özel 2008 all cited in the first two pages.
- [ ] $a_0$ value, $Z$, and $s=-1$ flagged POSTULATED at first mention and in the ledger.
- [ ] Both footings on every $a_0$-valued number; obstruction stated footing-independent.
- [ ] Passivity premise stated as a *premise* (theorem conditional), not a metatheorem; the open "forced-pump" door named.
- [ ] Ghost-freedom residuals (dynamical-khronon hinge; nonlocal-B assertion) disclosed, and noted not to affect the theorem ($G$ enters no step).
- [ ] No personal information beyond the byline and institutional email.
- [ ] Retraction of prior overclaims implicit in the scope ledger; do not re-assert derived-$a_0$/SM/TOE.
- [ ] ORCID 0009-0008-3508-7982 on the byline, in the cover-letter signature, and linked in the APS profile; Zenodo DOIs attached to the ORCID record before submitting (strategy §3.1).
- [ ] Data & Code Availability section present: repository named as self-verifying (every load-bearing number → committed exit-0 script); `a0kit` cited at Zenodo DOI 10.5281/zenodo.21478981 (ASCL submission pending editor review); one-line echo in the cover letter.
- [ ] "Related work by the author" note present (strategy §1.4): JCAP + MNRAS companions named with distinct results and Zenodo DOIs; the four consolidated deposits disclosed as the author's own preprint record.
- [ ] The 20973740 supersession sentence present (its item-iii covariant-completion no-go superseded by the present construction; strong-coupling wall assumed a propagating aether, does not apply to the passive 0-dof frame; correction DOI 21263846).
- [ ] $\sigma$-spread appears only as a one-line pointer cited to Zenodo 10.5281/zenodo.21421896 (never developed here).
- [ ] Nonlocal-ghost disclosure precisely scoped (A2(ii)): auxiliary-tower Herglotz check machine-verified (`ostro_nonlocal_verify.py` 13/13 + live negative controls); open lane = fully-coupled all-orders nonlocal Hamiltonian + global $B<1$ off sphericity.
- [ ] Supplemental scripts frozen only after `verify_adversarial.py` carries the corrected connective (not(D∧L) under S — fixed 2026-07-22, exit 0 re-verified); PhySH terms only (no PACS).
