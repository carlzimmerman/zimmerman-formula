# YM REFEREE — the adversarial survivability matrix for the yang_mills_gap door

**Audited door:** the mass gap = the eaten Goldstone of the a0-sector — L5's
shift-symmetric L = Λ⁴f(K), K = −(1/2)(Dφ)²/Λ⁴ with the minimal Stueckelberg
gauging Dφ = ∂φ − mA, mass faces m_A² = μ₂(u)m² (clean) and
m_A² = m²u(u²+3u+4)/(1+u)³ (exact), pinned by m = m_dust =
k_B T_0(1+z\*)/σ² = 5.09 keV (the committed ladder-mass inversion).

**Record audited (read in full before this ruling):** YM00_CAMPAIGN.md (K1–K5,
falsifier), YM01_gap_derivation.out (20/20), YM01_results.json,
YM_GAP_STATEMENT.md, lean/YM01_gap.lean (header + spine), THE_THEORY.md (L1–L16),
WAVEBOARD.md (B4, B8, C02, G081, G089, G152, G168, G212), TOE_STATUS.md,
glm53_push/G054_frozen_scalar_cosmology.py, deepseek_push/G155_sourced_eq.py,
F03_phantom_correlator.py, STATE.md, LAW_VERIFIED.md.

**Adversarial premise:** every registered statement that could kill or
circumscribe the door is ruled ALIVE (the statement survives exactly as
committed) / KILLED (the door contradicts it and dies) / BOUNDARY-REGISTERED
(the statement circumscribes the door; the boundary is either pre-registered
on the record or must be registered here). No ruling is made on the door's
behalf that the door itself did not print.

---

## THE MATRIX

### (a) L5 — "no vector sector (α₁ = α₂ = 0 by structure), no aether" — **BOUNDARY-REGISTERED**

L5 (THE_THEORY.md:56-59): "L = Λ⁴ f(K) … Lorentz invariant, no aether, no
vector sector (alpha1 = alpha2 = 0 by structure), zero free parameters beyond
a0." The minimal gauging adds a DYNAMICAL U(1) vector (2 Proca polarizations)
to L5's field content. In LETTER the assertion "no vector sector" is amended —
this is a structural change to a certified lemma, not a consequence of it.
In CLASS it is preserved: the killed object is the EXPLICIT BACKGROUND /
preferred-frame vector. The mass term (Dφ)² is Lorentz-invariant at the action
level (YM01 C1: D(φ + mχ) − m(A + dχ) = Dφ − mA IDENTICALLY, residual 0,
YM01_gap_derivation.out:26-28; Lean `stueckelberg`), and α₁ = α₂ = 0 survives
by structure (no c₁₄, no K_B, no congruence — G054 C1, G054:261-277). The
boundary was PRE-REGISTERED as K3: "the gauged shift has NO explicit background
(the gradient v is a solution of the sourceless equation, not a term of the
action) — registered as the boundary; the referee's override kills the door"
(YM00:62-67). A referee reading L5's letter strictly fires the override and
the door dies by its own pre-registration — that is the honest state. Adversarial
catch, resolved: B1's measured "mass^2 coefficient f'(K0) m²/2" (YM01.out:17)
vs the declared m_A² = μ₂m² is the canonical (1/2)A² Lagrangian convention —
the physical face is fixed at the Lean level (gap_clean := m·√μ₂,
YM01_gap.lean:36) and numerically (D5: √μ₂(0.2276) = 0.58002 vs m_A/m =
0.5800, YM01.out:69). Phrasing vulnerability, not an error.

### (b) G054 — "No background vector, no Stueckelberg, no khronon, no Einstein-aether" — **BOUNDARY-REGISTERED (the kill does not fire on its own scope)**

