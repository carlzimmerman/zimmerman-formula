# GW170817 disformal-lensing check — adversarial independent verification

**Verdict: EXCLUDED (not marginal). Erratum: YES.**

Re-ran `gw170817_lineintegral.py` (exit 0) and built an *independent* re-derivation
`verify_independent.py` (exit 0, sympy symbolic + closed-form deep-MOND bracket, no reuse
of the original numeric quadrature). Both footings throughout (canonical `a0=9.36e-11`,
alt `a0=1.13e-10`). A SAVE was hunted as hard as a KILL. No sightline geometry rescues it.

## The four sub-questions, answered independently

**(1) Is the differential B/2, B, or something else? → B/2 (symbolically proven).**
`g~=g+B u u`, rest frame `u_mu=(-1,0,0,0)` → `g~_00=-(1-B)`, `g~_ij=delta_ij` (the `u_iu_j`
block is zero — the same fact behind graviton `c_T=1`). Photon null on `g~`:
`c_gamma=sqrt(1-B)`; graviton on `g`: `c_gw=1`. sympy series:
`|c_gamma-c_gw|/c = 1-sqrt(1-B) = B/2 + O(B^2)`. Factor is **B/2**, photon subluminal. The
`c_T=1` "exact" pass is irrelevant: GW170817 bounds the graviton–photon *difference* = B/2 ≠ 0.

**(2) grad B and the void limit (re-derived).** Lensing potential `= Phi - B/4`; matching the
RAR field `g_obs=nu g_bar` gives (sympy) `grad B = 4(nu-1)g_bar` — matches UNIFICATION.md U2.
Void limit `(nu-1)g_bar / sqrt(a0 g_bar) -> 1` (sympy), so `grad B ~ sqrt(a0 g_bar) -> 0` in the
void. **This kills only the GROWTH of B, not B itself** — the delay `INT (B/2) dl` uses the
*accumulated* B (~1e-6, sustained across each shell), not grad B.

**(3) Worst-/best-case bracket (closed form, independent of any quadrature).**
Deep-MOND `B(r)=(4 sqrt(a0 GM)/c^2) ln(r_out/r)` → analytic
`Delta_t = (2 sqrt(a0 GM)/c^3)[(r_out-r_in) - r_in ln(r_out/r_in)]` per radial crossing.

| sightline (canonical a0) | Delta_t | vs 1.7 s | orders over |
|---|---|---|---|
| BEST case: single thin host shell 2→12 kpc (one MOND radius) | 5.2e5 s | 3.0e5× | 5.5 |
| CONSERVATIVE: host+MW to 100 kpc (banked geometry) | 1.2e7 s | 6.9e6× | 6.8 |
| REALISTIC min: host+MW to 300 kpc, IGM=0 | 4.0e7 s | 2.3e7× | 7.4 |
| WORST: + nominal IGM over 40 Mpc | ~1e11 s | ~6e10× | ~10.8 |

`|c_gamma-c_gw|/c = Delta_t/t_travel ≈ 1e-8` (realistic), vs the `<1e-15` bound → **~7 orders
over**. Alt footing identical to ~10%. **Every point in the bracket EXCLUDES.** The original
script's 3.5e7 s reproduces to within 12% of the analytic 4.0e7 s (difference = full ν vs
deep-MOND ν; same order, independent method).

**(4) Escape-class check.** The framework does **not** escape the TeVeS/bimetric class. B being
*tied* to `(nu-1)g_bar` (not a free field) is exactly why it **cannot be shrunk** below O(1e-6)
in galaxy shells — the disformal strength is fixed by the lensing it must produce. This is a
textbook dark-matter-emulator (Boran, Desai, Kahya & Woodard, PRD 97, 041501 (2018);
Kahya & Desai 2016): photons feel a deeper effective potential than the metric gravitons ride.
Tying B to data makes the wall **harder**, not softer.

## SAVE / KILL audit (both directions)

- **Manufactured SAVE — not present.** The host deep-MOND shell exit (where most B accumulates,
  the single largest term, 2.3e7 s alone) is INCLUDED, not dropped. The void-rescue is correctly
  rejected: it uses `grad B` (which the void suppresses) as if it set the delay, but the delay
  uses accumulated B. The B→0 void boundary condition is the choice *most favorable* to the
  framework and is used.
- **Manufactured KILL — not present.** Each galaxy is a *single radial crossing* (host exit +
  MW entry), not a doubled full-diameter path. Halving to one crossing total still exceeds the
  bound by ~7 orders. Shrinking the outer radius from 300→100 kpc (banked) still gives ~6.8
  orders. The verdict is geometry-robust; there is no forced worst-case path.

## Reconciliation with the banked ~6-order note

The banked `mi_disformal_gw170817_TENSION.py` (`Delta_t~3.6e6 s`, `|dc|/c~8.8e-10`, ~6 orders)
was **not** a single-galaxy wrong-path estimate: it already used host(1e11)+MW(6e10) and set
IGM=0. This independent segmented + closed-form re-derivation **reproduces it to the same
order**. The original prep script is ~10× larger only because it integrates to 300 kpc vs the
banked 100 kpc — a choice that does not change the verdict (both exclude by 6–7 orders).

## Consequence for the published paper (DOI 10.5281/zenodo.21403470)

`MI_FIELD_THEORY_RESULTS_2026.tex:489-490` ("Honest hinge") lists the LOS timing integral
`INT (B/2) dl` as open but calls it **"order-of-magnitude satisfied only."** That phrase is
**FALSE** — the integral is order-of-magnitude **EXCLUDED** by ~6–7 orders (`Delta_t~3.5e7 s
>> 1.7 s`; `|dc|/c~1e-8 >> 1e-15`, both footings). **Erratum required:** replace
"order-of-magnitude satisfied only" with a plain statement that the photon-vs-graviton LOS
timing integral is GW170817-**excluded**, so the disformal photon-only route to dark-matter-free
lensing does **not** clear GW170817 — a genuine open failure of the lensing sector, not a
near-miss. The abstract/§2.3 line `c_gamma^2=1-B>0` (line 427) is true (cone stays Lorentzian)
but must **not** be read as a GW170817 pass — the same B that keeps the cone Lorentzian is what
violates the timing bound.

**Scope:** what is excluded is *specifically* the disformal photon-metric route to
dark-matter-free lensing. The dynamics sector (RAR, BTFR, graviton `c_T=1`) is untouched.
No "resolved"/"proves" language warranted.

## Reproduce
```bash
cd /Users/carlzimmerman/new_physics/prep_2026/gw170817_check
python3 gw170817_lineintegral.py   # exit 0, original segmented integral, both footings
python3 verify_independent.py       # exit 0, sympy symbolic + closed-form bracket
```
