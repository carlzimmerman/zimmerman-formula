#!/usr/bin/env python3
"""
L153e -- VERDICT: does a c_s normalisation exist for which (a) the CMB clustering survives, (b) dwarfs and the
         Milky Way are clean, (c) clusters retain the dust, (d) the oscillatory radius sits outside rotation
         curves and weak lensing?  Assembled from L153a-d's committed results files (no new physics here).
=============================================================================================================
POLARITY: each check ASSERTS a statement; PASS = true.  No check uses a literal True.
"""
import json, os, sys, time
import numpy as np

T0 = time.time(); FAILS = []; N = [0]
def check(name, ok, detail=""):
    N[0] += 1; ok = bool(ok)
    tag = "PASS" if ok else "FAIL"
    if not ok: FAILS.append(name)
    print(f"  [{tag}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)
HERE = os.path.dirname(os.path.abspath(__file__))
def load(tag): return json.load(open(os.path.join(HERE, f"L153{tag}_results.json")))
A, B, C, D = load('a'), load('b'), load('c'), load('d')
C_KMS = 299792.458
CEIL_TKS = np.sqrt(3.21e-6)*C_KMS          # arXiv:1601.05097, constant GDM sound speed, 99.7% (Planck 2015)

sec("E1 -- the sector AS WRITTEN in L139 (constant c_Y, c_s^2 ~ a^3): the identity kills it before any collapse")
check("E1-1  all four lanes ran clean (every load-bearing check passed in L153a-d)",
      all(x['checks_failed'] == 0 for x in (A, B, C, D)),
      "failed: " + ", ".join(f"L153{t}:{x['checks_failed']}" for t, x in zip('abcd', (A, B, C, D))))
check("E1-2  c_s^2 = eps c_ad^2 with eps = 2 c_Y Qbar/K_Q ~ a^3 (L153a A2-3/A3-3): the a^+3 sound speed IS an "
      "a^+3 gravitational coupling; the span between recombination and today is 1.3e9",
      A['eps_span'] > 1.29e9 and A['identity'].startswith("c_s^2 = eps c_ad^2"), f"eps span = {A['eps_span']:.3e}")
p0 = A['p0']
check("E1-3  no normalisation is CDM-like at both ends: every eps(today) fails at recombination (ln ratio to "
      "CDM >= +2.3 or frozen) or explodes afterwards (ln late growth/CDM up to 2e4) -- L153a A5-1..A5-3",
      all(abs(r['ln_rec_vs_cdm']) > np.log(1.1) or abs(r['ln_late_vs_cdm']) > np.log(1.5) for r in p0),
      "; ".join(f"eps(1)={r['eps_today']:.0e}: rec {r['ln_rec_vs_cdm']:+.2f}, late {r['ln_late_vs_cdm']:+.1e}" for r in p0))
print("""  => BINDING CONFLICT, size 1.3e9: the coupling that must be ~1 at z = 1100 (to hold the potential for the third
     peak) and ~1 today (to not explode structure) differs by (1+z_rec)^3 in the transplant.  Nothing in parts 1-3
     can be reached by this sector because it never clusters like CDM in the first place.  DEAD.""")

sec("E2 -- the EP-consistent repair (c_Y -> K_Q/(2 Qbar), i.e. Lorentz-invariant k-essence dust; c_s = c_ad = const)")
floor_gal_template = B['window']['canonical'][0]; floor_gal_template_alt = B['window']['alt'][0]
ceil_cluster = B['window']['canonical'][1]
floor_sparc = D['tight_floor']; floor_sparc_loose = D['loose_floor']; floor_L61 = max(D['L61_floors'].values())
lf = C['lensing_floor_10pct']
floor_wl_iso11 = lf['canonical_gext0.01_Mb1e+11']; floor_wl_iso10 = lf['canonical_gext0.01_Mb1e+10']
floor_wl_loose = min(lf.values()); floor_wl_strict = max(v for v in lf.values() if np.isfinite(v))
rc = C['rC_floors']; floor_vsb_11 = rc['100000000000.0']['rc1000']; floor_vsb_10 = rc['10000000000.0']['rc1000']
c_deep = C['c_deep']
print(f"  (a) CMB : constant c_s = c_ad; published ceiling c_s^2 < 3.21e-6  =>  c_ad <= {CEIL_TKS:.0f} km/s   [arXiv:1601.05097]")
print(f"           the p = 1 sector tracks CDM to <1e-4 at k = 0.06 at recombination for all c_ad <= 537 (L153a A5-4)")
print(f"  (b) galaxies clean: template floor {floor_gal_template:.0f} (can) / {floor_gal_template_alt:.0f} (alt) km/s [L153b B3]; "
      f"SPARC a0-refit floor {floor_sparc_loose:.0f}-{floor_sparc:.0f} km/s [L153d]; L61 fixed-footing median floor {floor_L61:.0f} km/s")
print(f"  (c) clusters retain: 1e14-3e14 Msun keep > 50% of their cosmic share for c_ad <= {ceil_cluster:.0f} km/s [L153b B3]")
print(f"  (d) oscillatory/lensing: Helmholtz scale mu^-1 = {C['mu_inv_300']:.1f} Mpc x (c_ad/300) -- outside both ranges for all c_ad above (b);")
print(f"           induced-atmosphere 10% lensing floor: {floor_wl_loose:.0f}-{floor_wl_strict:.0f} km/s over footings/g_ext/M_b, "
      f"{floor_wl_iso11:.0f} km/s for an isolated 1e11 lens (canonical) [L153c C3]")
print(f"           on VSB's isolated-log scaling (r_C > 1 Mpc): {floor_vsb_11:.0f} (1e11) / {floor_vsb_10:.0f} (1e10) km/s [L153c C2]")
print(f"           if the a_b >= 1e-15 KiDS points are trusted (MMH2023 deep bound): c_ad >= {c_deep:.0f} km/s [L153c C1]")
lo_primary = max(floor_sparc, floor_gal_template, floor_wl_iso11); hi_primary = min(CEIL_TKS, ceil_cluster)
lo_loose = max(floor_sparc, floor_gal_template, floor_wl_loose)
lo_vsb10 = max(floor_sparc, floor_vsb_10); lo_vsb11 = max(floor_sparc, floor_vsb_11)
print(f"\n  WINDOW (primary: isolated 1e11 lens, canonical, 10% criterion):  c_ad in [{lo_primary:.0f}, {hi_primary:.0f}] km/s  "
      f"=  c_s^2 in [{(lo_primary/C_KMS)**2:.2e}, {(hi_primary/C_KMS)**2:.2e}]  (ratio {hi_primary/lo_primary:.2f} in c_ad, {(hi_primary/lo_primary)**2:.2f} in c_s^2)")
print(f"  WINDOW (loosest lensing setting):                                c_ad in [{lo_loose:.0f}, {hi_primary:.0f}] km/s")
print(f"  WINDOW (VSB isolated-log scaling, 1e11 lenses):                  c_ad in [{lo_vsb11:.0f}, {hi_primary:.0f}] km/s"
      + ("  (EMPTY)" if lo_vsb11 >= hi_primary else ""))
print(f"  WINDOW (VSB isolated-log scaling, 1e10 lenses):                  c_ad in [{lo_vsb10:.0f}, {hi_primary:.0f}] km/s"
      + ("  (EMPTY)" if lo_vsb10 >= hi_primary else ""))
print(f"  WINDOW (deep KiDS points trusted):                               c_ad >= {c_deep:.0f} vs <= {hi_primary:.0f}  (EMPTY)")
check("E2-1  a window EXISTS for the repaired sector under the primary settings, and it is a knife-edge: "
      "[300, 537] km/s, a factor 1.8 in c_ad (3.2 in c_s^2) -- numerically L138's 3.2, now with the correct "
      "temperature, a nonlinear atmosphere and an EFE-anchored lensing floor",
      280 <= lo_primary <= 320 and 530 <= hi_primary <= 545 and 3.0 <= (hi_primary/lo_primary)**2 <= 3.4,
      f"[{lo_primary:.0f}, {hi_primary:.0f}] km/s")
check("E2-2  the floor is set by LENSING (300 km/s), not by galaxies (175) nor by the templates (150): the "
      "L61/SPARC double-counting is NOT what binds once the dust is placed in its atmosphere",
      floor_wl_iso11 > floor_sparc > floor_gal_template - 1e-9, f"lensing {floor_wl_iso11:.0f} > SPARC {floor_sparc:.0f} >= template {floor_gal_template:.0f}")
check("E2-3  the ceiling is the CMB (537), not the clusters (700): clusters are never the binding side",
      CEIL_TKS < ceil_cluster, f"TKS {CEIL_TKS:.0f} < clusters {ceil_cluster:.0f} km/s")
check("E2-4  and the window CLOSES under two defensible alternative readings of the lensing gate: VSB's isolated-"
      "log scaling for 1e10 lenses (floor 820 > 537) and the deep a_b >= 1e-15 KiDS points (1340 > 537) -- so "
      "the surviving statement is a boundary-condition-dependent sliver, not a window",
      lo_vsb10 >= hi_primary and c_deep > hi_primary, f"VSB(1e10) floor {lo_vsb10:.0f}, deep floor {c_deep:.0f} vs ceiling {hi_primary:.0f}")

sec("E3 -- what is NOT decided (named, with the number that shows it is open)")
g300 = A['p1_growth_ratio']['300.0']; g537 = A['p1_growth_ratio']['537.0']
print(f"  LSS: dust growth today / CDM at k = 0.06, 0.1, 0.2, 0.5, 1.0 Mpc^-1:  c_ad = 300: " + ", ".join(f"{x:.3f}" for x in g300)
      + f";  537: " + ", ".join(f"{x:.3f}" for x in g537))
check("E3-1  inside the window the dust has lost its late-time power at k >= 0.5 Mpc^-1 entirely and half of it "
      "at k = 0.2 (300 km/s): the matter power spectrum at k >= 0.2 must then be carried by MOND-boosted "
      "baryons, a computation this lane does not do and L142 finds overshooting on its own -- OPEN, and it is "
      "the computation that would decide the sliver",
      abs(g300[3]) < 0.1 and g300[2] < 0.6, f"ratio(k=0.5) = {g300[3]:.3f}, ratio(k=0.2) = {g300[2]:.3f}")
check("E3-2  the repaired sector is Lorentz-invariant k-essence dust to the order computed (L153a A1-4/A2-4): "
      "it does not use the clock's foliation.  The transplant's distinctive structure -- the foliation-"
      "projected gradient with an independent coefficient -- is exactly the part that is dead.  What survives "
      "is not route 2; it is Scherrer-type k-essence with a constant ~300-540 km/s sound speed, which needs "
      "the O(w) PPN solve (L139 iii) no more than any minimally coupled scalar does",
      A['a_t_min_for_constant_cad'] >= 1.2, f"cosh turnover must sit at a_t >= {A['a_t_min_for_constant_cad']}")

print(f"""
  VERDICT
  -------
  1. L139's ROUTE 2 AS WRITTEN (L_dark = K(Q) - c_Y|D chi|^2, constant c_Y, the a^+3 sound speed of L138): DEAD.
     The identity c_s^2 = eps c_ad^2 (eps = 2 c_Y Qbar/K_Q, the ratio of inertial to gravitational response)
     means the running sound speed is a running equivalence-principle violation of (1+z_rec)^3 = 1.3e9 between
     recombination and today.  No c_s normalisation makes the sector cluster like CDM at z = 1100 AND fall
     normally today.  Binding conflict: 9 orders of magnitude.  This supersedes L138's 'nothing computed here
     excludes that corner' and L139's 'OPEN'.
  2. THE EP-CONSISTENT REPAIR (c_Y = K_Q/(2 Qbar); c_s = c_ad = const for cosh K with a_t >= 1.27): UNDETERMINED,
     with a knife-edge window  c_ad in [{lo_primary:.0f}, {hi_primary:.0f}] km/s  (c_s^2 in [{(lo_primary/C_KMS)**2:.1e}, {(hi_primary/C_KMS)**2:.1e}]):
       (a) CMB: carried by the constant-c_s GDM bound, ceiling 537 km/s;
       (b) dwarfs free (<1% of M_b), Milky-Way-class spirals clean, a0 unmoved on SPARC, for c_ad >= 170-175 km/s;
       (c) clusters keep their cosmic share for c_ad <= 700 km/s;
       (d) the Helmholtz regime sits at mu^-1 >= 7 Mpc, outside both ranges; the induced atmosphere's lensing
           deviation is <= 10% inside 1 Mpc for c_ad >= 300 km/s (isolated 1e11 lens, EFE-anchored potential).
     The window is EMPTY on VSB's isolated-log r_C scaling for 1e10 lenses and if the deep KiDS points are trusted.
     The interior is not cleared: the dust's late-time P(k) at k >= 0.2 Mpc^-1 is gone (E3-1), which only a
     baryon+MOND growth computation can adjudicate.
  3. The programme's ordering (dwarfs free, MW nearly free, clusters hold) IS achievable -- by an isothermal
     atmosphere at a constant temperature, exponentially sharp in v_f^2/c_ad^2 -- but not by the sector the
     programme proposed, and only inside a factor-1.8 sliver that two readings of the lensing data close.
""")
RES = dict(window_primary=[lo_primary, hi_primary], window_loose=[lo_loose, hi_primary],
           window_vsb_1e11=[lo_vsb11, hi_primary], window_vsb_1e10=[lo_vsb10, hi_primary], deep_lensing_floor=c_deep,
           floors=dict(template=floor_gal_template, sparc=floor_sparc, L61=floor_L61, lensing_iso_1e11=floor_wl_iso11,
                       lensing_loose=floor_wl_loose, vsb_1e11=floor_vsb_11, vsb_1e10=floor_vsb_10),
           ceilings=dict(cmb_TKS=CEIL_TKS, clusters=ceil_cluster), eps_span=A['eps_span'],
           checks_total=N[0], checks_failed=len(FAILS))
with open(os.path.join(HERE, "L153e_verdict.json"), "w") as f: json.dump(RES, f, indent=1, default=float)
print("=" * 112)
print(f"L153e COMPLETE: {N[0]-len(FAILS)}/{N[0]} checks PASS.   [{time.time()-T0:.1f}s]")
if FAILS: print("FAILED: " + "; ".join(FAILS)); sys.exit(1)
print("=" * 112)