G054 C2 (glm53_push/G054_frozen_scalar_cosmology.py:285) states a property of
the FROZEN COSMOLOGICAL completion: the action as deployed on FRW has zero
vector DOF ("vector DOF count = 0", G054:261-277; V3 "α₁ = α₂ = 0 by
structure", G054:20). The kill's scope is an action-level EXPLICIT background
vector. The door's v is a SOLUTION of the sourceless equation — φ = C ln r,
∂φ = C/r, "the phantom solves div[μ₂ grad φ] = 0 EXACTLY"
(G155_sourced_eq.py:308-314) — not an action term. YM01 K3: "G054's kill
(explicit background vector in the frozen completion) does not fire on a
solution-generated gradient" (YM01.out:92-94). What WOULD fire G054: an
observed preferred-frame parameter α₁ or α₂ ≠ 0 — which the door already
registers as its own falsifier class (c) (YM00:87-89; YM_GAP_STATEMENT:67-69).
RULE: the kill is scoped to the frozen-completion action; the door's vector is
dynamical and frame-free; both the boundary and the firing condition are on
the pre-registered record (YM00:62-67, YM01.out:92-94).

### (c) B8 / E02 / F03 / G081 — "gaugeless Goldstone branch, gap EXACTLY ZERO" — **ALIVE (the zero-gap claim is preserved as the m → 0 face)**

B8 (WAVEBOARD.md:1609-1622, 15/15): the EOS carries c_s² = σ² → the GAUGELESS
Goldstone acoustic branch ω(k) = c_s k, "gap EXACTLY ZERO (G081's ω² = 0
EXACT = the k→0 face: no growing mode, no decay channel)". G081
(WAVEBOARD.md:19-22): ω² = 0.000, cap-invariant, homology zero-mode
(THE_THEORY.md:150-153: marginal mode; an entropy extremum, not a dynamical
attractor). F03 (F03_phantom_correlator.py:40-42): the phantom's committed
linear response is carried by the gapless branch — "no gap at k → 0, no
gapped/massive counterpart on the record (G081: 'no such mode')" — and F03's
V3 kill conditions stay ARMED against the UNGAUGED equilibrium's density
response: "a GAP at k → 0: ω(0) > 0 … kills the Goldstone face of the
committed equilibrium" (F03:826-834). The door preserves every one of these
as the m → 0 face: D5 measures the gauged branch ω(k)² = k² + m_A² with the
SAME m_A on every momentum (max residual 5.33e-15) and registers "B8's
gaugeless branch ω = c_s k … is the m → 0 face: the pole LIFTS to
min_k ω(k) = m_A > 0"; at m = 0, min_k ω = 0 (YM01.out:68-70). G081's
marginal mode IS the gaugeless signature; gauging lifts ω(0)² = 0 → m_A² > 0
while "no growing mode, no decay channel" rigidity is preserved (a massive
vector decays only above 2m_A — YM01.out:70). E02's quantum face is a
circumscription, not a kill: "no graviton — no radiation sector, no
propagating DOF, no quantized metric" (TOE_STATUS.md:58-64, E2 15/15) — the
vector adds a propagating DOF (the door's price: classical, no quantization
claimed anywhere in the lane, no UV completion — YM_GAP_STATEMENT:42-48), and
it is observationally inert by D6 ((m/M_pl)² = 4.37e-48 at 5.09 keV,
YM01.out:79-81). REGISTERED SURFACE INCONSISTENCY (adversarial catch, must be
reconciled before a reader runs the numbers): E02's nλ_dB³ = 8.6e-9
(TOE_STATUS.md:64) vs B8's 3.4e-11 (WAVEBOARD.md:1619-1620) differ ~250×;
both sit ≥ 8 orders below 2.612, so "NOT a condensate" survives either way,
but the two registers disagree.

### (d) G155 — "the sourced equation door is CLOSED" — **ALIVE (the gauged mass term reopens nothing)**

G155's verdict (G155_sourced_eq.py:54-60, :356-367): no shift-symmetric
completion sources div[μ₂ grad φ] = 4πGρ without (i) an unscreened O(1) fifth
force (F_5/F_N = 2(M_pl/M)²/μ₂ = 1/μ₂ at the MOND-required M = √2 M_pl,
G155:21-24, :163-172), (ii) γ = 1/2 — Cassini fails 2.2e4× (G155:195-204),
and (iii) MICROSCOPE forces M_WEP ∈ [3.8e4, 3.8e5] M_pl, suppressing the
source by 7.1e8–7.1e10 (G155:214-239). THE FORCE-LAW READING IS CLOSED as a
fundamental sourced field equation; the AVAILABLE reading is G031's
equilibrium/EOS reading of the SOURCELESS equation (G155:364-367). The
Stueckelberg mass term changes the scalar's KINETIC sector (K →
−(1/2)(Dφ)²/Λ⁴); it adds NO matter coupling — baryons carry no shift charge
(tree-level decoupling, YM_GAP_STATEMENT:45-48), the vector's only force is a
(m/M_pl)²-suppressed dust-dust Yukawa (YM01.out:79-81). None of G155's three
candidates (trace/conformal, variable-mass, self-source) is re-opened, and
the door's gap profile rides the gradient of the SOURCELESS solution —
exactly G155's surviving reading (G155:364-367). SUB-BOUND (registered in the
lane, must stay registered): the U-MAP finding D1/G1b — the committed
constants give C_f = 0.0997356 ≈ 1/(2√(8π)) (rel. diff 1.77e-7), NOT the 1/2
that would align the field-equation face with the RAR face; "the closed
sourced-equation face (G155, dead) would carry a √(8π)-class a0-shift; the
LIVE equilibrium reading is unaffected" (YM01.out:36-41;
YM_GAP_STATEMENT:53-58). The profile TABLES are map-dependent; the closing,
monotonicity, and deep-law structure are map-independent (YM01.out:41). G1b
is the named follow-up gate; a referee who upgrades D1 to a kill must show
which committed normalization absorbs the map — none is shown on the record.

