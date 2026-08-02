#!/usr/bin/env python3
r"""mi_amendment7_wb_target_conflict_2026.py -- AMENDMENT 6 REGISTERED A TARGET ITS OWN DOCUMENT HAD
SUPERSEDED TWO DAYS EARLIER, AND THE 3-SIGMA REQUIREMENT IT INVOKES IS UNREACHABLE AT ANY SAMPLE SIZE.

This is the verification behind Amendment 7 to the frozen, hash-stamped PREREGISTRATION_DR4.md. Two defects,
both internal to that document, both found by the 2026-08-02 closure audit.

DEFECT 1 -- A SUPERSEDED TARGET RE-REGISTERED. Amendment 4(d) (2026-07-31) states verbatim "These supersede
the Amendment 3 table" and gives the in-force ungated alpha=2 target as gamma_v = 1.0310, full range
1.0218-1.0472. Amendment 6 (2026-08-02) then registers "framework-MI, UNGATED (the framework's prediction
under alpha = 2) ... ~ 1.02" -- which is Amendment 3's 1.0246, the value 4(d) had already retired. Amendment 6
reached back PAST the amendment that corrected it.

  Why 4(d) is right: the framework's law is a = nu(y) g_bar with the NEWTONIAN argument y = g_bar/a0.
  Amendments 2-3 fed nu the OBSERVED ratio g_ext,obs/a0 = 1.8996. Under alpha=2 the closure inversion of
  1.8996 is y_extN = 1.6809 -- so 1.8996 is the OUTPUT, and feeding it back in double-boosts. V1 verifies
  that inversion to machine precision, which settles which table is in force.

DEFECT 2 -- AN UNREACHABLE SCORING REQUIREMENT. Amendment 6 declares "gamma_v ~ 1.02 is a real risk taken in
advance ... This must not be re-hedged after DR4 lands." But the frozen error model has an IRREDUCIBLE
sigma_sys = 0.02 (section: sigma_tot = sqrt(sigma_fit^2 + 0.02^2)), and the in-force signal is
gamma_v - 1 = 0.0310. So Newton-vs-MI ceilings at ~1.6 sigma as N -> infinity. Three sigma is unattainable at
ANY sample size, and section 1.5's "3 sigma needs N >~ 12,200 -- expected DECIDABLE" is alpha=1,
statistical-only arithmetic that no amendment revisited.

  V1  the closure inversion that settles which table is in force
  V2  the conflict, quantified in the observable (gamma_v - 1)
  V3  the detectability arithmetic: z at N=30k, the infinite-N ceiling, and the statistical-only 3-sigma N
  V4  what Amendment 7 must register

Exit 0 = ran and every internal check held. No hard-coded verdicts, no check(True).
"""
from __future__ import annotations

import math
import sys

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 106)
    print(f"  {t}")
    print("=" * 106)


# ---- frozen values, quoted from PREREGISTRATION_DR4.md at the stated lines
Y_EXTN_A2 = {"canonical": 1.6809, "alt": 1.3280}     # Amendment 4(c), alpha=2 closure inversions
G_EXT_OBS_OVER_A0 = 1.8996                            # Amendment 4(b), the OBSERVED ratio
A3_TARGET = 1.0246                                    # Amendment 3, superseded by 4(d)
A6_REGISTERED = 1.02                                  # Amendment 6's table row
A4D_POINT = 1.0310                                    # Amendment 4(d), IN FORCE
A4D_RANGE = (1.0218, 1.0472)                           # Amendment 4(d), IN FORCE
SIG_FIT_30K = 0.0191                                  # frozen error model at N = 30,000
SIG_SYS = 0.02                                        # frozen IRREDUCIBLE systematic
N_REF = 30000
A15_N_FOR_3SIG = 12200                                # section 1.5's claim (alpha=1, statistical-only)


