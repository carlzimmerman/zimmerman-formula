#!/usr/bin/env python3
"""
L151 -- THE COMPARISON: f_gal_max vs f_cmb_min on one axis.  GAP or OVERLAP?

Consumes the JSON written by
    L145_cmb_third_peak_floor.py   the CMB floor      (CAMB; profiled over A_s,n_s,omega_b,theta*,N_eff,Y_He;
                                                     noise model calibrated against Planck's published sigma(omega_c))
    L149_binding_constraint.py     the a0-collapse curve and the binding-constraint survey
    L150_halo_robustness.py             the galaxy ceiling for every halo-modelling variant
and does the decisive CROSS-EVALUATION: each constraint evaluated AT THE OTHER ONE'S optimum.  A ratio
of two f values understates the situation, because Delta chi^2 grows steeply -- so the CMB Delta chi^2
AT the galaxy ceiling is reported as the primary gap measure.

PASS = the printed statement is TRUE.
"""
import json, os, math, numpy as np

FAILS=[]; NCHK=0
def check(name, ok, detail=""):
    global NCHK; NCHK+=1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def P(s=""): print(s, flush=True)
def info(s): print("      "+s, flush=True)
def sec(t): P(); P("="*112); P(t); P("="*112)

HERE=os.path.dirname(os.path.abspath(__file__))
L145=json.load(open(os.path.join(HERE,"L145_cmb_results.json")))
L146=json.load(open(os.path.join(HERE,"L146_results.json")))   # N_eff profiled EXACTLY -- supersedes L145's
                                                            # N_eff-linearised floors (L145 guard G1 failed)
L149=json.load(open(os.path.join(HERE,"L149_results.json")))
L150=json.load(open(os.path.join(HERE,"L150_results.json")))
P("="*112); P("L151 -- GAP OR OVERLAP?"); P("="*112)

# ---------------- CMB floor ----------------
sec("THE CMB FLOOR  f_cmb_min  (minimum CLUSTERING fraction of omega_c = 0.1200, 3 sigma)")
fl=L145['floor']; fb=L146['floor']
info("N_eff is profiled EXACTLY here (L145's N_eff template failed its own linearity guard G1 at 16.8%,")
info("which made L145's N_eff-profiled floors too LENIENT).  Third-peak-only rows come from L145, whose")
info("peak-ratio statistic does not use the N_eff template at all.")
CMB=[("variant B (background pinned), TT+TE+EE  [the hybrid-relevant case]", fb['B_TT,TE,EE_3']),
     ("variant B, TT only",                                                  fb['B_TT_3']),
     ("variant B, THIRD PEAK HEIGHT RATIO alone",                            fl['B_PEAK3ONLY_3']),
     ("variant A (background also changes), TT+TE+EE",                       fb['A_TT,TE,EE_3']),
     ("variant A, TT only",                                                  fb['A_TT_3']),
     ("variant A, THIRD PEAK HEIGHT RATIO alone",                            fl['A_PEAK3ONLY_3'])]
P("")
for lab,v in CMB: P(f"    f_cmb_min = {v:7.4f}    {lab}")
F_CMB=fb['B_TT,TE,EE_3']; F_CMB_LEN=min(v for _,v in CMB if np.isfinite(v))
P("")
info(f"HEADLINE     f_cmb_min = {F_CMB:.3f}  ->  omega_c^clustering >= {F_CMB*0.1200:.4f}")
info(f"MOST LENIENT f_cmb_min = {F_CMB_LEN:.3f}  (weakest of all six variants/statistics)")

# ---------------- galaxy ceiling ----------------
sec("THE GALAXY CEILING  f_gal_max  (maximum CDM fraction galaxy dynamics tolerates, a0 refit throughout)")
P("")
P(f"  {'halo-modelling variant':>56} {'BTFR':>9} {'RAR':>9} {'ceiling':>9}")
fmt=lambda x: "none" if x is None else f"{x:.4f}"
for lab,v in L150.items():
    P(f"  {lab:>56} {fmt(v['btfr']):>9} {fmt(v['rar']):>9} {fmt(v['obs']):>9}")
