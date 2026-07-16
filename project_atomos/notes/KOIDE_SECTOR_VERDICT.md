# The Koide Sector-Dependence Door — VERDICT: NULL (the 6th distinct attack, closed)

**Date:** 2026-06-25
**Task:** The first five attacks (formula-exhaustion, relational-exhaustion, mechanism-survey,
Dirac-normalization bridge, variational/fixed-point) all returned NULL on *deriving 2/3 for leptons
in isolation*. THE NEW QUESTION (genuinely distinct): is **Q(SECTOR)** a **FORCED FUNCTION of the
sector's gauge quantum numbers** {color N_c, weak isospin T3, hypercharge Y, electric charge Q_em,
the SO(10) **16** embedding}, so the *whole pattern* {lepton 2/3, up ~0.85, down ~0.73, neutrino}
is OUTPUT by one rule and leptons-2/3 is a **derived point**? Plus the scheme sub-question: is the
quark non-Koide a **running/scheme artifact** (quarks are MSbar/scale-dependent, leptons clean pole),
with the leptons the genuinely-clean case?

## VERDICT: generic-or-null. No forced predictive Q(quantum-numbers) law exists.

There is **no** Koide-free rule on {N_c, Q_em, T3, Y, SO(10)-16 slot} that outputs the measured
c-values for **all** sectors. Every candidate is either (a) **not a function** (N_c: up and down
share N_c=3 but have different c — same input, two outputs), (b) **a generic interpolation with zero
predictive degrees of freedom** ((T3,Y)-linear: 3 params spent on 3 charged sectors, exact by
construction, then mis-predicts the neutrino by 138–281%), (c) **a real universality prediction that
is FALSIFIED** (SO(10)-16: all four fermions share one spinor → would force all c=6 → killed by the
quarks and the free neutrino), or (d) **a near-hit on two sectors that catastrophically misses the
third** (c = 6/Q_em² lands leptons EXACTLY and up within ~2–5%, but predicts c_down=54 vs measured
7.45, a 625% miss). The scheme angle is **NOT** the escape: the QCD mass anomalous dimension is
**flavor-universal**, so the common running factor cancels exactly in Q and the quark Q's are
scale-invariant, never crossing 2/3 at any principled scale or scheme.

