# agentM — Milgrom 2022 (arXiv:2208.07073) through the kill battery: the last published modified-inertia object, confronted

*agentM, 2026-06-10. Files: `agentM_milgrom2022_gauntlet.py` → `.out` (all numbers below machine-generated there;
gates against banked agentA/agentE/SPARC values pass inside the run). Paper source fetched from arXiv
(`arxiv.org/e-print/2208.07073`, single-file LaTeX, 686 lines) — every quote below is verbatim from that source.
Battery inputs: `agentE_solar_reflex.out` (Door IVb budget), `agentA_f4_eccentric.out` (precession machinery + bounds),
`agentN5_freq_vs_accel.md` (the corridor), `mi_f4_sparc_shape_test.{py,out}` (locked SPARC conventions),
`mi_f4_widebinary_efe.out` (WB fork), `f4_lensing_wall.out` (40.5σ). Both a₀ footings + the hostile bath s=cH_Λ
throughout, per the working rule. Raw before comparison; no coefficient claims. No git.*

---

## 0. The EXACT construction (pinned from source)

**The law** (his Eq. labeled `law`): in Fourier space along a body's trajectory,
> m â(ω) 𝓘[{r̂}, ω, a₀] = F̂(ω)

with "the inertia functional, 𝓘[{r̂},ω,a₀], … a dimensionless functional **of the whole trajectory**", a₀ the only
new dimensioned constant. Deep-MOND limit forced by scale invariance: 𝓘 → 𝓐[{r̂},ω]/a₀ (his Eq. `limba`).

**The concrete class** (his Eq. `mumu`): 𝓘 = μ[𝓐(ω)/a₀] with μ the standard MOND interpolating function
(μ→1 high x, μ→x low x; xμ(x) monotonic required for uniqueness — same condition as AQUAL).

**The filter kernel — "the nonlocal acceleration"** (his Eq. `v`, called *heuristic* by him):
> 𝓐(ω) = (1/√2 π) ∫₀^∞ θ(ω′/ω) |â(ω′)| dω′

θ(y) symmetric, dimensionless — **the frequency filter**. For multi-frequency trajectories (his Eq. `shiluta`):
> 𝓐(ω_n) = ω_n²|r̄_n| + Σ_{k≠n} ω_k²|r̄_k| θ(ω_k/ω_n)

**The normalization that matters for everything below** (verbatim):
> "The normalization of θ(y) is degenerate with that of a₀. We pick the normalization such that **θ(1)=1** because
> then … the standard value of a₀ and the form of μ(x) that have been routinely used in rotation-curve analysis, apply."

**Free choices:** θ(y) (his named examples: 2/(1+y²), e^(1−y), e^((1−y)/q)) and μ(x). **Delivered:** WEP by
construction ("since for gravity F̂(ω) ∝ m, the theory obeys the universality of free fall"); nonlocal conserved
P, E, J; circular orbits reduce **exactly** to aμ(a/a₀) = a_N radius-by-radius (his Eq. `mdar`); the composite-body
(CoM) problem solved by the filter (his Eq. `shimasa`: Sun-in-Galaxy amplitude and frequency ratios both ~10¹², so any
θ falling faster than y¹ kills the internal term); an EFE enhanced to μ[θ(0)⟨a_ex⟩/a₀] with "θ(0) to be of the order
of a few". **Acknowledged open by the author:** causality/initial-conditions ("Perhaps the models can be modified to
incorporate such a requirement"), arbitrariness ("the construction of the models is somewhat arbitrary at present"),
mechanism ("inertia as an acquired attribute … interaction of the body with some ambient medium" — no dynamics given).

---

## 1. SOLAR REFLEX (the agentE killer) — **the filter is structurally INERT; power-law μ DIES, exponential μ survives**

