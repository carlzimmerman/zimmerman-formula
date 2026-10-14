# THEORY PUSH A (2026-10-14): can anything framework-native lift the MW ultra-faints by +0.33 dex?

> Status: **paper analysis only.** No script was run, nothing is committed, and no frozen result is changed. A 1024³ run was live,
> so the only numbers computed here come from one-line `python3 -c` arithmetic (top-hat r_f, isothermal σ). Every other number
> is cited from a committed lane. κ = ½ is FITTED. The cold energy's mass is required. No dark-matter particle is added and no
> ΛCDM halo model is used. This is not "theory closed".

## 0. Bottom line

- **No route works as the framework stands.** Each route is killed by a named constraint (table in §6).
- **One route has the right size: "fossil free cold energy".** This is collisionless, untethered cold energy that came with the
  baryons the ultra-faints lost early. It is placed by cold collapse at the formation epoch and acts on the stars only through
  Newtonian gravity. Its amount comes from the record's own numbers: 5.364 × (R_ind − 1) M_b, with R_ind ≈ 117 from CFG317's
  leaky box. With no knob, it gives an isothermal floor of σ_free ≈ 3.6 km/s. That moves the UFD median from +0.325 to about
  **−0.04 dex** (yield bracket +0.04 to −0.13).
- **It cannot be confined to the ultra-faints.** The same bookkeeping over-lifts the MW classicals to −0.14 to −0.21
  (−1.7 to −2.5σ) and the LV field dwarfs to about −0.18 (−2.4σ). If the SPARC dwarfs share the universal yield deficit
  (CFG317 point 3), it adds a +0.1 dex systematic to their outer g_obs. This repeats CFG42's trade (ΛCDM debris closes the
  UFDs and over-predicts the classicals), here with native masses.
