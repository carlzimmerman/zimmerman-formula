# agentUU — ROUTE 2: the DSSYK<->dS dictionary AT THE STATE LEVEL (2026-06-13)

**The lock under test.** agentSS (eb26ee4b) and agentTT (ddf212d8) independently named the SAME missing
structural ingredient: an *algebra-internal Tomita-Takesaki uniqueness statement closing DSSYK<->dS at the
STATE level*. IF DSSYK<->dS is a state-level *-isomorphism of von Neumann algebras (matching cyclic-separating
vectors), TT-uniqueness forces the matter chord's modular flow to EQUAL the GH boost -> forces BOTH the center
placement (TT/Link 8) AND the matter spectral/gain structure (SS/Link 5) in one stroke.

**This route's job (the load-bearing fact):** is the state-level isomorphism
  (a) PROVEN in the literature  => the lock FIRES, both gaps forced;
  (b) TYPE-COMPATIBLE but unproven => CONDITIONAL, the named new-physics step;
  (c) TYPE-OBSTRUCTED (types differ => no *-isomorphism possible) => the whole DSSYK<->dS route is WOUNDED.

A *-isomorphism of von Neumann algebras PRESERVES the Murray-von Neumann TYPE. So matching types is a
NECESSARY condition. Mismatched types => obstruction (c). Matching types => necessary-but-not-sufficient (b or a).

---

## STEP 1 — the von Neumann TYPES on each side (necessary condition)

### The types (primary-source abstracts, fetched this run)

| Side | von Neumann type | Source (abstract-verified) |
|---|---|---|
| dS static-patch OBSERVER algebra | **type II_1** | CLPW arXiv:2206.10780 ("The algebra is a von Neumann algebra of Type II_1") — II_1 via crossed product of the type III_1 QFT algebra by the modular boost, regularized by the observer Hamiltonian |
| DSSYK single-sided-BH boundary algebra | **type II_1** | Cao-Gao arXiv:2511.01978 ("...has a non-trivial commutant and is a type II_1 vN factor") — AdS/BH sector |
| DSSYK q-Askey observer algebra | **type II_1** (or I_inf, operator-dependent) | Aguilar-Gutierrez-Kukolj-Seitz arXiv:2605.13956 ("can be type II_1 or type I_inf factors, depending on the operators included") |

**Necessary-condition result: TYPES MATCH.** Both the dS observer algebra and the DSSYK chord algebra (with one observer/constraint) are **type II_1**. So case (c) TYPE-OBSTRUCTED is **RULED OUT** — there is no type obstruction to a *-isomorphism. (The DSSYK side can also present as I_inf without the observer constraint; the *matched* observer-dressed sector is II_1 on both sides, which is the relevant comparison.)

---

## STEP 2 — is type-matching SUFFICIENT? (does (b) collapse to (a)?) — NO.

Three strictly non-vacuous gaps separate "same type" from "the lock fires":

**Gap 1 — type II_1 is NOT a complete isomorphism invariant.** The type is complete only for type I and for the *hyperfinite* II_1 factor R (Murray-von Neumann) and hyperfinite III_lambda (Connes/Haagerup). For general II_1 there are **uncountably many non-isomorphic** type II_1 factors (Connes 1976 free-group factors L(F_n); McDuff's continuum; property-(T) factors). So "both II_1" does NOT imply *-isomorphic. *(machine-checked logic; standard classification.)*

**Gap 2 — even *-isomorphism is weaker than what the lock needs.** The lock needs a STATE-LEVEL iso: a *-iso phi: M_DSSYK -> M_dS that maps the chord cyclic-separating vector to the GH cyclic-separating vector, i.e. **intertwines the modular flows** sigma^dS_t o phi = phi o sigma^DSSYK_t. By Tomita-Takesaki the modular flow is unique per (algebra, vector), so the lock fires only if the iso is implemented by a unitary carrying GH-vacuum -> chord-vacuum. This is STRICTLY stronger than abstract *-isomorphism.

**Logical ladder (each arrow is a real gap):**
`same type ==>/ *-isomorphic ==>/ state-level (modular-intertwining) iso ==> LOCK fires`

**Gap 3 — what the literature actually proves.** No published paper constructs phi at the state level. The strongest center-camp result (Marini-Qi-Verlinde 2604.21014, abstract-verified this run) establishes DSSYK<->dS via **Israel junction conditions + action equivalence + Gibbons-Hawking entropy match + boundary Green-function = (DSSYK 2-pt)^2** — i.e. CORRELATOR / ENTROPY / ACTION matching AT AN ASSUMED placement, NOT an algebra iso theorem. agentR's 60-paper sweep concurs: the dictionary is a HOLOGRAPHIC-DICTIONARY CHOICE, contested-terminal, with the chord algebra admitting BOTH center and edge GNS sectors. 2403.05980 etc.: no state-level iso anywhere.

---

## VERDICT: DICTIONARY STATUS = (b) TYPE-COMPATIBLE BUT UNPROVEN

- (c) TYPE-OBSTRUCTED: **RULED OUT.** Both algebras are type II_1; no type obstruction.
- (a) PROVEN: **NO.** No published state-level *-isomorphism; correspondence is correlator/entropy-matching at an assumed placement (Marini-Qi-Verlinde 2604.21014; agentR sweep). Hyperfiniteness/factoriality not even uniformly matched.
- (b) TYPE-COMPATIBLE BUT UNPROVEN: **YES — this is the honest status.**

**Consequence for the lock.** The lock is **CONDITIONAL, NOT FIRED.**
- The TYPE-matching removes the worst-case kill (no obstruction) — a genuine, modest advance: the dictionary is at least *not forbidden* by von Neumann type.
- But type-compatibility is NECESSARY, not SUFFICIENT. Establishing the state-level *-isomorphism (the modular-intertwining unitary GH-vacuum<->chord-vacuum) is exactly the OPEN, genuinely-new-physics step. It is NOT a calculation on banked machinery; it requires proving (i) the two II_1 factors are actually isomorphic (beyond type), AND (ii) the iso carries one cyclic-separating vector to the other.
- THEREFORE: IF that state-level iso is established, TT-uniqueness fires the lock and forces BOTH gaps (SS gain shape + TT center placement). The forcing is **CONDITIONAL-ON-DICTIONARY**. The dictionary itself is the open assumption the whole lock rests on — precisely as agentTT ('the selector presupposes DSSYK<->dS') and agentR (contested-terminal) flagged.

**One-line honest status:** *DSSYK<->dS is TYPE-COMPATIBLE (both type II_1, obstruction ruled out) but the state-level *-isomorphism is UNPROVEN in the literature and is the named open new-physics step; the lock fires only CONDITIONALLY on it, so it forces both gaps ONLY IF the dictionary is closed at the state level — which it is not.*

## QUARANTINE
Only computed: von Neumann type labels (II_1 both sides), the isomorphism-invariant-completeness logic, the modular-intertwining requirement. q=1/4, Z, a0, coefficient NEVER asserted. No Z claims.

## FILES
`agentUU_routeDict.md` (this) · `/tmp/uu_typematch.py` (type-match sufficiency ladder).
Primary sources fetched: arXiv 2206.10780 (CLPW, dS II_1), 2511.01978 (Cao-Gao, DSSYK II_1), 2605.13956 (Aguilar-Gutierrez, DSSYK II_1/I_inf), 2604.21014 (Marini-Qi-Verlinde, correspondence = correlator/entropy matching, not iso).