### (e) TOE_STATUS — "LACKS the electroweak/QCD sector … the SM bridge is DEAD by the null" — **ALIVE (no re-raise; the registered boundary holds)**

B04/B4: the pre-registered 3-Z² family scan (15 members × 3 rungs, expected
count 0.10 at 1% tolerance) finds exactly ONE survivor — the m_e/100.531 hook
itself (z = −0.058σ); E_chance = 0.10 = 300× above the family-wise E* =
3.3e-4; "m_e/100 STANDS AS A SINGLE COINCIDENCE"; falsifier registered: any
measured m_i/100.531^n within 1% of a rung re-opens it (TOE_STATUS.md:89-90;
WAVEBOARD.md:1570-1574). And "the null and B4 bound the claim: the 5.09 keV is
the equilibrium's number, not SM numerology" (TOE_STATUS.md:56); the
m_e/32π = 5.083 keV adjacency is adjudicated purely arithmetic
(TOE_STATUS.md:80). The door's absolute scales at the pinned m = 5.09 keV —
m_A(8.2 kpc) = 3.88 keV, range 5.08e-11 m, ν_gap = 9.39e17 Hz (YM01.out:77) —
are μ₂-machinery products of committed constants (√μ₂(0.2276) = 0.5800, ratio
law D2, YM01.out:56-58); the door makes NO SM-ratio claim for any of them,
and the 5.09 keV enters at its registered status (ladder-derived, SM-adjacent
only through the adjudicated single coincidence). RULE: the null's gate is
unchanged; the pinned gap re-exhibits the registered number without adding a
new coincidence; the moment anyone claims an SM MECHANISM for m_A, B04's
falsifier (a measured m_i/100.531^n within 1% of a rung) re-opens and the
bridge dies again — the door does not claim it.

### (f) m = m_dust — identification or fit? — **BOUNDARY-REGISTERED (an identification, NOT a fit — and NOT a derivation; it needs a falsifier)**

The LADDER side is derived, not fitted: m = k_B T_0(1+z\*)/σ² is the
environment-blind fixed point — C02 (Lean 8/8): 101,600 (m, σ) environments,
max |m_rec − m| = 4.3e-14 keV; B03's 11 committed rungs recover
[4.99997, 5.00009] keV at 0.00012 spread (WAVEBOARD.md:1634-1641). G212's
mass triangle converged m = 5.09 ± 0.10 keV from three independent channels
(posterior 5.089 ± 0.097, intersection [5.000, 5.200], chi2 = 1.04,
WAVEBOARD.md:1245-1251); TOE_STATUS carries m as "the ledger's one derived
row" (:23). The DOOR's move — m_gauge = m_dust — is the identification, and
here the framework's own precedent cuts the other way. L4's
equilibrated_is_phantom is an identification WITH a certificate AND a test:
coefficient exactly 1, Lean-certified ("equilibrated_is_phantom — THE
IDENTIFICATION", THE_THEORY.md:43-50, :284-285), and the r^-2 law is
observable. The Stueckelberg identity has NEITHER: (1) no certificate — C02
certifies the ladder's environment-blindness, not the identity of the gauging
scale with the dust mass; the identity's warrant is L10's one-species claim
(the dust carries the shift charge, THE_THEORY.md:32-37, :155-168) — a
coherence argument, not a proof; (2) no test — D2/D3 cancel m ("one number
per radius, m cancels", YM01.out:56-58) and D6 registers the absolute scale
SILENT: "the fiducial absolute scale (m = Λ) is SILENT to laboratory probes
by the framework's own rules … silence is registered honestly as 'structure
proven, observability silent', never upgraded to 'detected'" (YM00:89-92;
YM01.out:79-81) — the identification is unfalsifiable at the absolute level
by the framework's own ledger; (3) a parameter-count cost — G089: "EXACTLY
ONE free dimensionless parameter (Z ↔ Ω_Λ)" (WAVEBOARD.md:56-59; G152
re-affirms, :567-572), while the door itself prices m: "One new constant: the
gauging scale m is the door's price … m = Λ is the one-constant fiducial, NOT
a derived value" (YM_GAP_STATEMENT:49-52) — the door's OWN registration is
the weaker (new-constant) claim; m = m_dust is the stronger (inherited)
claim, and it is the one that needs a falsifier. RULE: carried as an
assumption with a named falsifier → honest; upgraded to "derived" → cites C02
beyond its scope. Falsifier for the identification: any measured absolute
pinning inconsistent with √μ₂·m at the committed m (a dust-dust Yukawa range,
a fifth-force-class bound excluding a sub-micrometric carrier with
(m/M_pl)² coupling), or the ladder's own registered kill band m < 4 or
m > 6 keV (G168, WAVEBOARD.md:875-882) — which kills the pinning without
touching the shape law.