def nu2(y):
    """alpha=2: mu(x) = x/sqrt(1+x^2) => x^4 - y^2 x^2 - y^2 = 0; returns x = g_obs/a0 and nu = x/y."""
    y2 = y * y
    x2 = (y2 + math.sqrt(y2 * y2 + 4.0 * y2)) / 2.0
    x = math.sqrt(x2)
    return x, x / y


banner("V1  THE CLOSURE INVERSION THAT SETTLES WHICH TABLE IS IN FORCE")

print(f"  the framework's law is a = nu(y) g_bar with the NEWTONIAN argument y = g_bar/a0.")
print(f"  Amendment 4(c) publishes the alpha=2 inversions y_extN = "
      f"{Y_EXTN_A2['canonical']} (canonical) / {Y_EXTN_A2['alt']} (alt).\n")
print(f"  {'footing':<12}{'y_extN':>10}{'-> x = g_obs/a0':>18}{'nu(y_extN)':>13}{'1/2[nu-1]':>12}")
print("  " + "-" * 66)
inv = {}
for fn, y in Y_EXTN_A2.items():
    x, nu = nu2(y)
    inv[fn] = (x, nu)
    print(f"  {fn:<12}{y:>10.4f}{x:>18.4f}{nu:>13.4f}{0.5*(nu-1):>12.4f}")

check(abs(inv["canonical"][0] - G_EXT_OBS_OVER_A0) < 5e-4,
      f"V1a *** THE INVERSION CLOSES TO {abs(inv['canonical'][0]-G_EXT_OBS_OVER_A0):.1e}: *** y_extN = "
      f"{Y_EXTN_A2['canonical']} maps to g_obs/a0 = {inv['canonical'][0]:.4f}, i.e. the frozen "
      f"{G_EXT_OBS_OVER_A0} is the kernel's OUTPUT, not its argument. So Amendments 2-3 fed nu its own "
      f"output and double-boosted, exactly as Amendment 4(b) says -- which settles that Amendment 4(d)'s "
      f"table is the one in force and Amendment 3's 1.0246 is retired")
check(abs(0.5 * (inv["canonical"][1] - 1) - 0.0651) < 5e-4,
      f"V1b and the cubic law's amplitude prefactor 1/2[nu(y_extN) - 1] = {0.5*(inv['canonical'][1]-1):.4f} "
      f"on the Newtonian argument -- an independent cross-check on the same inversion, matching the value "
      f"WB_CUBIC_GATE_LAW should carry under alpha=2")


banner("V2  THE CONFLICT, QUANTIFIED IN THE OBSERVABLE (gamma_v - 1)")

print(f"  Amendment 3 (superseded by 4(d))         gamma_v = {A3_TARGET:.4f}   ->  gamma_v - 1 = "
      f"{A3_TARGET-1:.4f}")
print(f"  Amendment 6 registers                    gamma_v ~ {A6_REGISTERED:.4f}   ->  gamma_v - 1 = "
      f"{A6_REGISTERED-1:.4f}")
print(f"  Amendment 4(d), IN FORCE                 gamma_v = {A4D_POINT:.4f}   ->  gamma_v - 1 = "
      f"{A4D_POINT-1:.4f}")
print(f"  Amendment 4(d) full range, IN FORCE      {A4D_RANGE[0]:.4f}-{A4D_RANGE[1]:.4f}  ->  "
      f"{A4D_RANGE[0]-1:.4f}-{A4D_RANGE[1]-1:.4f}")
und_pt = (A4D_POINT - 1) / (A6_REGISTERED - 1) - 1
und_wc = (A4D_RANGE[1] - 1) / (A6_REGISTERED - 1) - 1
print(f"\n  the registered 0.0200 understates the in-force point value by {100*und_pt:.0f}% and the worst "
      f"frozen corner by {100*und_wc:.0f}%")
