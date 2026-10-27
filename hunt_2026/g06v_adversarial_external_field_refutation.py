#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g06v_adversarial_external_field_refutation.py -- ADVERSARIAL AUDIT of g06's load-bearing prescription claim.
=================================================================================================================
THE CLAIM UNDER ATTACK (g06_local_volume_groups_lambda_edge.py, section 4 / checks E1, E2, R4b):

  "The external field entering nu's argument must be the BARYONIC Newtonian field, not a LambdaCDM
   velocity-field reconstruction, and this rung's answer reverses if that is wrong."

  Supporting numbers: at the Local Group the direct baryonic sum gives g_N = 6.02e-15 m/s^2 = 6e-5 a_0; the
  2M++ reconstruction gives g = 1.161e-12 = 0.0124 a_0; inverting the reconstruction through nu(y) y a_0 = g
  gives g_N = 1.42e-14, so the two routes "agree to a factor 0.42" against a factor 193 raw.  Supporting
  cross-check offered: the baryonic field pushed through nu gives a Local Group peculiar velocity of 328 km/s
  against the CMB dipole's 620 km/s (the reconstruction gives 505 km/s), "so both are in the right decade and
  neither is a fit".

METHOD.  g06's own source is executed here (stdout suppressed) and its own objects -- groups, run(),
predict_sigma(), g_bary(), g_lss_lcdm(), qumond_invert() -- are used, so nothing is re-implemented and no
transcription error can be introduced.  Every number below is g06's own code, re-interrogated.

WHAT THIS FILE FOUND, in one line each (checks that FAIL are the findings):
  A1  the arithmetic is CORRECT and reproduces to the last digit.  The claim is not refuted on arithmetic.
  A2  the "supporting cross-check" is NOT independent: (g_B/g_N,inverted) is algebraically (nu(g_B)g_B/g_L)^2.
      The 328 vs 505 km/s comparison is E1's own ratio with a square root taken; it adds no evidence.
  A3  E1 passes by 6% of its own threshold and FAILS at Upsilon_K = 0.4, which is inside the bracket g06
      itself carries in its own systematics table.
  A4  the Local Group baryonic sum is a 145-degree near-cancellation of two comparable vectors, and the
      cancelling near-term is dominated by M31 -- which is INSIDE the Local Group, while the 2M++ comparison
      excludes everything within 3 Mpc/h = 4.45 Mpc.  The two sides of E1 are not the same volume.
  A5  the baryonic sum has an EMPTY SHELL from 3 to 5.36 Mpc (2MRS is cut at cz > 350 km/s, the UNGC is used
      only inside R_SEAM = 3 Mpc), and M81, Cen A, NGC 253, NGC 4945, NGC 4736, NGC 5236 all fall in the hole.
      This is a genuine estimator defect, but the 207 galaxies in the shell cancel down to 16% of the quoted
      sum, so the check PASSES and the defect is not a lever.  Recorded because it was looked for.
  A6  (FOR the claim) the 2MRS far-field normalisation is independently right to 20% against
      Omega_star+cold/Omega_m times the 2M++ total-matter field.  The stellar sum is not badly incomplete.
  A7  (FOR the claim) inside PURE-BARYON MOND the conclusion is robust: the Local Group's own 620 km/s caps
      the total baryonic g_N at ~3.6x the direct sum, which moves the median boost only to ~0.92.
  A8  THE REFUTATION.  The premise sentence "in this framework the actual matter is BARYONS" contradicts this
      repository's own STANDING.md item 5: "'No dark matter' is forfeited.  The framework HAS a dark sector --
      the AeST/ghost-condensate Q-mode ... MOND galaxies PLUS a no-particle CDM-like sector", with
      I_0 ~ Omega_dm recorded as robustly free and the 09-02 mu-pincer concluding "pressure cannot keep
      Omega_dm out of galaxies".  A CDM-like sector that clusters is a Newtonian source.  With it in the
      external field the rung lands in the cluster band, exactly as g06's own R4b warns.
  A9  the same 2M++ number is used with the OPPOSITE interpretation by the committed h81_h82 script, whose
      check 81a is built on reading it as the Newtonian field.  The repository holds both readings at once.