KEY="AM / NFW / c(M) standard   [the CDM-appropriate case]"
F_GAL=L150[KEY]['obs']
AMv={k:v for k,v in L150.items() if k.startswith("AM")}
CSv={k:v for k,v in L150.items() if k.startswith("CS")}
F_GAL_LEN=max(v['obs'] for v in AMv.values() if v['obs'] is not None)
CS_UNBOUNDED=all(v['obs'] is None for v in CSv.values())
P("")
info(f"HEADLINE (cold matter distributed as cold dark matter is): f_gal_max = {F_GAL:.3f}")
info(f"MOST LENIENT mass-DEPENDENT variant:                       f_gal_max = {F_GAL_LEN:.3f}")
info(f"Mass-INDEPENDENT halo/baryon ratio:                        f_gal_max = "
     +("NO CEILING at any f<=1" if CS_UNBOUNDED else "bounded"))

# ---------------- cross-evaluation ----------------
sec("THE CROSS-EVALUATION -- each constraint evaluated AT THE OTHER ONE'S optimum")
rows=L145['rows']; xf=np.array([r['f'] for r in rows]); o=np.argsort(xf); xf=xf[o]
def cmb_dchi2(f,key='chi2all_B'):
    """Delta chi^2 at f.  Returns (value, clamped) -- clamped=True means f lies BELOW the lowest f at
    which that variant could be computed (CAMB cannot hold theta_star with so little matter in
    variant A), so the value is np.interp's clamp and is a LOWER BOUND on the true Delta chi^2."""
    y=np.array([r[key] for r in rows])[o]; g=np.isfinite(y)
    return float(np.interp(f,xf[g],y[g])), bool(f < xf[g].min())
def dchi2(f,key='chi2all_B'): return cmb_dchi2(f,key)[0]
def mark(f,key):
    v,c=cmb_dchi2(f,key); return f"{v:>8.0f}"+(" (>=)" if c else "     ")
a0c=L149['a0_curve']; ks=np.array(sorted(float(k) for k in a0c))
a0v=np.array([a0c[[k for k in a0c if float(k)==kk][0]][0] for kk in ks])
def a0_ratio(f): return float(np.interp(f,ks,a0v))/float(a0v[0])
P("")
P("  (a) AT THE GALAXY CEILING, how badly is the CMB broken?")
for lab,f in (("headline (CDM-appropriate)",F_GAL),("most lenient mass-dependent",F_GAL_LEN)):
    P(f"      f = {f:6.4f} ({lab:28s}):  CMB Delta chi^2 = {mark(f,'chi2all_B')} (variant B)"
      f"   {mark(f,'chi2all_A')} (variant A)")
info_pending=True
info("'(>=)' marks a value clamped at the lowest f that variant could be computed at: a LOWER BOUND.")
P("")
P("  (b) AT THE CMB FLOOR, what has happened to the galaxies?")
for lab,f in (("headline CMB floor",F_CMB),("most lenient CMB floor",F_CMB_LEN)):
    P(f"      f = {f:6.4f} ({lab:22s}):  best-fit a0 = {100*a0_ratio(f):5.2f}% of its measured value")

# ---------------- verdict ----------------
sec("THE VERDICT")
GAP_BEST=F_CMB/F_GAL; GAP_WORST=F_CMB_LEN/F_GAL_LEN
P("")
P(f"    BEST ESTIMATE   f_gal_max = {F_GAL:.3f}   vs   f_cmb_min = {F_CMB:.3f}     gap = {GAP_BEST:.1f}x")
P(f"    WORST CASE      f_gal_max = {F_GAL_LEN:.3f}   vs   f_cmb_min = {F_CMB_LEN:.3f}     gap = {GAP_WORST:.1f}x")
P("")
check("the two requirements do NOT overlap, even when BOTH sides are pushed to their most lenient "
      "settings simultaneously",
      F_GAL_LEN < F_CMB_LEN, f"{F_GAL_LEN:.3f} < {F_CMB_LEN:.3f}")
NARROW = GAP_WORST < 2.0
if NARROW:
    P("    *** WORST-CASE GAP IS UNDER A FACTOR OF 2 -- THE NO-GO IS NOT ROBUST ON THE f AXIS ***")
else:
    P(f"    worst-case gap is a factor of {GAP_WORST:.1f} on the f axis.")
info("BUT the f-ratio understates the separation, because the CMB Delta chi^2 rises steeply:")
info(f"even at the MOST LENIENT galaxy ceiling f = {F_GAL_LEN:.3f}, the CMB is broken by "
     f"Delta chi^2 = {dchi2(F_GAL_LEN):.0f} (variant B) / {dchi2(F_GAL_LEN,'chi2all_A'):.0f} (variant A).")
