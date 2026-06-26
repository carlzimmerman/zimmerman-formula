# Koide as the Self-Dual Point of singlet↔doublet exchange — DEVELOP verdict

**C. Zimmerman, 2026-06-25 (banked 2026-06-26).** *Patient INVENTION-mode build on the
"Koide = self-dual point" reframing: the √-mass vector v=(√mₑ,√m_μ,√m_τ) splits under S₃ into the
trivial singlet (democratic axis n=(1,1,1)/√3) ⊕ the standard doublet (orthogonal plane); θ=∠(v,n)
gives cos²θ = 1/(3Q); the duality θ→90°−θ swaps |P_singlet|↔|P_doublet|, which on Q is the Möbius
involution Q→Q/(3Q−1) with unique physical fixed point Q=2/3. **THE BAR (non-circular):** a WIN needs
an INDEPENDENT physical Z₂ that ACTS as the singlet↔doublet swap for a reason NOT involving 2/3 / 45°,
with Koide falling out as the forced self-dual point. Tooling: sympy 1.13.1 + mpmath dps≥45, clean-room
(`/tmp/koide_selfdual_verify{,2,3,4}.py`). Quarantine held: 2/3, √2, r enter only as the empirical target.*

---

## VERDICT: **(C) NULL — tautological kinematics. The 173rd re-labeling.**

The self-dual **reframing is mathematically exact, real, and the cleanest geometric statement of what
Q=2/3 means** — full credit, stated below. But it is **NOT a derivation**. The involution θ→90°−θ has
cos²θ=½ as its fixed point for *any* vector, *any* axis, in *any* ambient dimension; it is the bare
kinematic statement "45° bisects a line and its orthogonal complement," carrying zero physics. The
"duality" Q→Q/(3Q−1) is that same reflection pushed through the change of variables Q=1/(3cos²θ); its
involutivity and its unique fixed point 2/3 are **forced by the algebra of the definition, not by any
dynamics.** The decisive test: **the lepton SPECTRUM is invariant under the swap only because the
leptons already sit at 45°** — applied to the quarks (same S₃ structure) the swap maps them to
non-physical configurations and relates no two physical sectors. It is therefore **no symmetry of
flavor dynamics**, just a geometric relabel of angles. Same wall as the banked corpus
(D3_SELFDUALITY, KOIDE_CHANNEL_MEASURE, KOIDE_CHANNEL_COUNT_SMUGGLE, KOIDE_FROM_DSUNRUH), reached here
from the **duality-physics axis** and closed cleanly.

---

## The KEY discriminator (sharp): contentful duality vs geometric relabel

A duality is **contentful** iff the *dynamics* (action / spectrum) is invariant under it. Test on the
quark control sectors, which share the identical S₃ 1+2 √-mass decomposition (mpmath dps=45,
Block 6):

| sector | Q | θ | swap → Q′ | swap → θ′ | image physical? |
|---|---|---|---|---|---|
| charged leptons (e,μ,τ) | 0.6666605 | 44.99974° | 0.6666728 | 45.00027° | ≈ identity (already at 45°) |
| up quarks (u,c,t) | 0.848981 | 51.20028° | 0.548812 | 38.79972° | **NO** — not a physical spectrum |
| down quarks (d,s,b) | 0.731428 | 47.53983° | 0.612441 | 42.46018° | **NO** — not a physical spectrum |

Cross-pairings: 90°−θ(leptons)=45.0003° vs θ(up)=51.20° (no), vs θ(down)=47.54° (no);
90°−θ(down)=42.46° vs θ(up)=51.20° (no). **The swap relates NO two physical sectors.** It is the
identity on the leptons *only because they already lie at θ=44.9997° / Q=0.66666* — the spectrum is
swap-invariant **because** Q is already 2/3, not the reverse. Applied to real quark spectra it produces
non-physical configurations. **⟹ the swap is not a symmetry of any flavor Lagrangian/spectrum;
Q→Q/(3Q−1) is a geometric relabel of angles = TAUTOLOGICAL-KINEMATIC.**

---

## What is EXACT and REAL (genuine credit, both ways — verified clean-room dps≥45)

