# Koide via Triality / Octonions: does Spin(8)-triality / J3(O)-F4 FORCE 45° (r=√2, Q=2/3)?

**Date:** 2026-06-26 (clean-room re-derivation, sympy + mpmath dps≥30, anti-circularity-guarded)
**Verdict:** **OBSTRUCTION-ROBUST — the octonionic home HOSTS the 1+2 but does NOT force 45°.**
**Scripts (LOCAL):** `/tmp/triality_verify.py`, `/tmp/albert_verify.py`, `/tmp/octonion_verify.py`
**Do NOT git-push.**

---

## The question (the "last stone")

The inequivalent-irrep obstruction killed ordinary flavor-S3: the perm rep on 3 √-masses is
`1 (singlet, trivial) + 2 (doublet, standard)`, and because singlet and doublet are **inequivalent**
irreps, no group element equates their magnitudes → the ratio `r = |doublet|/|singlet|` is a free
modulus, and `Q = 1/3 + r²/6` (phase-independent) leaves `Q=2/3 ⟺ r=√2` un-forced.

FRESH HOPE: **Spin(8)-triality** is the outer-automorphism S3 that permutes the **EQUIVALENT** reps
8v / 8s / 8c. The framework's gauge home is **J3(O)/F4** (Albert algebra, 27 = 3 real diagonal + 3×8
octonionic off-diagonal, cubic norm, F4 = Aut(J3(O))). Does this *richer, equivalent-reps* structure
output 45° non-circularly, evading the obstruction? Plus: does octonion non-associativity supply a
forced √2 the associative S3 lacks?

---

## What was computed (all clean-room, anti-circularity = output r, never input a chosen element)

### Empirical ground truth (mpmath, PDG masses)
`Q_lepton = 0.6666605`, `Q − 2/3 = −6.2×10⁻⁶`, angle to (1,1,1) = `44.99974°`, `cos² = 0.500005`.
A genuine 45-year, FDR-surviving (~1-in-44k) puzzle. We treat it as real, not numerology.