**The structural point (new, and decisive):** θ only reweights *other* frequencies' contributions to 𝓐. The
own-frequency term enters with coefficient **θ(1) = 1 — the same normalization constant that anchors μ and a₀ to
rotation curves**. A quasi-monochromatic worldline therefore responds with μ evaluated at ≈ its own acceleration —
exactly the magnitude-keyed response agentE killed. The Sun's barycentric wobble (Ω_J = 1.68×10⁻⁸ s⁻¹,
a_J = GM_J/r_J² = 2.091×10⁻⁷ m/s², matching agentE's integrated mean to 0.1%) **is** quasi-monochromatic and is the
*largest* acceleration content of the Sun's CoM worldline — there is nothing on the worldline to dilute it. The full
inventory (8 planetary lines + the galactic line, machine-summed per Eq. `shiluta`):

| θ (his examples) | 𝓐(Ω_J) | 𝓐/a_J | δa☉ suppression (a_J/𝓐)² |
|---|---|---|---|
| 2/(1+y²) | 2.441×10⁻⁷ | 1.167 | 0.734 |
| e^(1−y) | 2.460×10⁻⁷ | 1.177 | 0.722 |
| e^((1−y)/2) | 2.363×10⁻⁷ | 1.130 | 0.783 |

**Required suppression to clear the agentE budget (δa☉ ≤ 2.47×10⁻¹⁵): ≤ 0.117 (framework) / ≤ 0.072 (canonical).
His kernel delivers 0.72–0.78 — short by ×6–11.** The verdict table (δa☉ = a_J·(1/μ(𝓐/a₀)−1), stable form):

| μ | footing | δa☉ [m/s²] | × over strict budget | verdict |
|---|---|---|---|---|
| standard | framework 9.36e-11 | 1.51–1.64×10⁻¹⁴ | 6.1–6.6 | **FAIL** |
| standard | canonical 1.2e-10 | 2.49–2.70×10⁻¹⁴ | 10.1–10.9 | **FAIL** |
| standard | hostile cH_Λ | 5.07–5.50×10⁻¹³ | 205–222 | **FAIL** |
| simple | framework / canonical | 8.0×10⁻¹¹ / 1.0×10⁻¹⁰ | 3.2×10⁴ / 4.2×10⁴ | **FAIL** |
| McGaugh-RAR (exp tail) | framework / canonical | 1.1–3.2×10⁻²⁹ / 4.5×10⁻²⁷–1.1×10⁻²⁶ | ~0 | **PASS** |
| McGaugh-RAR | hostile cH_Λ | 1.2–1.8×10⁻¹⁶ | 0.05–0.07 | **PASS** |

(ranges = across his three θ examples; the result is θ-insensitive, which is the point.)

**Hostile audit of the rescue routes** (a kill owes its own escape map):
- *Bigger cross-terms?* To reach 𝓐_req = 2.9–3.7×a_J the filter would need **θ(0) ≈ 1860–2660** (galactic line) or
  **θ(0.40) ≈ 21–31** (Saturn line). Either wrecks the model's own phenomenology: the EFE argument θ(0)·a_ex/a₀
  becomes ~4000–5800 → 1−μ ~ 10⁻⁸ → wide-binary/vertical-disk MOND boosts quenched to ~0.000% (observed-class effects
  are ~10–20%), and it contradicts his own "θ(0) of the order of a few." A θ-spike at y≈0.4 only would also impose
  ×20 enhanced EFE on every subsystem with ω_ex/ω_in ≈ 0.4 — his own dwarf-satellite regime ("we estimate
  ω_ex ∼ ω_in"). **Closed.**
- *The second acceleration measure* |â·â|^½ (ellipticity-keyed; vanishes on circular orbits): the Sun's wobble is
  near-circular (e_J = 0.048) — the same x₂≈0 corner as the galactic circular orbits that pin μ(x,0) via rotation
  curves. It cannot separate the two. **Closed.**
- *Beyond the heuristic 𝓐 entirely?* Milgrom's own general theorem (his citation of Ann. Phys. 229, 384: circular
  single-frequency trajectories force aμ(a/a₀)=a_N in ANY MI formulation) + positivity of his construction leaves
  only kernels that are *not* positive-weighted averages of the worldline's acceleration content. Within the published
  object: **the μ-tail is the only escape**, and it works: the exponential-tail (McGaugh-RAR) μ passes by >10¹³.