| Fact | Status |
|---|---|
| Q = 0.6666605 (θ = 44.99974°, cos²θ = 0.500005); data at the self-dual cone to ~5e-6 rel | **EXACT** ✓ (−9.2e-6 vs 2/3, τ-mass-limited) |
| cos²θ = (Σ√m)²/(3Σm) = 1/(3Q) | **EXACT** ✓ |
| f(Q)=Q/(3Q−1) is an involution (f∘f = Q) | **EXACT** ✓ |
| Fixed points of f: {0, **2/3**}; Q=0 degenerate ⟹ **2/3 unique physical** | **EXACT** ✓ |
| θ→90°−θ (cos²→1−cos²) **IS** the Möbius map Q→Q/(3Q−1) | **EXACT** ✓ (1/(3Q′)=1−1/(3Q)) |
| f conjugate to w→−w via h(Q)=(Q−2/3)/Q: h(f(Q)) = −h(Q) | **EXACT** ✓ (same Z₂ type as S-duality τ→−1/τ) |
| {singlet=trivial irrep, doublet=standard irrep} of the √-mass vector under S₃-natural-3 | **HONEST rep theory** ✓ |
| Framework hosts S₃ 1+2 via Spin8 triality | **HOSTED** ✓ |

This is the cleanest geometric statement of *what* 2/3 means: **Q=2/3 ⟺ |P_singlet v| = |P_doublet v|
⟺ the unique physical fixed point of the singlet↔doublet projection-magnitude involution.** Worth
stating. Not high-priested away.

---

## Why it is NULL, not a lead — the three lethal obstructions (re-verified)

**1. UNIVERSAL-BISECTOR (zero physics) — Block 4.** cos²θ=½ is the fixed point of the swap cos²→1−cos²
for a *random* vector and axis in **every** dimension d=2..7 (checked). 45° is just the bisector of any
line and its orthogonal complement. The fixed locus carries **no** information about S₃, leptons, or
masses — it is the same number whatever the spectrum. The involution's fixed point being 2/3 is forced
by the definition Q=1/(3cos²θ), not by physics.

**2. S₃ stabilizes singlet & doublet SEPARATELY (no group element swaps them) — Block 5.** On the real
masses |P_s|=30.68425, |P_d|=30.68397 (equal to ~9e-6 ⟹ the 45° cone). All 6 S₃ permutations leave
**both** norms individually invariant — forced, because an irrep decomposition is group-invariant, so
the group that produces the 1+2 split *cannot* enact the exchange. The swap is an O(3) reflection across
the θ=45° cone distinguished by **nothing in S₃ alone**; it can only be pinned by NAMING equal-norm/45°.