- **It also needs two things the record does not have:**
  - a two-population postulate (CFG781 review: CFG723's identity ∇·P = ρ − ρ̄ forbids a free core in a single medium);
  - a **selector** that decides which lost baryons leave free cold energy. No such selector is derived.
- **Hand verdict: PARTIAL at best** (UFD closes, classicals in tension, field dwarfs and SPARC at risk). **FAIL** is likely
  unless the selector excludes gas-rich systems. Criteria are frozen-ready in §7.

## 1. The target in numbers (record)

- **Offset:** +0.325 ± 0.086 dex (canonical), +0.304 (alt), KM median of 31 + 9 limits (AUDIT_UFD). A mean statistic gives
  4.8σ.
- **Deep-law estimator:** σ_law² = g r/3 at r = (4/3) r_half with g = √(a₀ G M_b/2)/r. This gives σ_law ≈ 1.7 km/s at
  M_b = 1e4 M☉, independent of r.
- **What is needed:** σ_obs/σ_law = 10^0.325 = 2.11, i.e. **σ ≈ 3.6 km/s** at M_b = 1e4.
  - As extra mass added through the law: × 20 (Υ_V ≈ 35).
  - As extra Newtonian mass inside r: ≈ 84 M_b (CFG336 screen: k = 13.2 × M_b/f_b, all inside r).
- **What must not move:**
  - MW classicals: +0.10 stars-only, or +0.027 in the gas=True harness (CFG336), error ≈ 0.084.
  - M31 LVD +0.044 and Collins +0.064.
  - LV field −0.044 (error ≈ 0.073).
  - SPARC 0.1009 / 0.0994 dex.
  - Cassini Q2 (CFG770).
- **Already excluded (cited, not redone):**
  - binaries (CFG29: needs 3.4 km/s everywhere);
  - SPS Υ (≤ 0.05 dex);
  - kernel (ν_s = ν_mono to 5e-9 here);
  - footing (alt −0.02);
  - EFE (+0.44, worse);
  - infall gas (CFG18: +0.22);
  - native cosmic share at any z_f (CFG336, mass budget: the phantom exceeds the whole share 3.5×);
  - B's switch with R_ind (CFG317: needs R ≈ 4,500, has 117);
  - frozen relic (CFG776: deficit, f −1.07).

## 2. Route (1): fossil free cold energy from the original baryons

**Mechanism.**
- Before the system's gas was lost (reionisation photo-evaporation and SN outflow), its catchment held
  M_init = R M_b,now baryons, with cold energy 5.364 per baryon.
- The part that collapsed and phase-mixed as ordinary cold matter is *untethered*. This is eq. (9) of THEORY_v3 (no basin,
  no tether), held fixed by Argon's kernel (CFG781: phase-mixed carrier is untethered).
- This free part is collisionless and self-gravitating (its self-gravity is not cancelled, since it has no tether). It is
  **not** pushed by W_rem, so CFG776's expulsion does not act on it.
- Under the record's preferred condensed-source variant (T12), it does not source the law. It adds Newtonian gravity:
  - g = ν_s(g_N,cond/a₀) g_N,cond + G M_free(<r)/r²
  - M_free = 5.364 (R − 1) M_b
  - placement: collapse from rest at z_f (CFG336's top-hat r_f, P1 isothermal, or CFG637 Method B in the declared lane)
  - tethered part: the law on today's condensed baryons, supply 5.364 M_b/0.10 (no surplus, so CFG776 does not apply).
- For P1, M_free(<r) = M_free r/r_f, so **σ_free² = G M_free/(3 r_f), independent of r_half.** It is an isothermal floor.

**Numbers.** Inputs: R from CFG317 B1 (UFD 117; yield bracket 59–234), z_f from CFG336's a-priori split (8 for UFDs, 3
otherwise), f_b 0.157126, a₀ 1.13e-10. Δ = 0.5 log₁₀(1 + σ_free²/σ_law²).

| system (typical) | M_b | R | r_f | σ_free | σ_law | Δ (dex) | baseline → predicted |
|---|---|---|---|---|---|---|---|
| UFD | 1e4 | 117 | 0.70 kpc | 3.56 | 1.70 | +0.37 | +0.325 → **−0.04** |
| UFD, yield −0.5 / +0.1 | 1e4 | 59 / 234 | 0.56 / 0.89 | 2.8 / 4.5 | 1.70 | +0.29 / +0.45 | → +0.04 / −0.13 |
| UFD, M_b 4e3 | 4e3 | 117 | 0.52 | 2.62 | 1.35 | +0.34 | → −0.01 |
| MW classical | 3e6 | 30 | 6.7 kpc | 10.0 | 7.1 | +0.24 | +0.10 → −0.14 (−1.7σ); +0.027 → −0.21 (−2.5σ) |
| classical if z_f = 8 | 3e6 | 30 | 3.0 | 15.0 | 7.1 | +0.37 | → −0.27 to −0.34 (FAIL) |
| LV field (gas-rich) | 3e7 | 6 | 8.5 | 11.7 | 12.6 | +0.14 | −0.044 → −0.18 (−2.4σ) |
| SPARC dwarf (R ≈ 3 assumed) | 1e9 | 3 | 35 | V_c 36 km/s vs law V_f 62 | | | outer g_obs +0.13 dex |

Scaling: x ≡ σ_free²/σ_law² ∝ R^{2/3} M_b^{1/6} (1 + z_f). So x **rises** weakly with mass at fixed R. The classicals keep
x ≈ 0.46 × that of the UFDs only because their R and z_f are smaller.

**Stability vs CFG776/749.**
- Stable *only* under the two-population postulate. The free part has no tether, so no push acts on it.
- It is bound by its own gravity, so CFG749's "cold energy at orbital speed is unbound" applies only to the tethered part.
- If instead the fossil cold energy was ever tethered (it formed after the basin), CFG776 expels it and overshoots into a
  deficit (UFD f −1.07). The route then dies.
- Tidal survival: with M_free ≈ 6e6 M☉, the MW tidal radius at 50 kpc is ≈ 0.9 kpc ≥ r_f, so the inner 40 pc is safe.

**What kills it (as the record stands).**
- **(a) Selector.** CFG317 point 3: the yield deficit is universal ("every dwarf lost most of its baryons"). Fossil free cold
  energy therefore lands on the LV field dwarfs and, by extension, SPARC dwarfs. The LV field goes to −2.4σ, and SPARC dwarfs
  pick up a +0.1 dex tilt that the 0.10 dex RAR does not show. This is CFG35/CFG42's lesson again.
- **(b) Classicals.** They sit at the 2σ line (−1.7σ stars-only, −2.5σ in the gas harness). They fail outright if they share
  the UFD z_f.
- **(c) No derived origin.** Free cold energy has no derived origin (THEORY_v3 §3b; CFG741/742 selectors closed). The
  two-population postulate is in tension with CFG723's single-medium identity.
- **(d) Behaviour.** In the UFDs it behaves exactly like a cold dark halo of native mass. It differs from ΛCDM only in amount
  (5.364 × lost gas, about 50× below the 3e8 at which CFG42's debris crossed zero) and in profile (collapse at z_f, not
  abundance matching). Report it as that, plainly.

**What survives.** The *magnitude* is not tuned. σ_free ≈ 3.6 km/s against 3.6 needed comes from 5.364, R_ind, z_f = 8 and
f_b alone. R_ind is a lower bound for the UFDs (photo-evaporated gas is invisible to the leaky box, CFG317 B1). The boost is
therefore a lower bound too, and the risk is overshoot, not shortfall.

**Decisive tests.**
1. **On disk:** the UFD residual must rise with log R_ind at fixed M_b, with slope d log σ/d log R ≈ ½ · x/(1+x) · ⅔ ≈ 0.26.
   CFG317's post-hoc within-UFD ρ is +0.25 (p 0.08, a weak hint). At fixed M_b and R it must be **independent of r_half**.
2. **Data:** σ(R) profiles flat to r ~ 0.5 r_f ≈ 300 pc (isothermal floor). The law alone is also flat, so this is weak.
   Stronger: the tidal radius sits at the free-halo scale (≈ 0.9 kpc), not the law's.
3. **Kill:** an SPS/metallicity-independent loss measure (e.g. Weisz+14 quench epochs, not on disk) showing UFDs and field
   dwarfs lost similar fractions, while only UFDs are lifted.

## 3. Route (2): does stiffness screening retain a surplus?

**Mechanism tried.**
- Inside ℓ_γ = L*²/(2 r_M) the response is screened (CFG691). The cubic push R(u) = u²/(a₀ − u) needs u, and screening
  suppresses u. So a tethered surplus inside ℓ_γ might not be expelled.
- An intriguing near-miss: the *peak* (pre-loss) tethered phantom of M_init = 117 M_b inside 40 pc is ≈ 63 M_b. If that relic
  were retained, it would give σ ≈ 4.8 km/s at 40 pc (y_init ≈ 0.45, ν ≈ 2.07), close to the observed ≈ 4. That is exactly
  CFG776's H-FR, which failed dynamically.

**Why it dies.**
1. **Sign (convexity).**
   - W_rem'' > 0 for u < a₀, the gradient term (γ/2)|∇P|² is convex, and the completed square is quadratic.
   - So the static functional has a unique minimum (CFG722's argument, extended).
   - Screening *lowers* that minimum: CFG691 says UFDs get worse, and a star's phantom is ≤ 0.035 of its mass. It does not
     create a second one.
   - A retained surplus is still uphill, and the stiffness gradient force now pushes it out. The relaxation *rate* inside
     ℓ_γ is not computed (an honest gap), but the sign is fixed.
2. **Volume.**
   - Today ℓ_γ = 4.7 pc × (M_b/1e4)^{-1/2}. That is 1.5–5 pc for the bulk of UFDs, against r = (4/3) r_half ≈ 30–130 pc.
   - At formation ℓ_γ,init = L*²/(2 r_M,init) ≈ 0.4 pc, so nothing was screened when the relic formed.
   - Even total retention inside 5 pc of the peak phantom (≲ a₀ r²/G ≈ 2e4 M☉ ≈ 2 M_b) adds ≈ +0.04 dex at 40 pc.
   - Only the faintest (M_b ~ 1e3, ℓ_γ ≈ 15 pc) could gain, so the median does not move.
3. **Classicals/SPARC:** untouched (ℓ_γ ≪ 1 pc), so it would be harmless if it worked. It does not work.

**Verdict:** killed by convexity (sign) and by geometry (screened volume ≪ r_half).

## 4. Route (3): tides and non-equilibrium

| reading | status | constraint that kills it |
|---|---|---|
| Tidal heating at pericentre | **Excluded (data):** D_gc > 80 kpc gives +0.325 (CFG28); dropping disturbed systems *raises* it to +0.355 (AUDIT row 4) | Data |
| Same, framework-side | **Excluded:** density-match basin (CFG693, α = 2): r_J = D V_f/V_h ≈ 0.9 kpc at 50 kpc (V_f 3.5, V_h 200 km/s), r_J/r_half ≈ 20–30; CFG286 r_t/r_ev ≈ 34 | Basin ≫ r_half |
| Unbound / expanding remnant | **Excluded:** at σ_obs ≈ 2.1 σ_law the kinetic energy is ≈ 4.5× virial. Deep-law σ depends only on M, so the system cannot re-virialise at σ_obs. It expands on a crossing time 30 pc / 4 km/s ≈ 7 Myr, so seeing 40 systems in that state is ≲ 1e-3 probable each | Timescale |
| Not yet settled (cold energy still filling) | **Wrong sign:** an unfilled halo means a deficit, so a lower σ (CFG747/748). CFG763: τ ≤ 3.5 Gyr ≪ the UFD ages of 12–13 Gyr | Sign + clock |
| Overshoot after baryon loss | **Wrong sign:** CFG776 expels the surplus into a deficit (f −1.07) | Sign |
| Not modelled anywhere | Tidal heating *under ownership* at measured pericentres (AUDIT correction 2). The two exclusions above make a +0.33 dex median effect implausible | — |

## 5. Route (4): everything else in the record

| idea | estimate | killer |
|---|---|---|
| Law fed by initial baryons (M_init = R_ind M_b, AUDIT route) | UFD −0.208 (overshoot), classicals +0.10 → −0.271 | classicals |
| B's switch with R_ind (CFG317) | no tile moves; needs R ≈ 4,500 | budget |
| Native share with z_f density (CFG336) | phantom > whole share in all 40 UFDs | budget (Lean-certified) |
| Infall gas (CFG18/FG001 H8) | +0.22, 2.6σ | still fails; no gas measured at M★ 1e3–1e5 |
| Argon free = 5.364 M_hot *today* (CFG781) | UFD M_hot = 0, so no change | declared expected FAIL |
| Host's cold energy inside the UFD | MW phantom density at 50 kpc ≈ 3e-4 M☉/pc³, so ≈ 80 M☉ inside 40 pc ≪ 1e4 | negligible |
| Capacity a₀/πG, overflow H-OF | UFD phantom far below the cap. The overflow is pushed to the basin edge (CE kernel) and is unbound after loss (CFG749) | wrong place / unbound |
| a₀ footing or κ (0.42 ± 0.10) | σ ∝ a₀^{1/4}; +0.325 needs a₀ × 20 | SPARC / CFG493 |
| a₀(z) at formation | flat for w = −1 (CFG549) | no lever |
| All-source law (free mass also sources ν) | UFD × (1 + 50)^{1/4} gives −0.10; classicals −0.22 to −0.29 | classicals (worse than T12 reading) |
| Binaries, SPS Υ, kernel, EFE | see §1 | excluded |

## 6. Ledger of routes

| route | size right? | classicals | SPARC / SS | killer |
|---|---|---|---|---|
| (1) fossil free cold energy | **yes** (−0.04; +0.04 to −0.13) | −1.7 to −2.5σ | SPARC dwarfs +0.1 dex tilt if R_ind universal; SS untouched | selector + two-population postulate |
| (2) screened retention | no (+0.04) | untouched | untouched | convexity (sign), ℓ_γ ≪ r_half |
| (3) tides / non-equilibrium | no | — | — | data (CFG28, AUDIT), r_J/r_half ≈ 20–30, 7 Myr expansion, deficit sign |
| (4) others | no, or overshoot | break | — | budget (CFG336), classicals, sign |

## 7. Proposed frozen criteria: route (1), "fossil free cold energy"

**CFG ID: none taken.** Check the LEDGER and `ls campaign_fresh_gravity | grep CFG` and ask the owner. Run only after the 1024³
run and the queued T1x/CFG777/780/781 have finished. 1 process, < 1 GB.

**Question.** Does untethered, collisionless cold energy carried by the baryons each dwarf lost, 5.364 × (R_ind − 1) M_b,now,
placed by cold collapse at the system's formation epoch and added as Newtonian mass to the condensed-source law, close the MW
ultra-faints without breaking the classicals, M31, the LV field dwarfs or SPARC?

**Declared calculation (no new constant; nothing tuned).**
- **Amount.** R_ind = CFG317 B1 per object (nominal yield −0.2; bracket −0.5 / +0.1 reported). Non-detections use CFG317's
  declared fallbacks. M_free = 5.364 (R_ind − 1) M_b,now.
- **Epoch.** z_f = CFG336 a-priori split (UFD 8, range 6–10; others 3, range 2–4). The collapse mass is R_ind M_b/f_b.
- **Profile.**
  - P1 (primary): isothermal truncated at the top-hat r_f, as CFG336.
  - PB: Method B (CFG637 `maxent_reservoir`, at the turnaround energy of the collapse mass, self-gravitating, in the potential
    of baryons + tethered + free).
- **Gravity.** g = ν_s(g_N,cond/a₀) g_N,cond + G M_free(<r)/r² (T12 condensed source; free mass Newtonian). The all-source
  variant is reported, not decisive. Both kernels and both footings, never pooled.
- **Harness.** CFG45 `sigma_read` (r = (4/3) r_half, σ² = g r/3), KM median with limits, bootstrap 1000 seed 42, Υ_V 1–4 floor
  ⊕ ½ |R-bracket shift| ⊕ ½ |z_f-range shift|.
- **SPARC guard.**
  - R_ind(M_b) taken from CFG317's own per-object log R_ind–log M_b relation (OLS on the 97 objects, frozen before scoring),
    applied to every SPARC galaxy with z_f = 1.5.
  - Score the RAR scatter and the binned low-g_bar offset.
- **Solar System.** Report the MW's free density at 8 kpc under the same rule. Pass if ≤ the CFG770 Q2/planetary margins.

**Pass / fail lines (canonical footing decides; alt reported).**
- **P-UFD:** |z| < 2 for the MW UFD KM median at the nominal yield **and** at both yield ends.
- **P-SAT:** MW classical, M31 Collins, M31 LVD all |z| < 2 (CFG336 harness, gas=True).
- **P-FIELD:** LV field |z| < 2.
- **P-SPARC:** RAR scatter ≤ 0.11 dex **and** |median offset| ≤ 0.05 dex in the lowest g_bar bin.
- **SOLVES** = all four pass. **PARTIAL** = P-UFD passes and exactly one other fails. **FAIL** = otherwise, or P-UFD fails.
- **Correlation test (reported, power-checked):** within UFDs the partial ρ(residual of the *law*, log R_ind | log M_b) > 0
  at p < 0.05. The predicted slope is +0.26 per dex. Run a planted-signal power check (as CFG317 C4). Underpowered means
  NOT DIAGNOSTIC, never a pass.

**Controls.**
- **K1:** R_ind ≡ 1 reproduces the AUDIT_UFD baseline (+0.3245 / +0.3045) and CFG336's law rows to 1e-4.
- **K2:** P1 encloses M_free at r_f to 1e-12, and σ_free² = G M_free/(3 r_f) analytically to 1e-10.
- **K3:** Method B converges for ≥ 95% of systems.

**MUTATE.**
- **M1:** shuffle R_ind across all scored dwarfs (seed fixed). The within-UFD partial ρ must vanish (|ρ| < 0.1), and the UFD
  median must change by ≥ 0.03 dex.
- **M2:** free mass placed uniformly inside r_ta instead of P1/PB. The UFD median must change by ≥ 0.05 dex (placement
  matters).

**Hand estimate (before any script; one-line arithmetic above).**
- UFD +0.325 → −0.04 (bracket +0.04 / −0.13), so **P-UFD PASS**.
- MW classicals +0.027 → about −0.21 (−2.5σ), so **P-SAT FAIL** likely. With stars-only +0.10 → −0.14 it would be −1.7σ.
- LV field −0.044 → −0.18 (−2.4σ), so **P-FIELD FAIL** likely.
- SPARC dwarfs with R ≈ 3: outer g_obs +0.13 dex, so **P-SPARC FAIL** likely.
- **Expected: FAIL (the CFG42 trade, native version), PARTIAL at best.**
- What would change it is a *derived* selector that gives free cold energy only for gas lost before the tether could act
  (photo-evaporation below the IGM temperature at z_re). It must be written down and frozen as its own lane *before* this
  one. Otherwise it is a knob.

κ fitted; cold energy mass required; no DM particle added (but in UFDs route (1) is behaviourally a cold halo of native mass,
and must be reported as such); not theory closed.