- *Budget transfer caveat:* the agentE survival line was derived on the instantaneous-μ time template; Milgrom-22's
  per-frequency-constant μ is agentE's **frozen-μ** template, which agentE ran: linearized post-fit Mars 269.8 m
  (frozen) vs 269.2 m (instantaneous) at hostile — the budget transfers within ~2% (and the frozen pre-fit signal is
  *larger*: Mars 5417 vs 2303 m). The ×6–11 margins are far outside this slack.

**This is major news in the N4 frame:** 2208.07073 was built to pass the composite-body test (suppress *high*-frequency
internal motion leaking into *low*-frequency dynamics — θ(y≫1) small, easy, and it works). The solar reflex is the
mirror channel — the own-frequency response of an intermediate-frequency, high-x line — and there **the θ(1)=1
normalization that makes rotation curves come out standard makes the reflex un-suppressible.** The N4 flag (the
Hees+ 1510.01369 exponential-μ selection transferring from modified gravity to the MI/solar-reflex channel) is hereby
**confirmed at the level of the actual published MI construction**: the solar system selects the exponential-tail μ
*inside Milgrom-22's own class*; the filter contributes nothing to the selection.

## 2. ECCENTRIC ORBITS / PRECESSION — **suppressed ×3.4–6.8 AND sign-flipped; the channel RELAXES, not just passes**

Machinery: per-harmonic first-order secular theory on the exact Kepler orbit (FFT → harmonic amplitudes in his
√2|C_k| convention → 𝓐(kn) per Eq. `shiluta` → constant per-harmonic c_k = 1/μ(𝓐_k/a₀)−1 → Gauss apsidal integral).
**Gates inside the run:** constant-c (pure GM-rescaling) gives Δϖ = −6.8×10⁻¹⁹ ≈ 0; the instantaneous arm reproduces
agentA's banked closed form −π(4+e²)√(1−e²)s_c²/2 to ratio 1.0000 at e = 0.206/0.093/0.057; s²-scaling = 100.00/100.