check("the separation is decisive in likelihood terms: at the most lenient galaxy ceiling the CMB is "
      "broken by Delta chi^2 > 100 even in the weakest CMB variant",
      dchi2(F_GAL_LEN,'chi2all_A')>100,
      f"variant A Delta chi^2 = {dchi2(F_GAL_LEN,'chi2all_A'):.0f}, variant B = {dchi2(F_GAL_LEN):.0f}")
check("at the CMB floor the modification is switched OFF rather than merely reduced: best-fit a0 "
      "below 10% of its measured value",
      a0_ratio(F_CMB)<0.10, f"a0 = {100*a0_ratio(F_CMB):.2f}% of measured at f = {F_CMB:.3f}")
check("THE ESCAPE IS REAL AND MUST BE STATED: if the cold component's galactic abundance is "
      "MASS-INDEPENDENT, no galaxy criterion bounds f at all and the gap closes",
      CS_UNBOUNDED, "CS variants place no ceiling up to f=1")

sec("THE THEOREM-SHAPED STATEMENT")
P(f"""
   Let f = omega_c^clustering / 0.1200 be the fraction of the Planck cold-dark-matter density carried
   by a genuinely cold, clustering component, the remainder of the gravitating background being
   supplied by the MOND completion's own fields.  Then, on Planck data and the SPARC rotation curves:

   (i)   CMB.  Holding the expansion history EXACTLY fixed (theta_star matched to 7 digits) and
         re-optimising A_s, n_s, omega_b, theta_star, N_eff and Y_He, the acoustic peaks require
                   f >= {F_CMB:.3f}   (3 sigma, TT+TE+EE);  f >= {fl['B_PEAK3ONLY_3']:.3f} on the third-peak height ratio alone.
         The weakest variant and statistic examined still gives f >= {F_CMB_LEN:.3f}.

   (ii)  GALAXIES.  With a0 refit at every f over a range that includes a0 -> 0, with per-galaxy
         stellar M/L freedom under the standard 0.11 dex prior, and with halo mass recomputed
         self-consistently, a cold component distributed as cold dark matter is (abundance matched,
         cuspy) tilts the baryonic Tully-Fisher relation beyond 3 sigma of its observed slope once
                   f > {F_GAL:.3f}  ({F_GAL_LEN:.3f} for the most permissive mass-dependent halo variant tested).

   (iii) THEREFORE no f satisfies both.  The gap is a factor of {GAP_BEST:.0f} on best estimates and
         {GAP_WORST:.1f} in the worst case; in likelihood terms the CMB is broken by Delta chi^2 ~ {dchi2(F_GAL_LEN):.0f}
         at the most lenient galaxy ceiling.  At the CMB's minimum f the best-fit a0 has fallen to
         {100*a0_ratio(F_CMB):.2f}% of its measured value: the modification is not reduced but switched OFF, and the
         surviving theory is plain LCDM.

   (iv)  THE ONE ASSUMPTION HOLDING THE GAP OPEN.  The galaxy bound bites through the MASS DEPENDENCE
         of the halo-to-baryon ratio, not its size.  If every galaxy instead carried the SAME multiple
         of its baryonic mass, refitting a0 absorbs the entire effect and NO galaxy criterion bounds f
         at any value up to 1 (verified in L150).  A viable hybrid must therefore supply cold matter
         that clusters at z ~ 1100 but whose z = 0 galactic abundance is mass-independent -- depleted
         from dwarf haloes by a factor of order 100 relative to abundance matching.  Collisionless
         cold matter has no known way to do that; it does not feel feedback.  That is the door these
         numbers leave open, and it is a DYNAMICAL question, not a parameter choice.
""")
json.dump(dict(F_GAL_MAX=F_GAL,F_GAL_MAX_LENIENT=F_GAL_LEN,F_CMB_MIN=F_CMB,F_CMB_MIN_LENIENT=F_CMB_LEN,
               gap_best=GAP_BEST,gap_worst=GAP_WORST,
               cmb_dchi2_at_gal_ceiling=dchi2(F_GAL_LEN),
               a0_frac_at_cmb_floor=a0_ratio(F_CMB),mass_independent_unbounded=CS_UNBOUNDED),
          open(os.path.join(HERE,"L151_verdict.json"),"w"),indent=1)
P(f"  checks: {NCHK-len(FAILS)}/{NCHK} passed"+("" if not FAILS else "   FAILED: "+"; ".join(FAILS)))