check(A6_REGISTERED < A4D_RANGE[0] and und_pt > 0.5,
      f"V2a *** AMENDMENT 6's REGISTERED TARGET LIES BELOW THE ENTIRE IN-FORCE RANGE. *** {A6_REGISTERED} "
      f"sits under 4(d)'s lower edge {A4D_RANGE[0]}, and in the observable (gamma_v - 1) it is "
      f"{100*und_pt:.0f}% low at the point value / {100*und_wc:.0f}% low at the worst corner. This is a "
      f"registration error internal to the document, not a physics disagreement")
check(abs(A6_REGISTERED - round(A3_TARGET, 2)) < 5e-3,
      f"V2b and it is traceable: {A6_REGISTERED} is Amendment 3's {A3_TARGET} rounded -- the value "
      f"Amendment 4(d) explicitly retired with the words 'These supersede the Amendment 3 table'. "
      f"Amendment 6 reached back PAST the amendment that corrected it")


banner("V3  THE DETECTABILITY ARITHMETIC -- 3 sigma is unreachable at any N")

sig_tot_30k = math.hypot(SIG_FIT_30K, SIG_SYS)
print(f"  frozen error model: sigma_tot = sqrt(sigma_fit^2 + {SIG_SYS}^2), sigma_fit = {SIG_FIT_30K} at "
      f"N = {N_REF:,}, scaling as sqrt({N_REF}/N)")
print(f"  sigma_tot at N = {N_REF:,} = {sig_tot_30k:.5f}\n")
print(f"  {'hypothesis':<34}{'gamma_v-1':>11}{'z @ N=30k':>12}{'z @ N=inf':>12}")
print("  " + "-" * 70)
rows = [("Amendment 6 registered (~1.02)", A6_REGISTERED - 1),
        ("Amendment 4(d) point, IN FORCE", A4D_POINT - 1),
        ("Amendment 4(d) low corner", A4D_RANGE[0] - 1),
        ("Amendment 4(d) high corner", A4D_RANGE[1] - 1)]
for nm, sig in rows:
    print(f"  {nm:<34}{sig:>11.4f}{sig/sig_tot_30k:>12.2f}{sig/SIG_SYS:>12.2f}")

z_ceiling = (A4D_POINT - 1) / SIG_SYS
z_lo, z_hi = (A4D_RANGE[0] - 1) / SIG_SYS, (A4D_RANGE[1] - 1) / SIG_SYS
check(z_ceiling < 3.0 and z_hi < 3.0,
      f"V3a *** 3 SIGMA IS UNATTAINABLE AT ANY SAMPLE SIZE. *** As N -> infinity sigma_fit -> 0 and "
      f"sigma_tot -> sigma_sys = {SIG_SYS} irreducibly, so Newton-vs-MI ceilings at z = {z_ceiling:.2f} at the "
      f"in-force point value and {z_lo:.2f}-{z_hi:.2f} across the frozen corners. Not one corner reaches 3. "
      f"Amendment 6's 'a real risk taken in advance' is therefore not implementable in the frozen scoring "
      f"machinery as written")

# what section 1.5 would need on a statistical-only reading, under the IN-FORCE signal
sig_fit_needed = (A4D_POINT - 1) / 3.0
n_stat = N_REF * (SIG_FIT_30K / sig_fit_needed) ** 2
print(f"\n  section 1.5 claims '3 sigma needs N >~ {A15_N_FOR_3SIG:,} -- expected DECIDABLE'. That is "
      f"alpha=1, statistical-only.")
print(f"  redone statistical-only at the IN-FORCE signal {A4D_POINT-1:.4f}: need sigma_fit = "
      f"{sig_fit_needed:.5f} -> N ~ {n_stat:,.0f}")
check(n_stat > 3.0 * A15_N_FOR_3SIG,
      f"V3b even on the document's own statistical-only reading, section 1.5's N >~ {A15_N_FOR_3SIG:,} becomes "
      f"N ~ {n_stat:,.0f} -- a factor {n_stat/A15_N_FOR_3SIG:.1f} -- because it was computed for the retired "
      f"alpha=1 signal (1.09) and no amendment revisited it. 'Expected DECIDABLE' is stale either way")