### (g) The Clay problem — what the proof covers, what it does not — **BOUNDARY-REGISTERED (K5, pre-registered; the scope statement is exact)**

NOT covered: the SU(3)-class continuum Yang-Mills Hamiltonian's spectral gap.
No QCD sector exists anywhere on the record (TOE_STATUS.md:89-90: "LACKS —
the electroweak/QCD sector … a mechanism exists only where a member lands,
and none lands"); no non-Abelian sector, no confinement, no glueballs, no
quantum spectral statement of any kind (E02: no quantization —
TOE_STATUS.md:58-72). K5: "NOT A KILL — the SU(3)/QCD-scale gap is explicitly
OUT OF SCOPE (the framework has no QCD sector; an honest lane does not claim
it)" (YM00:72-76); YM01 K5: "this lane proves the framework's OWN gap
mechanism + scale law and does NOT claim the Clay problem" (YM01.out:98-100);
the Lean header repeats it verbatim: "Nothing here claims the SU(3)/QCD-scale
gap (the Clay problem)" (YM01_gap.lean:24-26). COVERED, exactly: the
framework's own sector's gap mechanism — m_A² = μ₂(u)m² (clean) and
m_A² = m²u(u²+3u+4)/(1+u)³ (exact), residual 0 (YM01.out:17-25); the Proca
dispersion ω(k) = √(k² + m_A²) ≥ m_A attained at k = 0, with n ≥ 1
excitations costing ≥ m_A (the Fock face: Lean `gap_theorem`, `gap_tight`,
`excitation_gap`; 19 theorems, exit 0, zero sorry, axioms
{propext, Classical.choice, Quot.sound} — YM_GAP_STATEMENT.md:4-6, :37, :77);
the parameter-free spatial law (D2 ratios 0.5379–1.2509; deep law −1/2 +
(9/8)u, D3a/D3b; vacuum/strong-field closing D4 — YM01.out:47-67). RULE: any
headline claiming the Clay prize through this lane is a KILL by K5; the
door's own statement is safe.

---

## THE VERDICT

**Scorecard: ALIVE 3 ((c) zero-gap face preserved; (d) G155 stays closed;
(e) no numerology re-raise) · BOUNDARY-REGISTERED 4 ((a) L5 letter + K3
override; (b) G054 scope; (f) m = m_dust, unfalsifiable assumption;
(g) Clay out of scope) · KILLED 0.** The door's own pre-registered gates pass
20/20 (K1–K5, YM01.out:86-100) and the algebra is Lean-certified; every kill
class that could fire on it is on the pre-registered record. The door is the
strongest structure the framework has produced — and it is strong exactly
because its circumscriptions were printed before the numbers landed.

**THE SINGLE MOST VULNERABLE ASSUMPTION (the one a hostile referee attacks
first): m = m_dust — the identification of the Stueckelberg scale with the
ladder mass.** Not the L5 letter (K3 pre-registered the override, and the
physical class — Lorentz-invariant mass term, α₁ = α₂ = 0 by structure — is
preserved), not the profile (D2/D3 are parameter-free and carry their own
falsifiers), not the G155 door (untouched), not the Clay scope (disclaimed in
print). The identification is the only plank that (1) has NO falsifier — D2/D3
cancel m and D6 declares the absolute scale silent (YM00:89-92); (2) has NO
certificate — C02 certifies the ladder, not the identity (WAVEBOARD.md:1634-
1641); and (3) costs the framework its one-parameter claim (G089/G152 vs "one
new constant", YM_GAP_STATEMENT:49-52). The referee's first attack is the L5
letter ("no vector sector") — and the door survives it ONLY through K3's own
override clause; the referee's SECOND attack, the m-identification, has no
such shield, because the door's own statement prices m as a new constant
while the framework-level reading inherits it as derived. The first attack
kills by registration; the second kills by unfalsifiability.

**THE FALSIFIER THAT WOULD KILL THE DOOR:** (1) structure-level (kills
m_A > 0 anywhere): a committed massless-vector signature INSIDE the phantom
at μ₂ > 0 scale; a gap that fails to close in the Solar System / beyond the
EFE cap; a preferred-frame observable α₁/α₂ ≠ 0 that G054's class forbids —
the pre-registered falsifier recipe (YM00:78-93; YM_GAP_STATEMENT:60-69).
(2) identification-level (kills the pinning, not the shape): any measured
absolute-scale pinning inconsistent with √μ₂·m at the committed m, or the
ladder's registered kill band m < 4 or m > 6 keV firing (G168,
WAVEBOARD.md:875-882). Either class ends the door as claimed; the door's
survivability is the honesty that both were printed in advance.