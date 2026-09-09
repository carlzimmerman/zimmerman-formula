# L39 — retarded-nonlocal gravity has TWO modes, and L31's locality hypothesis can still be dropped

2026-09-08. Lane L39 of [CHARTER.md](CHARTER.md), answering the single open computation named by
[L31_FOLIATION_NOGO.md](L31_FOLIATION_NOGO.md).
Script: [L39_nonlocal_modes.py](L39_nonlocal_modes.py) → [L39_nonlocal_modes.out](L39_nonlocal_modes.out).
**40 checks, 40 PASS / 0 FAIL.**

Method: nothing under `closure_2026/` or the lead's directories was imported, executed or copied. All
algebra — Christoffels → Ricci → quadratic actions, transverse-operator bases, conformal null geodesics —
was built from scratch in sympy in this file. Six controls guard it, including three that reproduce
published Dirac counts and one that reproduces the textbook conformal-factor problem from the metric.
Six papers were read in full (PDF text, not abstracts); every quotation below is verbatim.

---

## The verdict, first

**The mode count is 2. And it does not matter — the lensing decides, and it decides for L31.**

> **N_grav = 2** for retarded-nonlocal gravity. The retarded reading is correct; the localised reading
> answers a different question and, applied consistently, would give ordinary general relativity a ghost.
>
> **L31's theorem survives without hypothesis (iv).** Not because the nonlocal challenger fails (iii) —
> it satisfies (i), (ii) and (iii) simultaneously — but because **it satisfies the conclusion**: the
> Deffayet–Esposito-Farèse–Woodard model carries a unit timelike vector field `u^μ[g]`, its authors say
> so in print, and `u` is a normalised gradient, so it is hypersurface-orthogonal and L31's *corollary*
> (a preferred foliation) holds too.
>
> **And the reason is now a mechanism, not an enumeration.** The **lensing lock** proved here never uses
> locality.

This is verdict **(a)** on the mode count and verdict **(a)-with-a-named-gap** on the theorem: hypothesis
(iv) is removable against the entire known nonlocal class, by an argument rather than by case-checking,
with one precisely named residual computation (§7).

---

## 1. Controls

| control | result |
|---|---|
| C1 Dirac count for ADM general relativity | **2** = (12 − 2·4)/2 |
| C2 GR + one minimally coupled scalar | **3** = (14 − 8)/2 |
| C3 Einstein-aether | **5** = (18 − 8)/2, matches Jacobson–Mattingly |
| C4 L31's `±½` kinetic eigenvalues, re-derived independently | `K = [[0,½],[½,0]]`, eigenvalues `∓½`, **det K = −0.25** |
| C5 linearised GR's **conformal** mode vs its graviton | coefficient of `(∂_t·)²` is **+½ (TT)** vs **−6 (conformal)** |
| C6 the *published* localised DEFW MOND Lagrangian | **N = 6**, not 4 |

**C4.** Localising `S = (1/16πG)∫√−g R[1 + f(□⁻¹R)]` with `ξ = □⁻¹R` enforced by a multiplier `ψ` gives
the cross-term `−√−g g^{μν}∂_μψ∂_νξ`. Reading the kinetic matrix off by differentiation reproduces L31's
`±½` exactly. Sharpening L31: **the magnitude ½ is a normalisation convention; the
convention-independent statement is `det K < 0`**, i.e. exactly one negative kinetic eigenvalue.

**C5 is the control that decides the whole lane.** Apply the inference "a negative kinetic eigenvalue
means a propagating ghost" to ordinary linearised general relativity. Computing `√−g R` to second order
from the metric and reducing modulo total derivatives:

    TT mode         h_11 = −h_22 = χ(t,z)   :   coefficient of (∂_t χ)² = +1/2
    conformal mode  g_μν = (1+2φ(t)) η_μν   :   coefficient of (∂_t φ)² = −6

GR has exactly two degrees of freedom and no ghost. The conformal mode is removed by the Hamiltonian
constraint, not by a sign. **So `±½` does not by itself establish a ghost mode**, and any counting rule
that reads one off a redefined kinetic matrix is unreliable *before* it is applied to a nonlocal theory.

**C6.** L31 estimated the localised count from the generic `∫R f(□⁻¹R)`. The model as actually published
(Tan & Woodard 2018, eq. 1) is bigger — **four** auxiliary scalars `φ, ξ, χ, ψ` in two off-diagonal
kinetic pairs:

    L = (c⁴/16πG)√−g { R + (a₀²/c⁴) f_y( g^{μν}∂_μφ∂_νφ / (c⁻⁴a₀²) )
                         − [ ∂_μξ ∂_νφ g^{μν} + 2ξ R_{μν}u^μu^ν ]
                         − [ ∂_μψ ∂_νχ g^{μν} − ψ ] }