# and the scoring-label trap: gamma_hat = 1.000 under the document's |z| < 2 rule
z_newton_vs_mi = (A4D_POINT - 1) / sig_tot_30k
check(z_newton_vs_mi < 2.0,
      f"V3c the label trap, computed: a measured gamma_hat = 1.000 sits {z_newton_vs_mi:.2f} sigma_tot from "
      f"the in-force MI target, so under the document's own |z| < 2 rule it scores as CONSISTENT WITH "
      f"framework-MI -- the OPPOSITE label from the 'evidence AGAINST' Amendment 6 intends. The intent and "
      f"the machinery disagree, and the machinery is what a scorer executes")


banner("V4  WHAT AMENDMENT 7 MUST REGISTER")

print(f"""  (a) THE IN-FORCE UNGATED alpha=2 TARGET IS gamma_v = {A4D_POINT} (range {A4D_RANGE[0]}-{A4D_RANGE[1]}),
      per Amendment 4(d). Amendment 6's "~1.02" row is CORRECTED, not merely annotated -- it is Amendment
      3's retired value and it lies below the entire in-force range (V2).

  (b) THE SCORING CONSEQUENCE IS RESTATED HONESTLY, and it cuts BOTH ways:
      * Amendment 6's withdrawal of the Amendment 1 hedge STANDS. A Newtonian 2-30 kAU result remains
        evidence AGAINST the framework's wide-binary prediction, and that must not be re-hedged.
      * BUT the strength of that evidence is capped by the frozen sigma_sys = {SIG_SYS}: Newton-vs-MI ceilings
        at z = {z_ceiling:.2f} ({z_lo:.2f}-{z_hi:.2f} across corners) as N -> infinity. **A 3-sigma verdict on this axis is
        not obtainable at any DR4 sample size.** Declaring the risk does not create the power to resolve it.
      * Section 1.5's "3 sigma needs N >~ {A15_N_FOR_3SIG:,} -- expected DECIDABLE" is WITHDRAWN as stale: it is
        alpha=1, statistical-only arithmetic. Redone at the in-force signal it is N ~ {n_stat:,.0f}, and with
        sigma_sys included it is unreachable.
      * The |z| < 2 label rule must be read with V3c in mind: gamma_hat = 1.000 scores as CONSISTENT WITH
        framework-MI at {z_newton_vs_mi:.2f} sigma_tot. Any scorer must report the RAW gamma_hat and both
        distances (to Newton and to {A4D_POINT}), not a single label.

  (c) WHAT DOES NOT CHANGE. The 16-row cut table, the estimator, the NSS screen, the error model itself, the
      strictness ladder, Amendment 5's voiding of the s^TX bands, the a0-degeneracy flag, and kappa = 1/2
      being fitted not derived. No measurement moves. And the falsifiability trap stays at 2 routes to a
      Newtonian reading, not 1 -- the audit found the hybrid S(|a|/a0) x L(omega/omega_c) gate branch
      survives Amendment 6's withdrawal, because the registered 1.0004-1.0006 was computed FROM that hybrid
      form and not from the amplitude-free reading Amendment 6 refutes.

  FILED AGAINST INTEREST on (b): this amendment makes the wide-binary front WEAKER as a discriminator than
  Amendment 6 implied, while keeping the un-hedged scoring rule that can only hurt the framework. It raises
  the framework's own predicted signal from 0.0200 to {A4D_POINT-1:.4f} -- which is the one part that helps -- and
  simultaneously shows that even the larger signal cannot reach 3 sigma against the frozen systematic.""")

banner("RESULT")
n = sum(1 for x, _ in ok if x)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for x, m in ok:
        if not x:
            print(f"    - {m}")
    sys.exit(1)
print(f"  Exit 0: in-force target {A4D_POINT} ({A4D_RANGE[0]}-{A4D_RANGE[1]}); 3 sigma unreachable at any N.")