Both a_0 footings.  Mutation controls.  Checks can fail, and the load-bearing ones do.
"""
import sys, os, io, re, math, contextlib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import Check, P, info, A0, DATA, nu, nu_s, G, Msun, Mpc, H0, OM_M, OM_B, h as HLIT_LIB

ck = Check()
HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "g06_local_volume_groups_lambda_edge.py")

# ------------------------------------------------------------------ execute g06 and steal its own objects
P("="*126)
P("0.  RUN g06 ITSELF AND WORK ON ITS OWN OBJECTS (no re-implementation, so no transcription error)")
P("="*126)
Gm = {"__name__": "g06_under_audit", "__file__": SRC}
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        exec(compile(open(SRC).read(), SRC, "exec"), Gm)
except SystemExit as e:
    rc_g06 = e.code
info(f"g06 executed in-process, exit code {rc_g06} ({buf.getvalue().count('[FAIL]')} of its own checks FAIL)")

groups   = Gm["groups"];   run      = Gm["run"];      predict_sigma = Gm["predict_sigma"]
g_bary   = Gm["g_bary"];   g_lss    = Gm["g_lss_lcdm"]; qinv        = Gm["qumond_invert"]
gB, gL   = Gm["gB"],       Gm["gL"]
gNinv    = Gm["gN_from_lcdm"]
UPOS, UMB, UNM, UMD = Gm["UPOS"], Gm["UMB"], Gm["UNM"], Gm["UMD"]
T0, UPS_K, F_HOT = Gm["T0"], Gm["UPS_K"], Gm["F_HOT"]
a0c, a0a = A0["canonical"], A0["alt"]
med = lambda kw, a0=a0c: float(np.median([x["boost"] for x in run(a0, **kw)]))
MED_PRIMARY = {f: med({}, a) for f, a in A0.items()}
info(f"g06's primary median boost, recomputed here: canonical {MED_PRIMARY['canonical']:.3f}, "
     f"alt {MED_PRIMARY['alt']:.3f}")

# ================================================================================================ SECTION 1
P(""); P("="*126)
P("1.  THE ARITHMETIC.  Re-derive every number in the claim from scratch and demand it match")
P("="*126)
far0, near0 = g_bary(np.zeros(3), "MILKY WAY")
gB_re  = float(np.linalg.norm(far0 + near0))
gL_re  = float(np.linalg.norm(g_lss(np.zeros(3))))
# the QUMOND inversion, done analytically in the deep limit instead of by g06's bisection
gN_deep = gL_re**2/a0c                       # nu ~ 1/sqrt(y) => g = sqrt(gN a0) => gN = g^2/a0
info(f"    direct baryonic sum          g_N = {gB_re:.4e} m/s^2 = {gB_re/a0c:.6f} a_0   (claim 6.02e-15)")
info(f"    2M++ reconstruction          g   = {gL_re:.4e} m/s^2 = {gL_re/a0c:.6f} a_0   (claim 1.161e-12)")
info(f"    bisection inversion          g_N = {gNinv:.4e};  independent deep-limit g^2/a_0 = {gN_deep:.4e} "
     f"(differ by {100*abs(gN_deep/gNinv-1):.1f}%, the exact-vs-deep kernel correction)")
info(f"    ratio g_B/g_N,inv = {gB_re/gNinv:.4f}   (claim 0.42);   raw factor g_L/g_B = {gL_re/gB_re:.1f} "
     f"(claim 193)")
ck("A1 the arithmetic of the claim is CORRECT.  The bisection inverts the kernel properly, the linear-theory "
   "reduction v = 2 f g/(3 H_0 Omega_m) is applied consistently (the growth rate cancels between the velocity "
   "prediction and the conversion back to g), and every quoted number reproduces.  If this failed the claim "
   "would die here on arithmetic; it does not, so the attack has to be on the ESTIMATOR and the PREMISE",
   abs(gB_re/6.024e-15 - 1) < 0.01 and abs(gL_re/1.161e-12 - 1) < 0.01
   and abs((gB_re/gNinv)/0.424 - 1) < 0.01 and abs(gN_deep/gNinv - 1) < 0.05,
   f"g_B {gB_re:.4e}, g_L {gL_re:.4e}, ratio {gB_re/gNinv:.4f}, deep-limit inversion agrees to "
   f"{100*abs(gN_deep/gNinv-1):.1f}%")

# ================================================================================================ SECTION 2
P(""); P("="*126)
P("2.  THE 'SUPPORTING CROSS-CHECK' IS THE SAME NUMBER.  620 km/s adds nothing that E1 did not already say")
P("="*126)
v_bar  = nu_s(gB_re/a0c)*gB_re*T0/1e3
v_lcdm = gL_re*T0/1e3
info(f"    baryons through nu, v ~ g t_0 : {v_bar:.0f} km/s        (g06 prints 328)")
info(f"    2M++ field, v ~ g t_0         : {v_lcdm:.0f} km/s        (g06 prints 505)")
info(f"    CMB dipole (Local Group)      : 620 km/s   (Planck 2018 VI / Kogut+1993)")
identity = (nu_s(gB_re/a0c)*gB_re/gL_re)**2
info(f"    but in the deep limit g_N = g_MOND^2/a_0 EXACTLY, so   (nu(g_B) g_B / g_L)^2 = {identity:.4f}")
info(f"    and E1's ratio                                          g_B / g_N,inv       = {gB_re/gNinv:.4f}")
ck("A2 the velocity cross-check offered in support of E1 is NOT independent of E1.  Because the kernel is deep "
   "at these accelerations, g_N = g_MOND^2/a_0 exactly, so the ratio of the two ROUTES' Newtonian fields is the "
   "SQUARE of the ratio of their predicted velocities.  Quoting 328 vs 505 km/s beside a ratio of 0.42 is "
   "quoting one number twice.  This check asserts the two are independent (differ by more than 5%), and it "
   "fails.  What the velocities DO add is a comparison against 620 km/s -- and there the baryonic route is "
   "1.9x short while the reconstruction is 1.2x short, so that comparison mildly favours the reconstruction's "
   "normalisation, not the baryonic sum's",
   abs(identity/(gB_re/gNinv) - 1) > 0.05,
   f"(nu(g_B)g_B/g_L)^2 = {identity:.4f} against E1's g_B/g_N,inv = {gB_re/gNinv:.4f} -- the same quantity to "
   f"{100*abs(identity/(gB_re/gNinv)-1):.1f}%.  Against the 620 km/s dipole: baryons {620/v_bar:.2f}x short, "
   f"reconstruction {620/v_lcdm:.2f}x short")

# ================================================================================================ SECTION 3
P(""); P("="*126)
P("3.  E1 IS KNIFE-EDGE, AND IT FAILS INSIDE g06'S OWN STELLAR M/L BRACKET")
P("="*126)
P(f"    {'Upsilon_K':>10} {'g_B (m/s^2)':>13} {'g_B/g_N,inv':>13} {'E1 (0.4 - 2.5)':>16}")
e1 = {}
for u in (0.4, 0.5, 0.6, 0.8, 1.0):
    gb = gB_re*u/UPS_K; r = gb/gNinv; e1[u] = r
    P(f"    {u:10.1f} {gb:13.3e} {r:13.4f} {('PASS' if 0.4 < r < 2.5 else 'FAIL'):>16}")
info("(Upsilon_K scales the stellar mass in BOTH the 2MRS far term and the UNGC near term, so this is the")
info(" honest one-parameter sensitivity of E1 to the single largest systematic g06 itself carries.)")
ck("A3 E1 -- the check the whole rung is declared to rest on -- passes by 6% of its own threshold and FAILS at "
   "Upsilon_K = 0.4, which is not an invented value but the LOW END OF THE BRACKET g06 CARRIES IN ITS OWN "
   "SYSTEMATICS TABLE (where it is shown to move the median boost to 1.011).  A load-bearing check must survive "
   "the file's own declared systematics.  This asserts that; it fails",
   all(0.4 < e1[u] < 2.5 for u in (0.4, 0.6, 1.0)),
   f"Upsilon_K = 0.4 gives ratio {e1[0.4]:.3f} (E1 FAILS), 0.6 gives {e1[0.6]:.3f} (PASS, by "
   f"{100*(e1[0.6]/0.4-1):.0f}% of the threshold), 1.0 gives {e1[1.0]:.3f} (PASS)")

# ================================================================================================ SECTION 4
P(""); P("="*126)
P("4.  THE ESTIMATOR: the Local Group number is a near-cancellation, and the two sides of E1 are not the")
P("    same volume")
P("="*126)
cosang = float(np.dot(far0, near0)/(np.linalg.norm(far0)*np.linalg.norm(near0)))
def galdir(v):
    u = v/np.linalg.norm(v)
    return math.degrees(math.atan2(u[1], u[0])) % 360.0, math.degrees(math.asin(u[2]))
lf, bf = galdir(far0); ln, bn = galdir(near0)
info(f"    far term  (2MRS, r > 3 Mpc)  |g| = {np.linalg.norm(far0):.4e} toward (l, b) = ({lf:.0f}, {bf:+.0f})")
info(f"    near term (UNGC, r < 3 Mpc)  |g| = {np.linalg.norm(near0):.4e} toward (l, b) = ({ln:.0f}, {bn:+.0f})")
info(f"    the two are {math.degrees(math.acos(cosang)):.0f} degrees apart and nearly equal in size, so the "
     f"quoted sum {gB_re:.3e} is {np.linalg.norm(far0)/gB_re:.2f}x SMALLER than either term")
rr = np.linalg.norm(UPOS, axis=1)
big = sorted([(UNM[i], UMB[i], rr[i]) for i in range(len(UNM)) if rr[i] < 3.0 and UNM[i] != "MILKY WAY"
              and UMD[i] != "MILKY WAY"], key=lambda t: -t[1]/max(t[2], 0.15)**2)[:4]
info( "    the near term's largest contributors, by g = G M / r^2:")
for nm, mb, r in big:
    info(f"        {nm:14} M_b = {mb:.2e} Msun at {r:.2f} Mpc  ->  g = "
         f"{G*mb*Msun/(max(r,0.15)*Mpc)**2:.3e} m/s^2")
info( "    M31 is INSIDE the Local Group.  It does not source the Local Group barycentre's motion, and the")
info( "    2M++ side of the comparison excludes everything within 3 Mpc/h = 4.45 Mpc.  So E1 compares a sum")
info( "    that includes Local Group members against a reconstruction that excludes them.")
r_far_only = np.linalg.norm(far0)/gNinv
v_far_only = nu_s(np.linalg.norm(far0)/a0c)*np.linalg.norm(far0)*T0/1e3
info(f"    dropping the near term (the volume-matched comparison): ratio = {r_far_only:.3f} instead of "
     f"{gB_re/gNinv:.3f}, and the predicted Local Group velocity rises to {v_far_only:.0f} km/s")
ck("A4 the two sides of E1 are volume-matched.  They are not: the baryonic sum runs from 0 Mpc outward and is "
   "half-cancelled by an M31-dominated near term that lies INSIDE the Local Group, while the 2M++ side is cut "
   "at 3 Mpc/h.  This check asserts the quoted sum is not dominated by that cancellation -- that dropping the "
   "unmatched near term moves the ratio by less than 20%.  It fails.  NOTE THE DIRECTION: the volume-matched "
   "number is BETTER for the claim, so this is an error in g06's own disfavour",
   abs(r_far_only/(gB_re/gNinv) - 1) < 0.20,
   f"as quoted {gB_re/gNinv:.3f}; volume-matched (far term only) {r_far_only:.3f}, a factor "
   f"{r_far_only/(gB_re/gNinv):.2f}; the two terms cancel at "
   f"{math.degrees(math.acos(cosang)):.0f} degrees")

# ---- the empty shell
cz2 = Gm["cz2"]; H0_KMS = Gm["H0_KMS"]; R_SEAM = Gm["R_SEAM"]
dmin2 = float((cz2[(cz2 > 350) & (cz2 < 15000)]/H0_KMS).min())
shell = (rr > R_SEAM) & (rr < dmin2)
g_shell = (G*Msun/Mpc**2)*np.sum((UMB[shell]/rr[shell]**3)[:, None]*UPOS[shell], axis=0)
info("")
info(f"    2MRS is cut at cz > 350 km/s, i.e. d > {dmin2:.2f} Mpc; the UNGC is used only inside "
     f"R_SEAM = {R_SEAM:.1f} Mpc.")
info(f"    So the shell {R_SEAM:.1f} - {dmin2:.2f} Mpc contributes NOTHING to the baryonic external field, and "
     f"it holds {int(shell.sum())} UNGC galaxies")
info(f"    (M81 3.63, NGC 5128 3.75, NGC 4945 3.80, NGC 253 3.94, NGC 4736 4.66, NGC 5236 4.92 Mpc all sit in "
     f"the hole).")
info(f"    Their summed vector field at the Local Group is {np.linalg.norm(g_shell):.3e} m/s^2, i.e. "
     f"{np.linalg.norm(g_shell)/gB_re:.2f}x the quoted total.")
ck("A5 (ATTACK ATTEMPTED, ATTACK FAILED -- reported anyway) the baryonic external field has a real gap in its "
   "radial coverage: a 3.00 - 5.36 Mpc shell is sampled by neither catalogue, and it contains M81, Cen A, "
   "NGC 253, NGC 4945, NGC 4736 and NGC 5236.  This check asserts the gap is worth less than 30% of the quoted "
   "total, i.e. that it does not matter.  It PASSES: 207 galaxies spread over the sky largely cancel, and the "
   "residual is 16%.  So the gap is a defect in the estimator but not a lever on the answer, and filling it "
   "would in any case RAISE the baryonic field and move E1 toward agreement",
   np.linalg.norm(g_shell)/gB_re < 0.30,
   f"{int(shell.sum())} UNGC galaxies in the unsampled 3.00 - {dmin2:.2f} Mpc shell contribute "
   f"{np.linalg.norm(g_shell):.3e} m/s^2 = {np.linalg.norm(g_shell)/gB_re:.2f}x the quoted "
   f"{gB_re:.3e}")

# ================================================================================================ SECTION 5
P(""); P("="*126)
P("5.  AN INDEPENDENT NORMALISATION OF THE FAR TERM -- and it is FOR the claim, not against it")
P("="*126)
OM_STAR = 0.0027 + 0.0007   # Fukugita & Peebles 2004 (ApJ 616, 643): stars ~0.0027, cold gas ~0.0007
info(f"If light traced mass, the Newtonian field of stars-plus-cold-gas would be Omega_(*+cold)/Omega_m times")
info(f"the total-matter field the 2M++ reconstruction returns.  Fukugita & Peebles 2004 give "
     f"Omega_(*+cold) = {OM_STAR:.4f};")
g_pred_far = OM_STAR/OM_M*gL_re
info(f"Omega_m = {OM_M:.3f} here, so that is {OM_STAR/OM_M:.4f} x {gL_re:.3e} = {g_pred_far:.3e} m/s^2, "
     f"against the 2MRS sum's {np.linalg.norm(far0):.3e}.")
ck("A6 (THIS ONE SUPPORTS THE CLAIM, and is checked as hard as the ones that do not) the 2MRS far-field sum is "
   "independently normalised.  Its magnitude is predicted to 20% by the cosmic stellar-plus-cold-gas density "
   "fraction times the 2M++ total-matter field.  So the magnitude-limited 2MRS sum is NOT badly incomplete for "
   "this purpose, and g06's 'lower bound, a threefold error is possible' caveat is if anything too generous to "
   "its critics.  The disagreement between the two routes is therefore NOT a data-quality problem; it is "
   "exactly the Omega_(*+cold)/Omega_m ratio, which is the real question",
   0.5 < np.linalg.norm(far0)/g_pred_far < 2.0,
   f"2MRS sum {np.linalg.norm(far0):.3e} vs Omega_(*+cold)/Omega_m x 2M++ = {g_pred_far:.3e}, ratio "
   f"{np.linalg.norm(far0)/g_pred_far:.2f}")

# ================================================================================================ SECTION 6
P(""); P("="*126)
P("6.  HOW BIG MUST THE EXTERNAL FIELD BE BEFORE THE RUNG'S ANSWER ACTUALLY REVERSES?")
P("="*126)
info("g06 shows two points -- x1 (boost 0.817) and x3 (0.909) -- and the raw reconstruction (2.215).  The")
info("interesting question is the curve between them, because the candidate corrections are not factors of 3.")
P(f"    {'g_ext multiplier':>17} {'median e_N/a_0':>15} {'boost canonical':>16} {'boost alt':>11} "
  f"{'in cluster band?':>17}")
CURVE = {}
for mult in (1.0, 3.0, 6.4, 10.0, 14.5, 30.0, 60.0, 100.0, 193.0):
    bc = med(dict(gext_mult=mult)); ba = med(dict(gext_mult=mult), a0a)
    en = float(np.median([g["gext"]*mult/a0c for g in groups]))
    CURVE[mult] = bc
    P(f"    {mult:17.1f} {en:15.5f} {bc:16.3f} {ba:11.3f} {('YES' if bc >= 1.45 else 'no'):>17}")
flip = min([m for m in CURVE if CURVE[m] >= 1.45], default=None)
info(f"the median boost first enters the liability table's cluster/group band (>= 1.45) at a multiplier of "
     f"about {flip:.0f} on the baryonic external field")
info(f"and reaches g06's own R1 threshold of 1.8 between "
     f"{max([m for m in CURVE if CURVE[m] < 1.8]):.0f}x and "
     f"{min([m for m in CURVE if CURVE[m] >= 1.8], default=float('nan')):.0f}x")

# ---- the pure-baryon ceiling, set by the Local Group's own motion
lo, hi = 1e-18, 1e-10
for _ in range(200):
    mid = math.sqrt(lo*hi)
    if nu_s(mid/a0c)*mid*T0/1e3 < 620.0: lo = mid
    else: hi = mid
gN_dipole = math.sqrt(lo*hi)
mult_dip = gN_dipole/gB_re
info("")
info(f"PURE-BARYON CEILING.  If ALL baryons (not just stars and cold gas) source the field, how large can the")
info(f"baryonic g_N be before the framework over-predicts the Local Group's own 620 km/s?  Solving")
info(f"nu(g_N/a_0) g_N t_0 = 620 km/s gives g_N = {gN_dipole:.3e} = {gN_dipole/a0c:.5f} a_0, i.e. "
     f"{mult_dip:.1f}x the direct sum,")
info(f"which is a median boost of {med(dict(gext_mult=mult_dip)):.3f} canonical / "
     f"{med(dict(gext_mult=mult_dip), a0a):.3f} alt.")
info(f"(For contrast: if all baryons traced the 2M++ structure, Omega_b/Omega_m = {OM_B/OM_M:.3f} x "
     f"{gL_re:.3e} = {OM_B/OM_M*gL_re:.3e} = {OM_B/OM_M*gL_re/gB_re:.0f}x the direct sum, which the 620 km/s")
info(f" dipole EXCLUDES -- it would predict "
     f"{nu_s(OM_B/OM_M*gL_re/a0c)*OM_B/OM_M*gL_re*T0/1e3:.0f} km/s.  That over-prediction of bulk flows by")
info(f" MOND is a known separate liability and is not this rung's problem.)")
ck("A7 (ALSO FOR THE CLAIM) inside a strictly baryons-only reading the conclusion is ROBUST.  The Local Group's "
   "own measured 620 km/s caps the baryonic Newtonian field at a few times the direct sum, and at that cap the "
   "median boost is still far under the cluster band.  So no plausible error in COUNTING BARYONS reverses this "
   "rung.  This is the strongest thing that can be said for the claim and it is said here",
   med(dict(gext_mult=mult_dip)) < 1.45 and med(dict(gext_mult=mult_dip), a0a) < 1.45,
   f"at the dipole cap ({mult_dip:.1f}x the direct sum) the median boost is "
   f"{med(dict(gext_mult=mult_dip)):.3f} canonical / {med(dict(gext_mult=mult_dip), a0a):.3f} alt, against the "
   f"cluster band's 1.45")

# ================================================================================================ SECTION 7
P(""); P("="*126)
P("7.  THE REFUTATION: the premise 'in this framework the actual matter is BARYONS' is not this repository's")
P("    own standing")
P("="*126)
info("g06 section 4, verbatim: 'In QUMOND the external-field parameter is e_N = |g_N,ext|/a_0 where g_N,ext is")
info("the NEWTONIAN field sourced by the actual matter.  In this framework the actual matter is BARYONS.'")
info("")
info("STANDING.md, section 5 item 5, verbatim: \"'No dark matter' is forfeited.  The framework *has* a dark")
info("sector -- the AeST/ghost-condensate Q-mode, a gravity mode rather than a particle.  Honest framing:")
info("MOND galaxies **plus** a no-particle CDM-like sector.\"")
info("STANDING.md line 423: 'I_0 ~ Omega_dm is recorded as robustly free'.")
info("STANDING.md item 3 (the 09-02 mu-pincer): 'pressure cannot keep Omega_dm out of galaxies.'")
info("")
info("A CDM-like sector that clusters is a NEWTONIAN SOURCE.  If the framework's relativistic completion")
info("carries it -- and the repository's own standing says it does, at ~Omega_dm -- then the Newtonian field")
info("external to a Local Volume group is sourced by baryons PLUS that sector, which is what a LambdaCDM")
info("velocity-field reconstruction returns.  On that reading g06's 'wrong, shown' branch is the right one.")
txt = re.sub(r"\s+", " ", open(os.path.join(HERE, "..", "STANDING.md"), encoding="utf-8").read())
has_forfeit = ('"No dark matter" is forfeited' in txt and "AeST/ghost-condensate Q-mode" in txt
               and "no-particle CDM-like sector" in txt)
b_raw  = med(dict(gext_key="gext_lcdm"))
b_rawa = med(dict(gext_key="gext_lcdm"), a0a)
b_omb  = med(dict(gext_key="gext_lcdm", gext_mult=float(OM_B/OM_M)))
info("")
info(f"    external field = baryons only (g06 primary) ................ boost "
     f"{MED_PRIMARY['canonical']:.3f} / {MED_PRIMARY['alt']:.3f}")
info(f"    external field = total matter (2M++ raw, the dark-sector")
info(f"      reading, which is g06's own R4b branch) .................. boost {b_raw:.3f} / {b_rawa:.3f}")
info(f"    external field = 2M++ scaled by Omega_b/Omega_m (a sanity")
info(f"      intermediate, no dark sector but all baryons) ............ boost {b_omb:.3f}")
ck("A8 THE LOAD-BEARING PREMISE HOLDS.  It does not.  The claim's first half -- that nu's argument takes the "
   "Newtonian field of the actual matter -- is correct QUMOND and is not in dispute.  Its second half -- that "
   "the actual matter is BARYONS -- is contradicted by this repository's own STANDING.md, which forfeits 'no "
   "dark matter' and records a CDM-like ghost-condensate Q-mode at ~Omega_dm that the mu-pincer says cannot be "
   "kept out of galaxies.  With that sector sourcing the external field the rung lands at a median boost of "
   f"{b_raw:.2f}, inside the cluster band -- which is g06's own R4b, the check it already fails on purpose.  So "
   "the rung's answer is CONDITIONAL on a premise the repository has already retracted, and 'the answer "
   "reverses if that is wrong' is not a hypothetical here",
   not has_forfeit,
   f"STANDING.md item 5 forfeits 'no dark matter' and names the AeST/ghost-condensate Q-mode: found in "
   f"STANDING.md = {has_forfeit}.  Baryons-only boost {MED_PRIMARY['canonical']:.3f}; total-matter external "
   f"field {b_raw:.3f} canonical / {b_rawa:.3f} alt, i.e. {math.log10(b_raw/MED_PRIMARY['canonical']):+.3f} dex "
   f"and inside the 1.45-3.45 cluster band")

# ---- the repository holds both readings at once
h81 = open(os.path.join(HERE, "h81_h82_mw_external_fields.py"), encoding="utf-8").read()
h81_newtonian = ("the NEWTONIAN large-scale field at the Local Group is g" in h81
                 and "1.5*H0*OM_M*(v1*1e3)/B_2MPP" in h81)
ck("A9 the repository is self-consistent about which quantity the 2M++ reduction returns.  It is not: the "
   "committed h81_h82_mw_external_fields.py computes the IDENTICAL expression and calls it 'the NEWTONIAN "
   "large-scale field at the Local Group', and its check 81a is built on that reading ('in the Newtonian units "
   "the EFE actually uses, large-scale structure beats the LMC by about an order of magnitude').  g06 calls the "
   "same expression a MOND field.  Both are committed; they cannot both stand",
   not h81_newtonian,
   f"h81_h82 uses the same reduction and labels it Newtonian: {h81_newtonian}.  Under h81's reading e_N at the "
   f"Local Group is {gL_re/a0c:.4f} a_0; under g06's it is {gB_re/a0c:.5f} a_0, a factor {gL_re/gB_re:.0f}")

# ================================================================================================ SECTION 8
P(""); P("="*126)
P("8.  MUTATION CONTROLS ON THIS AUDIT")
P("="*126)
b_zero = med(dict(gext_mult=0.0))
ck("V-M1 mutation -- set the external field to exactly zero.  If the external field were doing the work "
   "attributed to it, this must move the answer; if the sensitivity curve of section 6 were an artefact of the "
   "gext_mult plumbing, zero would not sit at the isolated-branch value g06 already prints (0.706)",
   abs(b_zero - 0.706) < 0.02, f"gext_mult = 0 gives {b_zero:.3f}, against g06's independently computed "
   f"isolated branch 0.706")
mono = [CURVE[m] for m in sorted(CURVE)]
ck("V-M2 the boost must rise monotonically with the external field, because a larger e_N pushes nu toward 1 and "
   "shrinks the predicted dispersion.  A non-monotone curve would mean the gext plumbing or the EFE branch is "
   "doing something other than advertised",
   all(mono[i] <= mono[i+1] + 1e-9 for i in range(len(mono)-1)),
   f"boosts across multipliers 1 -> 193: {', '.join(f'{v:.2f}' for v in mono)}")
gr = np.linalg.norm(g_lss(np.array([3.0, 4.0, 5.0])))
ck("V-M3 mutation -- evaluate the 2M++ field somewhere other than the origin.  If g_lss_lcdm returned a "
   "position-independent constant (a plumbing bug), the whole R4b branch would be meaningless",
   abs(gr/gL_re - 1) > 0.05, f"|g| at the origin {gL_re:.3e}, at (3, 4, 5) Mpc {gr:.3e}, ratio {gr/gL_re:.3f}")
ck("V-M4 both footings throughout: every boost in section 6 was computed on both a_0 and the verdict does not "
   "turn on the choice",
   abs(math.log10(b_raw/b_rawa)) < 0.15,
   f"total-matter external field gives {b_raw:.3f} canonical / {b_rawa:.3f} alt, "
   f"{math.log10(b_raw/b_rawa):+.3f} dex apart")

# ================================================================================================ SECTION 9
P(""); P("="*126)
P("9.  VERDICT")
P("="*126)
info("WHAT SURVIVES THE ATTACK")
info("  * The arithmetic.  Every number in the claim reproduces (A1), the kernel inversion is right, and the")
info("    linear-theory reduction is applied consistently.  No bug was found in the computation.")
info("  * The 2MRS baryon sum's normalisation, independently confirmed to 20% (A6).")
info("  * The claim's structural half: QUMOND's nu takes the Newtonian field of the actual matter.  True.")
info("  * The robustness of the rung to any error in COUNTING BARYONS: the Local Group's own 620 km/s caps")
info(f"    that at {mult_dip:.1f}x and the boost only reaches {med(dict(gext_mult=mult_dip)):.2f} (A7).")
info("")
info("WHAT DOES NOT")
info("  * The premise that the framework's matter is baryons (A8).  STANDING.md forfeits 'no dark matter' and")
info("    carries a CDM-like Q-mode at ~Omega_dm.  With it, the external field IS the total-matter field, the")
info(f"    rung reads {b_raw:.2f}, and the claim's own escape clause -- 'this rung's answer reverses if that is")
info("    wrong' -- is triggered by the repository's own standing rather than by a hypothetical.")
info("  * The evidence offered for the premise.  E1 fails inside g06's own Upsilon_K bracket (A3); its")
info("    supporting velocity cross-check is E1 restated (A2); and the compared volumes do not match (A4, A5).")
info("  * Repository self-consistency: h81_h82 reads the same number the opposite way (A9).")
info("")
info("WHAT THIS DOES NOT SHOW.  It does not show the baryonic reading is WRONG -- if the Q-mode is smooth on")
info("4-200 Mpc scales, or if I_0 is small, the baryonic reading is right and the rung stands at 0.82.  It")
info("shows the rung is CONDITIONAL on an unsettled premise that the repository has already retracted in the")
info("other direction, and that the conditionality is a factor 2.7 in the answer -- the difference between")
info("'groups do not look like clusters' and 'groups look exactly like clusters'.")
sys.exit(ck.done())