so the localised reading gives **N = 6**, not 4. L31's "≥ 4" was a lower bound and is not contradicted.

---

## 2. The two readings, stated as Hamiltonian statements

**Localised reading.** Phase space per space point `Γ_loc = {γ_ij, π^ij; ξ, p_ξ; ψ, p_ψ; …}`, dimension
`12 + 2n_aux`, with the *same* four first-class constraints as GR — the auxiliaries add none, since they
appear with nondegenerate (if indefinite) kinetic terms. Dirac's algorithm terminates at
`N = 2 + n_aux`. Cauchy data for the auxiliaries is **free**.

**Retarded reading.** The theory is defined not by an action but by field equations in which
`ξ(x) = ∫G_ret(x;x′)R(x′)dx′` with **no** homogeneous piece, relative to an initial-value surface `S`. On
a slice at time `t` the pair `(ξ, ξ̇)` is a *functional of the past history of the metric*, not free data.
Free data = the graviton's 2.

The question is whether the restriction is legitimate. Four tests, each of which could have failed:

| test | result |
|---|---|
| **A2** is the retarded set preserved by the dynamics? | **YES.** Restarting the retarded solution from its own slice data at `t = 10` reproduces the remaining evolution with max relative difference **0.000e+00** — an invariant submanifold |
| **A3** is it a Dirac constraint? | **NO.** Two source histories identical for `t ≥ 8` and different before give `|R_A − R_B| = 0` on the slice at `t = 16` but `|ξ_A − ξ_B| = 1.02` |
| **A4** does it follow from a variational principle? | **NO.** The gradient kernel of `∫f □⁻¹f` sits at distance **0.50** from `G_ret` and **0.00** from `(G_ret+G_adv)/2` |
| **A5** does it break conservation? | **NO.** `∂_t T^t_t + ∂_x T^x_t + ψ ∂_t j = 0` on shell, symbolically, using only the differential equations |

**A3 is the structural heart of the disagreement.** The retarded condition is not a function on the
instantaneous phase space, because `ξ_ret(t)` depends on the past and the instantaneous slice data does
not. Dirac's algorithm is therefore *structurally blind* to it. The two readings are not two answers to
one question; they are answers to two questions.

**A5 answers the conservation half of the crux exactly as DEFW claim.** Their words (1106.4984 §IV):

> "The result is manifestly causal. It is also conserved … because we have just substituted, in the field
> equations, the causal retarded Green's function everywhere an acausal advanced Green's function
> appeared. Conservation requires only the differential equation, which both the advanced and retarded
> solutions obey."

Verified: the conservation identity uses only `□ξ = −j` and `□ψ = 0`, which the retarded particular
integral satisfies as much as any other solution. The homogeneous piece never enters.

**A4 answers the variational half, and it is a genuine cost.** Foffa–Maggiore–Mitsou §2, verbatim:

> "the variational of the action automatically symmetrizes the Green's function. It is therefore
> impossible to obtain in this way a retarded Green's function in the equations of motion"
> … "eq. (1.1) is not the classical equation of motion of a non-local quantum field theory."

DEFW say the same of their own model: *"This sort of acausality is inevitable for any nonlocal action
based on a single field"*, and of their partial-integration fix, *"Of course this is just a trick; a true
derivation from fundamental theory would require use of the Schwinger-Keldysh formalism."*

**A6.** Combining A2 and A4: the retarded theory is **not a different theory**. It is the localised
theory restricted to the invariant submanifold `ξ = ξ̇ = ψ = ψ̇ = 0` on `S`. The codimension is `2n_aux`
functions — exactly the gap between the two counts.

---

## 3. The mode count: 2

**N_grav = 2, and the retarded reading is the correct one for a theory whose *definition* is the nonlocal
field equation.** Three reasons, none of them a preference:

1. **The localised rule overcounts even GR** (C5, computed here; Foffa–Maggiore–Mitsou §3.1 reach the
   same conclusion from unitarity: *"If one treats them as propagating degrees of freedom … one reaches
   the (wrong) conclusion that in GR the vacuum is unstable."*)
2. **The restriction is legitimate**: preserved by the dynamics (A2), conservation-safe (A5), locally
   covariant (A5b).
3. **It is invisible to Dirac's algorithm** (A3), so the localised 4 — really 6 — is not a rival answer.

Independent corroboration from the model itself, Soussa & Woodard 2003 abstract, verbatim:
*"Although nonlocal, these equations do not seem to possess extra graviton solutions in weak field
perturbation theory."*

**The price, which must always be quoted with the count.** The prescription does not follow from a
variational principle (A4); the theory cannot be quantised as written; and it requires a preferred
initial surface. Foffa–Maggiore–Mitsou, verbatim:

> "at the quantum level, there are no creation and annihilation operators associated to `s`"
> "there is no sense, and no domain of validity, in which the Lagrangian (1.5) can be used to define a QFT
> associated to our theory"
> "such equations cannot be fundamental. Rather, they are effective classical equations."

So **the ghost is genuinely absent from the physical spectrum — because there is no spectrum.** The
theory is a classical effective description whose UV completion is, in its own authors' reading, a
**local** one (the Schwinger–Keldysh effective action of quantum gravity). L31's hypothesis (iv) then
binds the underlying theory rather than the effective one. That is an argument from the literature, not a
theorem, and it is labelled as one.

---

## 4. THE LENSING LOCK — the new result, and it never uses locality

This is where the lane turns. **The mode count is not what decides L31. The lensing is.**

**Controls first** (C-a), all computed from the metric here and checked against Deffayet–Woodard 2026
eqs. (21)–(22) for `ds² = −(1+2Ψ)dt² + (1+2Φ)δ_ij dx^i dx^j`:

    R_00^(1) = ∇²Ψ            G_00^(1) = −2∇²Φ                    [DW eq. 21] ✓
    R^(1)    = −2∇²Ψ − 4∇²Φ    G_ij^(1) = (δ_ij∇² − ∂_i∂_j)(Ψ+Φ)  [DW eq. 22] ✓

The `ij` equations enforce `Ψ + Φ = 0` — no slip — and **that is what supplies MOND's lensing**
(DW 2026 §3.2: *"The spatial equations imply Φ = −Ψ, which is consistent with weak lensing provided that
Ψ obeys (20)"*, their Tully-Fisher equation).

**The operator lemma (proved here, C-b).** Let `𝒮[g]` be any generally covariant scalar functional of the
metric alone — local or nonlocal, any order in derivatives, inverse d'Alembertians allowed — whose
expansion about flat space begins at first order in `h_μν`. Diffeomorphism invariance of the action forces
`𝒮^(1) = ∫O^{μν}h_μν` with `∂_μO^{μν} = 0`. Counting transverse symmetric operators in Fourier space by
an actual linear solve:

| available background structures | transverse solutions |
|---|---|
| `{η^{μν}, k^μk^ν}` — **no preferred vector** | **1-parameter family**: `O^{μν} = B(□)(∂^μ∂^ν − η^{μν}□)` |
| `{η^{μν}, k^μk^ν, ū^μū^ν, ū^{(μ}k^{ν)}}` — **one unit timelike `ū`** | **2-parameter family** |

So without a preferred vector **every** such scalar is a function of `□` acting on `R^(1)`. `□⁻¹` is such
a function. **Nonlocality buys nothing.**

**The lock (C-c1).** `R^(1) ∝ ∇²(Ψ + 2Φ)`, with *both* coefficients nonzero. Therefore for any
Lagrangian addition `ΔS` built as an arbitrary function of such scalar blocks,

    (δΔS/δΨ) : (δΔS/δΦ)   is LOCKED at   1 : 2 ,

so `ΔS` **cannot modify the 00 (Tully-Fisher) equation while leaving the `ij` equations undisturbed**.
Adjoining a unit timelike `u` supplies the missing independent combination `R_μν u^μu^ν → ∇²Ψ` — the
Newtonian potential, separated from the lensing potential. That is precisely, and only, what the extra
transverse structure buys.

**A second, independent proof for the case the literature actually hit (C-c2).** A modification acting on
the metric only through a conformal factor cannot bend light at all: verified symbolically from the
Christoffels of `Ω²g` that `Γ̃^a_{bc}k^bk^c − Γ^a_{bc}k^bk^c − 2k^a(k·∂lnΩ) = 0` for null `k`, i.e. null
geodesics are conformally invariant up to reparametrisation.

**And the literature record matches the lock line for line.**

- **Soussa & Woodard 2003** (the *frame-free* nonlocal metric MOND model), abstract, verbatim:
  *"We compute the angular deflection of light in the weak field regime and demonstrate that it is the
  same as for general relativity, resulting in far too little lensing if no dark matter is present."*
  and *"An interesting feature of our equations is that they become conformally invariant in the MOND
  limit."* — exactly the C-c2 mechanism.
- **DEFW 2011** (the model L31 named as the challenger): *"One major problem has always been
  simultaneously reproducing the Tully-Fisher relation and giving a sufficient amount of weak lensing.
  That problem was finally surmounted in 2004 by … TeVeS … where the presence of a unit timelike vector
  field helps in obtaining the right amount of light deflection."* Their own fix:
  *"the gradient of the invariant volume of the past light-cone allows us to define a timelike 4-vector
  with which we can select particular components of the curvature … The second property is needed to get
  the right weak fields."*

      u^μ[g](x) ≡ − g^{μν}∂_ν V[g](x) / √( −g^{αβ}∂_αV ∂_βV )

  *"It can therefore be used to pick out the timelike components of a tensor, just like the fundamental
  vector field U_μ of TeVeS."* And, decisively:
  **"Although the timelike vector field u^μ[g](x) will certainly introduce PREFERRED FRAME EFFECTS…"**
- **Deffayet & Woodard 2026** (arXiv:2512.10513v2, 30 Apr 2026 — the current state of the art):
  `u_μ = ∂_μφ[g]` with `g^{μν}∂_μφ∂_νφ = −1` and `φ(0,x) = 0` at the end of inflation. Their own label
  for it: *"the Lagrangian for 'mimetic gravity'."*

**Frame or foliation? (C-e).** Both `u ∝ ∇V` and `u = ∇φ` are normalised gradients. Checked directly:
`u_{[α}∂_βu_{γ]} = 0` for all 64 index triples. By Frobenius `u` is hypersurface-orthogonal, so the
nonlocal challenger realises **L31's corollary — a preferred foliation — not merely its theorem.**

---

## 5. L31's hypotheses on the actual nonlocal theories

| theory | (i) MOND **+ lensing** | (ii) one metric | (iii) N = 2 | preferred timelike structure | N_grav |
|---|---|---|---|---|---|
| Soussa–Woodard 2003, `f(□⁻¹R)` — **frame-free** | **NO** (GR-level deflection) | yes | yes | **NONE** | 2 (no extra graviton solutions) |
| DEFW 2011 nonlocal MOND | yes | yes | yes | **YES** `u^μ = −∇V/‖∇V‖` | 2 retarded / 6 localised |
| Kim et al. 2016, cosmological branch | yes | yes | yes | **YES** same `u^μ` | 2 retarded / 6 localised |
| Deffayet–Woodard 2026 mimetic-nonlocal | yes | yes | yes | **YES** `u_μ = ∂_μφ`, `(∂φ)² = −1` | 2 retarded / 3 localised |
| RAQUAL/AQUAL *(control)* | **NO** | yes | no | NONE | 3 |
| TeVeS *(control)* | yes | yes | no | **YES** unit timelike `A^μ` | ≥4 |
| GEA / AeST *(control)* | yes | yes | no | **YES** unit timelike aether | ≥5 |
| general relativity *(control)* | NO | yes | yes | NONE | 2 |

**No row has (i) + (ii) + (iii) with no preferred structure.** The pattern is not L31's original
exclusive-OR — DEFW genuinely has all three — it is sharper: **every frame-free MOND theory, local or
nonlocal, fails on lensing.** The lock explains all of it, including the 1984→2004 history that forced
Bekenstein to a unit timelike vector in the first place.

---

## 6. Viability of the challenger, recorded plainly

Not part of the theorem, but it belongs on the record.

- **Kim et al. 2016** tuned the free function to the ΛCDM expansion history and got `H₀` about 4.5%
  larger — a serendipitous fit, not a failure.
- **Tan & Woodard 2018**, abstract: *"it becomes obvious (in this model) that the MOND enhancement is not
  sufficient to allow ordinary matter to drive structure formation"*; conclusions: **"Hence this
  particular model is falsified."**
- **Deffayet & Woodard 2026** restore cosmology by adding a pressureless perfect fluid `T_μν = ρu_μu_ν` as
  a nonlocal functional of the metric — their own words: *"the model defined by (5) and (9) is just dark
  matter, expressed as a nonlocal functional of the metric."*

**Both footings, on the 2026 model's own numbers.** It fixes its dust normalisation by
`ρ₀ = 45a₀²/16πG`, asserting the coincidence `ρ₀ = 3c²H₀²/32πG`:

| footing | `45a₀²/16πG` | `3c²H₀²/32πG` | ratio | coefficient needed |
|---|---|---|---|---|
| canonical (9.3619e-11) | 1.1757e-10 | 1.9173e-10 | **0.613** | 73.4 |
| alt (1.1279e-10) | 1.7065e-10 | 1.9173e-10 | **0.890** | 50.6 |

The coincidence is exact only at `a₀ = cH₀/√30 = 1.1955e-10 m s⁻²` (= 1.277 canonical, 1.060 alt). **The
"45" is a fitted coefficient, and it is footing-dependent at the tens-of-percent level.**

DEFW's own scales, both footings: `c/a₀ = 3.20e18 s = 6.99/H₀` (canonical) and `2.66e18 s = 5.81/H₀`
(alt) — their guessed instability time scale. Their preferred-frame estimate is `(v_pec/c)² ≈ 1e-6` at
`v_pec = 300 km/s`, offered as a belief. **No `α₁, α₂, α₃` has ever been computed for this class.**

---

## 7. What is still not proved — named precisely

1. **The lensing lock is proved for covariant scalars whose expansion begins at FIRST order in `h_μν`.**
   Scalars beginning at second order — Kretschmann, `R_μνR^μν`, `C²` — do separate `Ψ` from `Φ` and are
   not covered. They are, however, exactly the objects L31's STEP E showed to be uniform-field-blind and
   dominated by the nearest star (`G_loc/|∇Φ| = 11.0` at `r = 0.2b` for a Plummer sphere; 99.0% of the
   solar neighbourhood inside `d_eq = 2.23 pc`).
   **THE MISSING COMPUTATION:** *is there a nonlocal scalar, quadratic or higher in curvature, that both
   separates the Newtonian from the lensing potential AND remains sensitive to the coherent
   coarse-grained field rather than to the nearest star?* If no, hypothesis (iv) is removable outright and
   L31 becomes a theorem in (i)–(iii). If yes, that object is a live candidate for a frame-free MOND
   theory and should be built. **This is the successor to L31's item 1, and it is a strictly smaller
   target.**
2. **No PPN computation exists for the DEFW class.** DC-019 puts `α₃ = O(1)` for preferred-frame MOND
   against `|α₃| < 4e-20`. If DC-019's mechanism applies to a `u` built *nonlocally* from the metric, the
   nonlocal class is excluded by ~2.5e19× on the same grounds as every other preferred-frame MOND theory.
   That is a computation, not a claim, and it is **not made here**.
3. **The claim that the retarded theory's UV completion is local** is the authors' reading
   (Schwinger–Keldysh), and it is the reason L31 (iv) would bind the underlying theory. Argument from the
   literature, not a theorem.
4. **Not claimed:** that the lensing lock is original. That a conformally-coupled scalar cannot lens is
   Bekenstein–Sanders folklore; what is new here is the operator-counting form (1 transverse structure
   without `ū`, 2 with), which covers the *nonlocal* case in one stroke and therefore removes L31's
   hypothesis (iv) rather than merely re-deriving the local result.

---

## 8. What this changes in the programme's standing record

- **L31's escape route is closed against everything that exists.** The nonlocal door was the last one
  L31 left ajar. It is now shut against the whole known class, and by a mechanism.
- **L31's `±½` ghost claim should be retired as an argument.** It is arithmetically right and
  inferentially wrong — C5 shows the same inference gives GR a ghost. L31's own text already declined to
  bank it; this lane supplies the reason.
- **DEFW should be re-labelled in L31's control table.** It is not "contested (iii)" — it *satisfies*
  (iii) with N = 2 and it *has* a preferred foliation. The row was in the wrong column, and correcting it
  strengthens the table rather than weakening it.
- **The single-metric pincer's exhaustiveness now has a second, independent backing.** L31 supplied the
  kinematic reason (hyperbolic vs degenerate principal symbol) *under locality*. L39 supplies a reason
  that does not need locality at all: the 00/`ij` lock. The two agree, and they agree with 42 years of
  relativistic MOND model-building — TeVeS's `A^μ`, GEA/AeST's aether, DEFW's `u^μ[g]`, and the 2026
  mimetic `∂_μφ` are the same object, forced by the same requirement, wearing four different hats.
- **Nothing in the lead's IC-series is contradicted.** The IC8–IC10 outcome — metric sector exactly
  Einstein, `N_grav = 2`, one separately counted healthy clock — remains what the theorem predicts, and
  the theorem is now stronger by one hypothesis.