**3. DIMENSION-MISMATCH (no linear duality can be the swap) — Block 7.** A linear bijection of R³
preserves subspace dimension; it cannot map a 2-plane into a 1-line. So **no linear involution swaps the
dim-1 singlet with the dim-2 doublet.** The "duality" really lives on the single free modulus
r=|P_d|/|P_s| as a Möbius map (geometric r→1/r, fixed at equal norms; the corpus' amplitude modulus
r→2/r, fixed at √2 — same 45° cone, different normalization of the doublet's 2 components). Either way it
is a map on the **free amplitude** and is a "symmetry" *only at the value it must explain*. Any realizing
physical duality must therefore be **nonlinear/field-space with its own equal-norm fixed point**, mapped
to the S₃ angle by an external dictionary — which no surveyed duality supplies.

---

## Dualities surveyed — none clears the bar (both axes: flavor-duality + dS/triality)

| candidate duality | acts as singlet↔doublet swap? | why it fails |
|---|---|---|
| electric-magnetic / S-duality τ→−1/τ | **no** | the Möbius match is purely formal (every order-2 Möbius map is conjugate to w→−w); no τ↔Q dictionary, τ lives on gauge-coupling field space |
| particle-vortex / level-rank | **no** | electric/magnetic dof of a 2+1 CFT; no map to the S₃ √-mass projection angle |
| UV-IR | **no** | the framework's own UV/IR self-dual *radius* r→r_s R_H/r is a **different object** (DEEP_GEOMETRY), unrelated to the S₃ angle |
| seesaw Dirac↔Majorana (Singh EJA δ²: 3/2↔3/8) | **no** (least-bad) | touches the same S₃ 1+2 and the **Dirac** point δ²=3/2 *is* self-dual (|singlet|²=3c²=2d²=|doublet|²); but the "halving" δ→δ/2 **shrinks** the doublet (θ:45°→26.6°), it is NOT the involution (θ_Dirac+θ_Maj=71.6°≠90°; f(2/3)=2/3 not 5/12) |
| mirror / T-duality | **no** | no dictionary to the projection angle |
| dS antipodal map (X→−X) | **no** | O(d+1,1) spacetime Z₂, flavor-blind by Coleman–Mandula |
| static-patch complementarity / dS-CFT | **no** | spacetime/holographic Z₂s, no S₃-irrep action |
| **Spin8/triality order-2 element** | **no** | irrep-invariance: the order-2 transposition (8v↔8s fixing 8c) leaves |P_s|,|P_d| separately invariant (Block 5); triality *breaking* halves δ² (3/2→3/8) ⟹ Q=5/12, not 2/3 (Singh arXiv:2108.05787) |
| Shulga 2026 (arXiv:2605.10245, rank-one detQ=0 ⟹ s²=2|d|²) | **no** | reaches the equal-norm cone but **engineered** via the coherence/Sumino choice; by the authors' own words "not a second independent derivation" — circular by the bar |

**Decisive rep-theoretic obstruction (kills all uniformly):** θ→90°−θ swaps the magnitudes
|P_s|↔|P_d|, but (a) a 1-dim and a 2-dim irrep cannot be exchanged as subspaces (dimension mismatch),
and (b) every S₃ element leaves (|P_s|,|P_d|) invariant. The involution is a reflection across the 45°
cone — an O(3) element pinned by NOTHING in S₃ — so any realizing duality must already carry an
independent reason for the equal-norm cone. None does.

---

## Already tried — YES (this is the 173rd re-labeling; corpus adjudicated the identical move)

All at `/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/`, multiple times this week:

- **D3_SELFDUALITY_VERDICT_2026-06-25.md** — ruled a structurally identical "self-dual point = forced"
  claim **DECORATIVE/CIRCULAR** ("cannot predict or falsify anything 3 cannot already"). *(That file is
  the gravity-side d=3 self-duality; the present file is its flavor-side analog, same wall.)*
- **KOIDE_CHANNEL_MEASURE_VERDICT_2026-06-25.md** (the "171st") — r=√2 is the p=0 **non-covariant**
  endpoint of weight∝dim^p, chosen because it hits 2/3; every covariant/thermal measure → r=2, Q=1
  overshoot. The |singlet|²=|doublet|² equipartition the present involution's fixed point re-expresses.
- **KOIDE_CHANNEL_COUNT_SMUGGLE_CHECK_2026-06-25.md** (the "170th"), **KOIDE_FROM_DSUNRUH_2026-06-20.md**
  (the "165th"), **KOIDE_IR_MECHANISM_2026-06-17.md** — same wall, re-confirmed clean-room (wjx8gedyb).

External literature: Brannen's circulant/phase Koide parametrization and the broad "2/3 = equal-
projection / maximal / special point" literature already observe 45° as the equal-amplitude locus;
**Sumino (arXiv:0903.3640) IMPOSES 2/3** as a tuned potential minimum + per-flavor radiative lock (his
own words: "deliberately choosing a specific form of the potential," "accidental factor (or parameter
tuning)" α=¼α_F) — **not** a duality. None derives 2/3 from a dynamical self-duality.

---

## New falsifiable content IF it were genuine — and why the prediction FAILS (the selector test)

If the singlet↔doublet self-duality were a real **flavor-blind** symmetry (which any S₃/dS/triality
duality is, by the equivalence principle), it would force θ=45° / Q=2/3 in **every** fermion sector.
That is a sharp, falsifiable prediction — **and it is FALSIFIED by the quarks** (mpmath dps=45):

| sector | Q | vs 2/3 |
|---|---|---|
| charged leptons | 0.6666605 | −6e-6 (hits) |
| up quarks | 0.848981 | +0.182 (**miss**, robust to ±30% mass) |
| down quarks | 0.731428 | +0.0648 (**miss**) |
| neutrinos (NO) | 0.585 (m₁=0) … 0.336 (m₁=0.05 eV) | free function of m₁ |

**LEPTON-SELECTOR: ABSENT (fatal).** The S₃/dS/triality structure supplies no selector; a flavor-blind
duality forces 45° on quarks too ⟹ falsified. So the reframing makes **no surviving new prediction** —
its only would-be prediction (universal self-duality) is already dead.

---

## The one un-foreclosed avenue (a SEARCH for new dynamics, not content the involution supplies)

To clear the non-circular bar one must exhibit an **independent, LEPTON-SPECIFIC, DYNAMICAL** duality of
a *real flavor action* (a genuine S-duality / particle-vortex / level-rank / UV-IR analog) whose
self-dual locus is the spectrum's IR fixed point and lands θ=45° for a reason that **never mentions
2/3 / 45°** — precisely the **Sumino-class lepton-selective IR protector** the corpus already named as
the sole open C-path (KOIDE_CHANNEL_MEASURE lines 162–166). Two further constraints any such object must
clear: it must (i) **break flavor-blindness** (else quarks falsify it), and (ii) **land 2/3 without
tuning** (the open lepton-selector problem). A residual-Z₂ **modular-flavor** model (à la Feruglio, with
τ pinned at a self-dual point i/ω and a rep assignment tying it to the charged-lepton 1+2) is the one
exotic family I did **not** exhaustively foreclose — but it would still face (i) and (ii). **That is new
dynamics to be found, not content the geometric involution provides.**

---

## Ledger

| Claim | Verdict |
|---|---|
| Q=2/3 ⟺ \|P_s\|=\|P_d\| ⟺ unique physical fixed point of the involution | **EXACT REFRAMING** (real credit) |
| Q→Q/(3Q−1) involution; conjugate to w→−w; data at cone to 5e-6 | **EXACT** but **definitional algebra** (zero physics) |
| cos²=½ fixed for any vector/axis/dimension | **UNIVERSAL BISECTOR** (Block 4) ⟹ no information content |
| S₃ swaps singlet↔doublet | **IMPOSSIBLE** — all 6 elements fix both norms (Block 5); dim mismatch (Block 7) |
| lepton **spectrum** invariant under the swap | **NO** — identity only because already at 45°; quarks → non-physical (Block 6) |
| any surveyed physical duality acts as the swap | **NONE** (S/particle-vortex/UV-IR/mirror/dS/triality/seesaw/Shulga all fail) |
| flavor-blind self-duality prediction (universal 2/3) | **FALSIFIED by quarks** (selector absent) |
| already tried | **YES** — 173rd re-labeling; D3_SELFDUALITY + KOIDE_CHANNEL_MEASURE already at this wall |
| derivation of 2/3 from a dynamical self-duality | **NONE** (corpus + literature) |

**NET: NULL — tautological-kinematic.** A genuine, exact, elegant self-dual **reframing** of what Q=2/3
means; **NOT** a non-circular derivation. The spectrum is not self-dual as dynamics — it sits at the
fixed point, and the involution is a geometric relabel of the 45° cone, falsified as a prediction by the
flavor-blind quark control. r (= √2 / equal-norm) stays free (drifts ~178σ under RG); no lepton-selector;
literature self-duality engineers, not derives. **No manufactured win; no high-priesting of the real,
exact, hosted shape.** Consistent with the banked corpus, reached from the duality-physics axis.

**Scripts (clean-room, this session):** `/tmp/koide_selfdual_verify.py` (Q/involution/conjugacy),
`verify2.py` (universal-bisector + S₃ swap-invariance), `verify3.py` (quark-control spectrum test),
`verify4.py` (dimension-mismatch + modulus involution). Banked:
`D3_SELFDUALITY_VERDICT_2026-06-25.md`, `KOIDE_CHANNEL_MEASURE_VERDICT_2026-06-25.md`,
`KOIDE_CHANNEL_COUNT_SMUGGLE_CHECK_2026-06-25.md`, `KOIDE_FROM_DSUNRUH_2026-06-20.md`.
