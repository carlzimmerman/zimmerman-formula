# AX1_action_for_law: NO UNSCREENED ACTION GIVES THE LAW AND PASSES THE SOLAR SYSTEM. Every class whose static limit is AQUAL or QUMOND with g²/(g + a0) fails Cassini Q2 (1.69–5.18× Hees) and, without a turn-off, the planets (1.3e4–1.6e4×). Only v3s's screening length passes G1–G4 on both footings (reading; clean label UNDECIDED)

κ = ½ FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. Not blind. Not theory closed. Nothing here says the data favour the framework. The cold sector stays retired; nothing here reinstates it. **CMB and clusters are out of scope and open**; the cluster gap is a requirement, not solved. Literature entries are PROVISIONAL (web snippets 2026-11-04 or memory). No downloads; every run takes seconds on one thread.

## Lead table: final status of every class

| class | canonical | alt | killing gate and number | where |
|---|---|---|---|---|
| AQUAL / QUMOND / RAQUAL | **FAIL** | **FAIL** | G2a 2.44–4.55× (AQUAL), 1.69–3.68× (QUMOND); G3: a conformal scalar gives no extra lensing | AUDIT |
| BIMOND | **FAIL [G4]** | **FAIL [G2a]** | alt: E0 1.19–1.20× Hees for every candidate. Canonical: only β ≥ 2.5 survives G1–G2; G4 fails on Chesler & Loeb 2017 [PROVISIONAL] | `BIMOND/` |
| TeVeS | **FAIL** | **FAIL** | G4: GW170817 (Boran+ 2018; Skordis & Złośnik 2019) | AUDIT |
| AeST | **FAIL** | **FAIL** | G2a AQUAL: law 2.44–5.15×; β fail E0 1.01–1.12× / 1.42–1.47×; G2c α1 = −22/5 (AS3) | `AeST/` |
| khronon (Blanchet–Marsat) | **FAIL** | **FAIL** | G2a as AeST; G2c open | `khronon/` |
| Einstein-aether MOND | **FAIL** | **FAIL** | G4: GW speed depends on the local potential (Chesler & Loeb 2017); \|c13\| ≤ 1e-15 | AUDIT |
| superfluid, effective field only | **FAIL** | **FAIL** | G2: √(a0 g_N) at Saturn 1.1e7 / 1.2e7 × the bound; G1 different law; G3 conformal | AUDIT |
| non-local metric MOND (DEW) | **OPEN [G4, static form]** | **FAIL [G2a]** | alt: E0 1.19–1.47×. Canonical survives only with β ≥ 2.5 and only if its static form is QUMOND-type | `nonlocal/` |
| v3s (regraded under the 11-04 lift) | **UNDECIDED, reading PASS** | **UNDECIDED, reading PASS** | none in G1–G4; inherits C6's failed check C2 (float). The 10-24 verdict stands | `v3s/` |

- **v3s update, 11-04:** `../C6P_cassini_high_precision/` reruns C6's C2 at 30, 50 and 80 digits and under an analytic rewrite, and the check clears. The Solar-System gate (Cassini Q2, planets, γ − 1) is then a **clean PASS on both footings**: Q2 is ≥ 4.8e7 inside Hees, and the worst planet is Mars at 0.173 of its bound at 24 pc. This adopts nothing, and the 10-24 verdict stands.
- **v3s weak spots, 11-04:** `../V3W_v3s_weak_spots/`. Results by test:
  - **W1 PASS.** γ − 1 = 0 and β = 1 are derived from the action, with remainders ≤ 1.3e-13 and ≤ 1.1e-12.
  - **W3 PASS.** On KiDS isolated lenses M_lens/M_dyn,law = 1.13 ± 0.21 (canonical) and 1.03 ± 0.19 (alt); the M★ systematic dominates.
  - **W4 split.** c_T = c and health on galaxy backgrounds PASS; health on the Solar-System background is UNDECIDED, because it was never run at β = η = 0.
  - **W2 UNDECIDED.** C6's checks reproduce, but the in-window ladder misses its 2e-2 line at 2.3e-2.

  This adopts nothing.

G5 (a0 ∝ √(Gρ_DE) from the action): **by hand in every class.** KF1 finds nothing forced.

## Why, in one paragraph
Cassini's Q2 is made at r ≈ 7000 AU around the Sun, where g ≈ a0. That is the range SPARC pins, so no static interpolation can both reproduce SPARC and stay quiet there in AQUAL form (E2, D7c). In QUMOND form a sharper β ≥ 2.5 does it on canonical only, and it is not g²/(g + a0). The alt footing fails at the framework's own Milky Way field. A turn-off above y ≈ 60 fixes the planets for free but not Q2. The record's one way past this is a length that screens each mass. v3s's L★ does that, and so do the filtered-QUMOND rules (KT16/KT17), which have no action. The relativistic classes that keep the law's interpolation without that length (BIMOND, TeVeS, Einstein-aether) die on GW propagation; AeST and khronon die on Q2 first.

## Recommendation
- **No non-v3s class is viable for *this* law on both footings.** The nearest non-v3s miss is a QUMOND-type theory with a β ≥ 2.5 interpolation, canonical only. In BIMOND that dies on GWs [PROVISIONAL]; in DEW it waits on two derivations. It is a different law, and alt fails it.
- If the action question is to be pursued, the owner's call is between (a) v3s as it stands (reading PASS here; 10-24 failures out of scope) and (b) a covariant smoothed-QUMOND action with a fixed length. (b) is the same mechanism as L★ in another form, and no action for it exists.

## Unfinished
- BIMOND's G4 rests on a snippet of Chesler & Loeb; their argument was not read. The δ-mode share α/(α + β) and the O(a0) wave gradients are argued support, not a speed derivation.
- DEW: the non-spherical static limit and the tensor speed on a MOND background.
- Khronon G2c: the record's static and moving branches disagree (X15 vs A22).
- AeST G4 health: X6's H1 line not re-read.
- v3s: C6's check C2 is a float-cancellation failure; a higher-precision rerun of C6 would clear the clean label. Not done here.

## Files and commits
`AUDIT.md` 677c5c79a3. Criteria / result: common + BIMOND fd417eea04 / ffd6f71b2a; AeST 7b7d1a7811 / 360bf66de8; khronon 6b618b184d / 6d20d2bbc9; nonlocal cd18cad5dd / 04cbb9ddb5; v3s 9f1d7df884 / 0c5f1cb613. Engine `common/ax1_engine.py`: K1 reproduces D7c / PAPER58's QUMOND Q2 to 3.8e-6, K2 the β members to 6.9e-8, K3 grid 5.3e-6, K4 exact; the ν ≡ 1 MUTATE twin fails K1 and K2 in every class; every class rerun is byte-identical.