### [A] The 1+2 obstruction is DIMENSION-INDEPENDENT (the decisive structural fact)
Character of the permutation rep on **3 objects**: χ = (3,1,0) over classes (e, transposition, 3-cycle).
Decomposition (sympy-exact): `mult(trivial)=1, mult(sign)=0, mult(standard)=1` → **3 = 1 + 2**.
This depends ONLY on permuting **3 objects** (χ = #fixed points), **NOT** on whether those objects are
1-dim flavors or 8-dim Spin(8) reps. **Any** S3 permutation rep on 3 things is 1+2 by character —
identical for flavor copies and for {8v,8s,8c}. The equivalence of the 8's does **not** change the
1+2 split on the **generation** axis where r lives.

### [B] Q = 1/3 + r²/6, phase-independent (sympy-exact)
Brannen circulant √m_k = μ(1 + r·cos(δ + 2πk/3)): `Q(μ,r,δ) = r²/6 + 1/3` — the circulant phase δ
**cancels identically**. So **r is the entire unforced content**; Q=2/3 ⟺ r=√2 ⟺ 45°.

### [C] J3(O)/F4 cubic norm is SILENT on the amplitude (non-injective on Q)
The complete F4-invariants of X ∈ J3(O) are the three characteristic-cubic coefficients
`(T1=tr, T2=2nd-sym, N=det)`. Load-bearing identity (sympy-exact): **Q = 1 − 2·T2/T1²**, so
**Q=2/3 ⟺ 6·T2 = T1²**. But T2 is an **independent** char-poly coefficient: fixing tr(X) **and**
det(X)=N still leaves T2 — hence Q — **free**. Explicit witness: triples with T1=6, N=6 but different
T2 give Q = 0.18 (x=0.5), 0.39, 0.47 (x=4). **No F4-invariant condition (trace, cubic norm, or both)
pins the eigenvalue vector to 45°.** The eigenvalues are a genuine 3-parameter family.

### [D] No F4-DISTINGUISHED element lands at 2/3
Identity/democratic (1,1,1) → Q=1/3; primitive idempotent (1,0,0) → Q=1; rank-2 idempotent (1,1,0)
→ Q=1/2; idempotent spectra ∈ {0,1}³ → Q ∈ {1/3, 1/2, 1}. The algebra PICKS OUT only **rational**
special points; **2/3 is the measure-zero irrational midpoint**, reached only by a non-canonical
element whose 3 eigenvalues are **TUNED** to the lepton ratio (i.e. *input*, not output).

### [E] Triality (Singh) forces the SHAPE at the WRONG amplitude
The exceptional-Jordan / triality construction (Singh 2108.05787) genuinely DERIVES an equally-spaced
√-mass shape (μ−δ, μ, μ+δ) → `Q = 1/3 + (2/9)(δ/μ)²` (sympy-exact). Triality-forced spread
δ/μ = √(3/8) → **Q = 5/12 = 0.4167, NOT 2/3.** Reaching 2/3 needs δ/μ = **√(3/2)**, which Singh's own
paper flags as "disagrees with known values." So triality forces a Koide-shape at the wrong amplitude;
2/3 is INPUT via a chosen signature, not OUTPUT.

### [F] Genuine forced octonionic √2's exist — but in the WRONG slot
The honest both-ways check: the algebra DOES carry forced √2's.
- **F4 = Aut(J3(O)) root lengths long:short = √2** (sympy: this is real and forced).
- G2 long:short = √3 (not √2); D4=so(8) all roots length √2 → ratio = 1 (global scale, no ratio);
  associator norm of off-line octonion triples = 2 (not √2).

But F4's √2 is a ratio of **gauge root lengths** in the 52-dim Lie algebra. Koide's r is a ratio of
**generation √-mass amplitudes** in the 3-vector. The √-mass eigenvalues are **F4-invariants**
(char-poly coefficients); root lengths are **adjoint** data. No F4-equivariant map sends a root-length
ratio to a mass-eigenvalue ratio. **The √2 exists but is in the wrong slot — using it for r is tuned.**

### [G] Schur: where triality-equivalence DOES bite, it forces r=0 (the WRONG point)
Triality is **OUTER**, so 8v, 8s, 8c are pairwise **inequivalent as Spin(8)-reps**. By Schur,
`Hom_{Spin(8)}(8a, 8b) = 0` for a≠b, = ℂ·Id for a=b. A Spin(8)-equivariant (gauge-allowed) operator on
8v⊕8s⊕8c is therefore **block-diagonal scalars** `diag(c1·Id, c2·Id, c3·Id)` — structurally identical
to 3 flavor copies. The genuine real intertwiners 8v→8s exist (they implement the outer auto) but are
**NOT Spin(8)-equivariant** → gauge-noncovariant → inadmissible as mass terms; using one to set
singlet=doublet **is** inputting a chosen element. And where the equivalence DOES act admissibly
(equating the three 8-magnitudes), it forces |8v|=|8s|=|8c| ⟹ c1=c2=c3 ⟹ **democratic point r=0,
Q=1/3** — the exact OPPOSITE of 45°.

### [H] Wrong space (the cleanest statement)
Triality's outer-S3 permutes three **8-dim** reps in the **internal octonion fibre**. Koide's 1+2 lives
in the generation-S3 on **R³** (the 3 √-masses) on the **generation base**. These are different S3
actions on different spaces. The equivalence 8v~8s~8c (as abstract reps) says **nothing** about the
1+2 split of an R³ vector. The equivalence is **orthogonal** to the amplitude r.

---

## Did the equivalence of the 8's change the magnitude argument?

**No — and identifying WHY sharpens the obstruction.** The obstruction was never *really*
"the irreps are inequivalent." It is deeper and more robust:

> **No admissible (gauge-covariant) operator equates a symmetric-singlet magnitude with a
> doublet-norm.** The 1+2 decomposition is itself **group-invariant** — every group/algebra element
> (including the triality transposition / the 8v↔8s swap) preserves |P_singlet| and |P_doublet|
> **separately**. The very symmetry that BUILDS the 1+2 split provably cannot enact the exchange.

Triality's equivalence lives **sideways** in the 8-dim fibre, gauge-noncovariant on the generation
axis. It changes nothing about r because (a) the 1+2 split is dimension-independent (it's a property of
permuting 3 objects, not of the objects' internal equivalence), and (b) by Schur the only admissible
operators are block-diagonal scalars, which can equate the three magnitudes only at the democratic
r=0 point. So the obstruction is **deeper than irrep-inequivalence** — it is a covariance/measure
statement, robust to swapping in equivalent reps.

---

## Both-ways credit (the structure is NOT sterile — state it loudly)

- **Right symmetry neighborhood, real hosting hook.** J3(O)/F4 supplies exactly the 1+2 democratic +
  standard decomposition a Koide circulant needs, with three **real** eigenvalues that ARE the natural
  √-mass triple and an invariant triple (T1, T2, N) that cleanly restates Koide as Q = 1 − 2T2/T1².
- **Triality permits genuine isomorphisms** (8v~8s~8c via real algebra automorphisms), unlike mere
  flavor relabelings — a real structural distinction, correctly identified.
- **Singh genuinely DERIVES the Koide SHAPE** (equal spacing / 1+2) from the algebra, not by hand.
- A **forced octonionic √2 really exists** (F4 long:short = √2) — it just doesn't map to r.
- The load-bearing identity Q = 1 − 2T2/T1² (= 1/3 + r²/6) is a clean F4-invariant restatement.

This is the right HOME, with a real forced SHAPE. It is **not** numerology.

---

## Both-ways concede (no manufactured win)

For three converging exact reasons, J3(O)/F4 does **not** force 45°:
1. **Cubic norm silent on amplitude** — T2 independent of (tr, det), so Q is free; eigenvalues are a
   3-param family.
2. **No F4-distinguished element at 2/3** — all canonical elements give rational Q∈{1/3,1/2,1}; 45° is
   the irrational midpoint, reached only by a tuned element.
3. **Triality forces the shape at the wrong amplitude** (Q=5/12); 2/3 needs the chosen √(3/2)
   Singh flags as data-disagreeing.

And the triality-equivalence lever specifically fails: dimension-independent 1+2, gauge-noncovariant
sideways equivalence, Schur block-diagonal → democratic r=0 where it bites. **The forbidden
magnitude-equating operator stays forbidden.**

---

## VERDICT

**OBSTRUCTION-ROBUST — hosts, does not force.** The Spin(8)-triality / J3(O)-F4 octonionic structure
HOSTS the Koide 1+2 shape (right home, forced shape, real forced √2 in F4) but does **not** force the
amplitude r=√2 / 45° / Q=2/3. The inequivalent-irrep obstruction is not evaded — it is actually
**dimension/algebra-robust**, deeper than irrep-inequivalence: no gauge-covariant operator equates a
symmetric-singlet with a doublet-norm, and the genuine 8v~8s~8c equivalence lives orthogonally in the
internal fibre (and where it bites, forces the wrong r=0 point). **r=√2 stays the entire unforced
content of Koide.** Consistent with and sharpening the banked verdicts (KOIDE_MECHANISM_SUMINO,
KOIDE_IR_MECHANISM, KOIDE_DIRAC_BRIDGE circularity theorem, KOIDE_CHANNEL_MEASURE).

**NOT "no doors":** a gauged U(3)/triality Sumino-class lepton-selective family sector with a potential
minimizing at r=√2 remains a standing posit — the open 45-year physics problem itself. The
triality-equivalence mechanism specifically does not open it; a real solution still needs
lepton-selective IR dynamics (Sumino-class, with its own tuned α_F=4α) the gravity/triality spine
provably cannot supply (flavor-blind by the equivalence principle).