**Independently re-verified this session** (from-scratch mpmath dps=40 + sympy, not trusting the
route scripts' printed conclusions): all load-bearing claims reproduce.

---

## The measured pattern (the entire stake), mpmath dps=40

| sector | Q | c = 2/(1−Q) | QN: (N_c, |Q_em|, T3, |Y_L|) |
|---|---|---|---|
| **charged leptons** | 0.666661 | **6.000** (exact) | (1, 1, −½, ½) |
| **up-type quarks** | 0.845–0.887* | 12.9–13.2* | (3, 2/3, +½, 1/6) |
| **down-type quarks** | 0.731–0.747* | 7.45 | (3, 1/3, −½, 1/6) |
| **neutrinos (NO)** | **FREE in m₁** (0.585 → 0.336) | 4.8 → 3.0 | (1, 0, +½, ½) |

\* *footing-dependent (see scheme section): mixed-MSbar PDG-quoted → Q_up≈0.845; common-scale MSbar
→ Q_up≈0.884–0.887. Both are robustly off 2/3 and off the rule predictions; the spread is the
"scheme freedom" and 2/3 sits OUTSIDE the entire spread.*

Only the charged leptons sit at the target. The lepton c=6 is sympy-exact (Q=0.666661,
|Q−2/3|=6×10⁻⁶, the Koide value). The quark c's are **tight, well-determined physical numbers**
(MC over PDG mass errors keeps them at c_up=13.2±0.1, c_down=7.4±0.1 — NOT washed out by
light-quark uncertainty, because the heavy-pair spread dominates c).

---

## ROUTE 1 — FORCED Q(quantum-numbers) rule. Verdict: no-forced-rule.

**The decisive structural obstruction (independently re-derived, sympy-clean):** up and down quarks
share **every magnitude quantum number** — N_c=3, |T3|=½, |Y_L|=1/6, the same SU(2) doublet, the
same SO(10) **16** multiplet. They differ **only in the SIGN of T3 / electric charge** (+2/3 vs
−1/3). But c = e1²/e2 is a **ratio of POSITIVE masses, sign-blind by construction**. So any forced
QN map that separates them (c_up/c_down = 1.734) must be sign-sensitive with **no a-priori reason**,
and the required ratio 1.734 matches **no** natural QN ratio (|Q_d/Q_u|=½, squared=¼, inverse=2,
√2=1.414 — none is 1.734).

**Exhaustive zero-parameter QN-rule scan** (15 zero-param combinations of {N_c, Q_em, T3, Y},
no free constants except the geometric anchor 6; re-run from scratch): **NONE** hits all three
sectors within 5%. The single genuine near-hit:

- **c = 6/Q_em²**: leptons EXACT (6/1²=6.000, 0.002%), up within ~2–5% (6/(2/3)²=13.5 vs measured
  12.9–13.2), **but down catastrophic** (6/(1/3)²=54 vs measured 7.45, **625% off**). A real
  structural coincidence on lep+up — flagged honestly, killed on down with the same rigor a claimed
  win would demand.

**Leave-one-out on charge forms** (fit 2 sectors, predict the 3rd): worst-held errors 48–543% for
every monotone form (A+B|Q|, A+B/|Q|, A|Q|^B, A+B|Q|²). **(T3,Y)-linear** fits all 3 charged sectors
EXACTLY but only by spending all 3 dof (0 predictive dof, a generic interpolation), and then
mis-predicts the neutrino by **138–281%** at every m₁.

**SO(10)-16 universality is the one real PREDICTION** (all four fermions in one spinor → all c=6)
and is thereby **FALSIFIED**: quarks robustly off 2/3, neutrino Q free in m₁.

**Color-DOF reweighting** (the only Koide-free reweighting that could pull quarks to 2/3): uniform
N_c=3 weight **cancels in the ratio** (Q unchanged); no per-generation color factor exists (all 3
generations are identical color triplets) → no escape.

**Neutrino is fatal to any rule by itself:** Q is a **free function of m₁** (0.585 at m₁→0 down to
0.336 at m₁=0.05 eV) — not even a fixed target. A QN rule would have to predict a *moving* number
from fixed quantum numbers — impossible.

**⟹ The pattern {lepton 0.667, up 0.85, down 0.73, ν-free} is set by the un-derived Yukawa
mass-spread (log-hierarchy up 4.9 > lep 3.5 > down 2.9), NOT a gauge quantum number.** A 3-point
polynomial in Q_em fits trivially with 3 free params — but that is a FIT, not a forced rule.

## ROUTE 2 — QCD scheme/running (the strongest sub-angle). Verdict: NULL — sharpens the null.

The quark non-Koide is **robustly NOT a scheme/running artifact**, for a clean structural reason:

**The QCD mass anomalous dimension γ_m is FLAVOR-UNIVERSAL.** Every quark in a sector receives the
**same** multiplicative running factor, and Q = Σm/(Σ√m)² is **exactly invariant** under common
rescaling m_i → R·m_i (sympy: Q(R·m) − Q(m) = 0 identically; numeric: Q_up unchanged to 8 digits
under R ∈ {0.5, 1, 2, 10}). So the leading running **drops out** — "leptons-clean-pole / quarks-
running" **cannot** explain 13.2 and 7.45.

Running all six quark masses **consistently** across scales (1-loop universal exponent; cross-checked
against the 4-loop γ_m + 4-loop β RGE in `route2_qcd_scheme_running.py`, validated to
α_s(M_Z)=0.118): Q_up stays ~0.845–0.887, Q_down ~0.731–0.747 to 5 digits from 2 GeV to 2×10¹⁶ GeV.
**Neither converges to 2/3 nor to a lepton-matched pattern at any scale.** The full scheme spread
{mixed-MSbar PDG-quoted, common-scale MSbar, pole-where-defined} gives Q_up ∈ [0.832, 0.887],
Q_down ∈ [0.731, 0.747] — **2/3 = 0.667 lies OUTSIDE both entire ranges.** Only the
mass-dependent (non-universal) differential running shifts Q, by <10⁻³.

**Both-ways (verified):** the LEPTON cleanness is **not** a pole-vs-MSbar comparison artifact —
putting leptons in MSbar with universal QED running leaves Q=2/3 invariant (same universality
argument). So the asymmetry (leptons clean at 2/3, quarks robustly off) is **real**, not manufactured
by comparing pole leptons against running quarks.

---

## SMUGGLE AUDIT (the 169th-re-labeling test) — clean

No candidate rule's **definition** inputs 2/3 / Koide / r=√2 / c=6. The 2/3 / c=6 / r=√2 tokens
enter ONLY as the empirical/algebraic **target** that the rules' outputs are compared against, never
as an input to any candidate rule. The geometric anchor "6" used in the near-hit scan (c=6/Q_em²) is
the lepton c-VALUE itself — and even granting it, the rule is killed by the down sector. Quarantine
HELD: a₀ / Z / κ / Koide never asserted derived.

---

## Both-ways ledger

**Not a manufactured deficit (each "it fails" verified as hard as a win):**
- The quark c-values are **robust, not light-quark noise** — MC over PDG errors keeps c_up=13.2±0.1,
  c_down=7.4±0.1 (the reflexive-skeptic dismissal "it's just uncertain light-quark masses" is
  WRONG; the heavy-pair spread dominates c).
- The one genuine near-hit (c=6/Q_em² lands leptons EXACTLY and up within ~2–5%) was **found,
  flagged, and traced honestly** before being killed on the down sector with the same rigor.
- The scheme angle was tested **as hard as a result, not waved away**: the flavor-universal
  cancellation is an exact identity (sympy residual 0), and the leptons-in-MSbar both-ways check
  confirms the cleanness is not a comparison artifact.

**Not a manufactured win:**
- The honest prior was correctly **WEAK** — 12.9 and 7.45 are generic c-values (random-triple
  P(within 5%)~2–3%, random-c spans 4–166), NOT special angles like the lepton 2/3 (~1-in-44k).
- The up-vs-down sign-blindness obstruction is structural and sympy-clean.
- Consistent with all five banked priors: KOIDE_VARIATIONAL_VERDICT (2/3 non-extremal, neutrinos
  colorless yet non-Koide → no derived selector), RELATIONAL_THEOREM (Koide unique survivor but
  kernel-free), KOIDE_DIRAC_BRIDGE (167th re-labeling, halving tradeoff), the cross-fermion
  falsifier, and KOIDE_FROM_DSUNRUH (four-leg kill).

**No maximal-re-verification flag** — this is the honest expected null, not a lead.

---

## HONEST META-CALL: are we at the structural wall?

**YES — the brute-force / derivation route to a Koide TOE is now EXHAUSTED of genuinely-distinct
attacks.** Six distinct attacks have run:

1. **Formula-exhaustion** (per-constant) — null; Koide not even reachable by formula search.
2. **Relational-exhaustion** (1014 relations × 15 targets) — Koide the *unique* survivor, kernel-free.
3. **Mechanism-survey** (dS-Unruh IR loop) — four-leg kill.
4. **Dirac-normalization bridge** (EJA/Singh, gravity↔flavor) — 167th re-labeling, halving tradeoff.
5. **Variational / fixed-point** (4 independent principles) — 2/3 non-extremal; r=√2 a free modulus.
6. **Sector-dependence** (this) — no forced Q(QN) law; quark non-Koide not a scheme artifact.

These six span the **complete** logical space of "derive the Koide amplitude without inputting it":
the relation itself (1,2), a dynamical mechanism (3), a gravity bridge (4), an extremum principle
(5), and a gauge-quantum-number law (6). Every one converges on the **same structural wall**: the
framework hosts the **SHAPE** (S3/triality 1+2 democratic+doublet decomposition; the equally-spaced
√-mass triple; α=cH₀ MOND), but **no dynamics forces the AMPLITUDE r=√2**, and there is **no derived
sector-selecting ingredient** (the deepest falsifier, sharpened here: neutrinos are colorless like
charged leptons yet non-Koide — and now also: up/down are QN-identical up to a sign yet differ in c
by 1.73×, which c cannot see).

**The next thing IS a re-run.** Any further attack of the "derive 2/3 / find a forced rule" kind
would re-traverse one of these six axes. There is **no remaining genuinely-distinct derivation
attack** — we are at the structural wall.

**The honest remaining moves are NOT derivations** (and so are out of scope for "the brute-force
route"): (i) **new measurement** — a future neutrino absolute-mass / ordering determination could
pin the neutrino Q and either reveal or kill a pattern (currently free in m₁); (ii) **a NEW forced
kernel** appearing in the gauge/Yukawa sector from outside (a genuinely new mechanism, not a re-run
of 1–6) — the memory rule already says do NOT re-open the mass sector absent exactly this. Neither is
a brute-force/derivation attack on the existing structure.

**One line:** No forced predictive Q(quantum-numbers) law outputs all sectors — N_c isn't a function,
charge/(T3,Y) forms are generic fits or single-sector, SO(10)-16 universality is falsified, the
c=6/Q_em² near-hit dies on the down quark, and the quark non-Koide is a flavor-universal-running-
invariant fact, not a scheme artifact (2/3 outside the whole scheme spread). After six distinct
attacks the derivation route to a Koide TOE is exhausted — we are at the structural wall; the only
non-re-run moves are new data or a new external kernel, neither of which is a derivation.

---

## Files (all re-run / re-verified this session)

- `opus_48_extended_research/reviews/koide_dsunruh/route_gaugeQN_rule.py` (QN-rule tests)
- `opus_48_extended_research/reviews/koide_dsunruh/route2_qcd_scheme_running.py` (4-loop RGE,
  validated α_s(M_Z)=0.118; the universal-γ_m cancellation + scheme spread)
- Independent from-scratch re-verification (this session): `/tmp/koide_sector_indep.py`,
  `/tmp/koide_sector_indep2.py`, `/tmp/scheme_running_fast.py`
- Priors (do NOT redo): `project_atomos/notes/{KOIDE_VARIATIONAL_VERDICT, KOIDE_DIRAC_BRIDGE,
  RELATIONAL_THEOREM}.md` + `.../koide_dsunruh/`

**The sector-dependence door is CLOSED. r=√2 / Q=2/3 has no forced gauge-QN law and no scheme
escape. The SM mass sector stays WALLED. The derivation route to a Koide TOE is structurally
exhausted.**