Result (μ_standard; the task's expectation "the filter should kill the signal" is **partly wrong, quantified**): the
per-harmonic-constant structure removes the time-domain μ(|a(t)|) modulation but leaves an O(1)-spread c_k ladder
across harmonics (𝓐_2/𝓐_1 ≈ θ(1/2) ≠ 1). Net: Δϖ(M22)/Δϖ(instantaneous) = **−0.148 to −0.300** (e- and θ-dependent)
— a ×3.4–6.8 suppression **with a sign flip to prograde**. Physical predictions:

- **Saturn, hostile s=cH_Λ:** +0.055 to +0.091 mas/cy → tension **+0.03 to +0.21σ** on the tightest bound
  (INPOP15a-C2, +0.05±0.20) — vs agentA's instantaneous −0.307 mas/cy at −1.79σ (the binding case). The filter turns
  agentA's only marginal cell into a comfortable pass.
- Framework/canonical a₀: Saturn +1.7–4.5×10⁻³ mas/cy, Mercury ≤ 2.6×10⁻⁵ mas/cy — orders below all bounds.
- McGaugh-RAR μ: c_k ~ e^(−√x) → precession ≈ 0 identically.

**Verdict: channel EMPTY for the class** (and *more* comfortable than instantaneous F4 was).

## 3. THE N5 CORRIDOR — **Milgrom-22 is the p = 0 EDGE: not the killed pure-frequency class, but not dressed either**

𝓐 is *acceleration-valued*; frequency enters only through dimensionless ratios ("Only ratios of frequencies enter,
and a₀ remains the only new dimensioned constant" — abstract). On single-frequency (circular) orbits the law reduces
**exactly** to aμ(a/a₀) = a_N (his Eq. `mdar`; verified mechanically through our FFT pipeline: 𝓐(n)/|a| = 1.000000008
for all three θ). In N5's parametrization a₀_eff = a₀·[(1+Ω/H₀)/(1+Ω_ref/H₀)]^(−p): **p ≡ 0.**

- It is **NOT** the pure-frequency-keyed class N5 killed (+0.0226–0.0263 dex, 4.4–5.2σ sign-flipped V_flat trend).
  That kill does not extend to 2208.07073. The RAR's tightness in acceleration is *native* to his construction.
- **SPARC scatter implied = exactly the acceleration-keyed baseline** (gate reproduced in-run, locked conventions,
  175 galaxies, unweighted dex / best-Υ on [0.3,1.2]×46): framework a₀ — McGaugh-RAR 0.1950, simple 0.1951,
  fw 0.1969, F4-standard 0.1984; canonical a₀ — best 0.1968. Identical to `mi_f4_sparc_shape_test.out`. SPARC-ALIVE
  for every μ shape (the shape freedom is his).
- **But p = 0 means the N5 corridor escape (p ∈ [0.069, ≥1] dressing) is UNAVAILABLE to this construction.** The
  corridor was the only way a power-law-tail μ survives the solar reflex; Milgrom-22 supplies no dressing (§1: the
  multi-frequency machinery cannot manufacture it for the Sun — suppression 0.72–0.78 vs required ≤0.117). So within
  the corridor logic: Milgrom-22 + power-law μ sits at the dead p=0 corner (F4's own position); Milgrom-22 +
  exponential μ sits at the undressed-PASS corner (N5's context row, now realized by a *published, complete* MI object).

## 4. WIDE BINARIES + THE LENSING WALL

**WB (Ω_WB ≈ 4.2×10⁻¹³ s⁻¹; Ω_gal/Ω_WB ≈ 2×10⁻³ → θ(≈0)):** Milgrom-22's EFE is (i) **scalar-additive across
frequencies** (magnitudes |â(ω)|, no vector angle-averaging — a structural difference from the repo's vector-MI
prescription) and (ii) **θ(0)-enhanced**. His own words on this exact system:
> "for the description of vertical dynamics, or that of wide binaries in the solar neighborhood we have a_ex/a₀ ≈ 2,
> and even a value of θ(0) of a few can have a large impact on 1−μ, since 1−μ[2θ(0)] can be rather smaller than 1−μ(2)."

Quantified (deep bin y_int = 0.18, self-consistent solve; banked vector-MI column gates against
`mi_f4_widebinary_efe.out`):

| shape (framework a₀) | banked vector-MI | M22 θ(0)=1 | θ(0)=2 | θ(0)=e |
|---|---|---|---|---|
| F4/standard | +3.9% | +3.8% | +1.1% | +0.6% |
| simple | +15.2% | +18.0% | +9.9% | +7.5% |
| McGaugh RAR | +13.2% | +12.1% | +6.1% | +4.2% |

(canonical a₀: θ(0)=2 → 1.7/12.4/8.0%; θ(0)=e → 1.0/9.4/5.7%.) **Milgrom-22 SUPPRESSES the WB boost ×2–4 via the
EFE channel** — the frequencies between galactic and planetary play no role (the WB's own term has coefficient
θ(1)=1, as always); the suppression is pure θ(0)-enhanced external quenching. **The DR4 fork is reshaped
(pre-registered in the .out):** a clean DR4 null at ~3% kills soft-shape M22-MI only if θ(0)≲2 (at θ(0)~e the
soft shapes sit at 4–7%, marginal); a +10–15% full-amplitude detection (Chae-type) kills the θ(0)-enhanced EFE for
**all** shapes (the enhancement cannot be undone while θ decreases); an intermediate +4–8% would positively SELECT
M22-style enhanced-EFE MI over both AQUAL-EFE modified gravity and undressed F4. The θ(0)-quenching also bears on MW
vertical/disk dynamics — flagged as a further discriminator, not adjudicated here (his own caveat: "A proper
treatment of the vertical dynamics … must take all this into account").

**Lensing:** the word does not appear in the paper (grep over the full source). The construction is nonrelativistic
by explicit self-restriction:
> "However, here we consider only the nonrelativistic limit, where the gravitational field may be considered static.
> I thus restrict myself to modifications of only the kinetic part of the equations of motion."
His only gesture at the relativistic completion concedes the partner requirement:
> "an eventual relativistic Fundamond will probably involve modification of all parts of the action.
> [footnote:] This will also be necessary, it appears, if we want to reproduce the observation that gravitational
> waves follow the same world lines as photons."
As pure MI with Newtonian interbody forces and an unmodified metric sector, it predicts **baryon-only lensing** and
hits the banked metric-passive wall unchanged: **40.5σ** on the repo's own re-measured isolated lensing RAR
(`f4_lensing_wall.out`; deep-bin amplitude deficit ~230×, C-bracket unbridgeable). Same hybrid conclusion as F4:
**cannot be the whole theory; needs the lensing-carrying metric partner of the spec.**

## 5. VERDICT (both ways, full weight — the four pre-registered outcomes adjudicated)

**The verdict is μ-tail-CONDITIONAL, and the filter is irrelevant to it — that is the finding.**

1. **DEAD-on-reflex for the power-law-μ members** (standard ×6.1–10.9 over the agentE budget at the two physical
   footings, ×205–222 at the bath normalization; simple ×3×10⁴): the agentE kill **transfers to the published
   Milgrom-22 construction essentially undiminished** (kernel suppression 0.72–0.78, θ-insensitive), because the
   θ(1)=1 normalization that anchors rotation curves pins the Sun's own-frequency response. The test the construction
   was built to pass (composite-body CoM) it passes; the test it was never confronted with, it fails — for the μ
   shapes (standard/simple) that the MOND literature historically used.
2. **ALIVE-in-the-corridor (at the p=0 PASS corner) for the exponential-tail member:** Milgrom-22 + McGaugh-RAR μ
   passes the reflex by >10¹³, the precession channel empty, SPARC at the baseline optimum 0.1950 dex, WB inside the
   DR3 degeneracy band — **the full nonrelativistic battery, passed by a published, WEP-safe, conservation-law-complete,
   CoM-solved, time-nonlocal MI functional.** This is the first published object to clear every matter-sector wall the
   repo has erected. **Adoption recommendation:** the spec's matter-sector template should adopt the Milgrom-22 form
   ⟨m â 𝓘 = F̂, 𝓘 = μ_exp[𝓐(ω)/a₀], θ(1)=1⟩ — noting that what the spec's tail/memory mechanism must *derive* is
   then the exponential μ-tail (the dressing-p corridor remains the alternative if the mechanism produces power-law
   tails; the two routes are distinguishable: corridor members suppress the WB boost by frequency, Milgrom-22
   suppresses it by θ(0)-EFE, and ONLY the corridor kills lab/atom-interferometer signatures outright).
3. **Not the whole theory, by its author's own concession:** nonrelativistic, mechanism-free, causality open, and
   40.5σ dead on lensing as it stands — exactly the spec's hybrid slot (trajectory-nonlocal MI matter sector +
   lensing-carrying metric partner), now with the matter half worked out in print.
4. **New falsifiable surface gained:** the θ(0)-enhanced EFE row (WB fork reshaped, §4) and the sign-flipped prograde
   Saturn precession (+0.06–0.09 mas/cy at the bath normalization — within a factor ~2–4 of INPOP15a-C2's σ, a
   *near-future-testable* signature unique to per-harmonic MI).

**Scope locked:** the §1/§2 kill/pass statements are for the concrete published class (Eqs. `law`+`mumu`+`v`/`shiluta`
with any monotone-product μ and any θ with θ(1)=1, θ decreasing fast enough for CoM); the abstract 𝓘 beyond it is
constrained by the rescue audit (§1) but not exhausted. First-order perturbation theory used in §2 (validated against
agentA's amplified-s integrations at ratio 1.0000); the WB numbers use the one-dominant-external-frequency reduction
(his Eq. `exasa` regime). Bug log: (i) naive 1/μ−1 underflowed to 0 below double-eps at physical planetary x — caught
on first run (Mercury rows printed +0.000e+00), replaced with exact stable forms; (ii) the draft verdict text assumed
"the filter kills the precession" — the measured result (suppression ×3.4–6.8 WITH sign flip, channel relaxed not
killed) replaced it; the task's stated expectation was wrong in detail and the correction is recorded, not hidden.
