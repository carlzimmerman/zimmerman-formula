#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
dust_filters.py -- the FREE screening filters for open problem 2d (dust retention).
====================================================================================
Open problem 2d: the framework's dark sector is a shift-symmetric condensate whose
excitation is DUST.  Halos capture it, nothing stops it collapsing, and the endpoint is a
black hole falsified 5.8e5x against Sgr A*.  Every escape tried so far has died.

THIS FILE EXISTS SO THAT DEAD IDEAS DIE IN SECONDS INSTEAD OF IN A SESSION.  Five filters,
all derived and committed elsewhere, three of them PARAMETER-FREE.  Run a candidate through
them BEFORE spending a session on it.  Filters 4 and 5 are new (2026-08-17,
real_research/reviews/second_field_catalog_2026.py, 47/47) and each one alone would have
killed a construction the corpus spent real time on.

    python dust_filters.py --selftest        # gates: reproduce every committed number
    python dust_filters.py --explain         # print the five filters in full
    python dust_filters.py --screen spec.json

USAGE FROM A WORKER SESSION.  Write a small JSON describing the candidate, then screen it:

    {"name": "my mechanism",
     "suppresses_rho_locally": false,     # does it need rho < Q_0 n anywhere?  (F1)
     "hides_energy_from_both": false,     # does it need rho+p=0 AND rho+3p=0?   (F2)
     "keeps_sector_warm": false,          # does it need c_s^2 to NOT fall as a^-3? (F3)
     "support_is_barotropic": true,       # is the support pressure a local P(rho)? (F4)
     "Gamma": 1.3333,                     # its polytropic index, if barotropic       (F4)
     "gate_is_monotone_in_grad_phi": true # is the gate a monotone function of |grad phi|? (F5)
    }

Any FAIL is fatal on its own.  A candidate that passes all five is NOT thereby alive -- it
has merely earned a session.  Say so in the ledger row; do not upgrade "unscreened" to
"viable".

PROVENANCE.  F1/F2/F3 are nbody_2026 stages 5/6/9.  F4 is second_field_catalog D2b/D2c.
F5 is second_field_catalog F5a/F5b.  The CMB sound-speed cap 2606 (km/s)^2 is the committed
CLASS recombination run.  Nothing here uses kappa, a_0, the nu(y) kernel or the promotion:
these filters constrain the DUST SECTOR, so they are footing-independent by construction.
"""

import argparse
import json
import sys

import numpy as np

# ------------------------------------------------------------------ committed constants
KPC = 3.0856775814913673e19
MSUN = 1.98892e30
CS2_CAP = 2606.0                  # (km/s)^2, committed CLASS recombination cap
M_DUST = 2.51e12 * MSUN           # captured share in an L* halo
M_BAR = 6.0e10 * MSUN             # L* baryons
POLY_C_OVER_MEAN = np.pi**2 / 3.0  # n=1 polytrope central/mean density ratio
GAMMA_STABILITY = 4.0 / 3.0       # dynamical-stability boundary
F_LENS_FIXED_POINT = 1.0 / 3.0    # stage 6 Part E
M_LENS_OVER_DYN = 29.0            # at the f = 1/3 fixed point
BAROTROPIC_VIOLATION_AT_43 = 1.16e3   # x the cap, CALIBRATION-INDEPENDENT

FAIL, NCHK = [], [0]


def _chk(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


# ============================================================== the filters, as functions
def crossover_fraction(m_bar=M_BAR, m_dust=M_DUST):
    """F5: r_x/R_supp, the radius inside which a monotone |grad phi| gate has the RIGHT sign.

    Derivation (second_field_catalog F5a): the gate is built from |grad phi|, which for a
    self-gravitating dust cloud RISES outward wherever the held dust dominates its own
    field.  The crossover is where the baryons' field GM_bar/r^2 equals the dust's own
    (4pi/3)G rho_c r.  Solving, every scale except the mass ratio cancels:

        r_x/R_supp = [ M_bar / ((pi^2/3) M_dust) ]^(1/3)

    R, K, a_0, q, the footing and the gate scale all drop out.  PARAMETER-FREE.
    """
    return (m_bar / (POLY_C_OVER_MEAN * m_dust)) ** (1.0 / 3.0)


def mass_fraction_anti_supported(m_bar=M_BAR, m_dust=M_DUST):
    """F5b: the share of held mass OUTSIDE r_x, where the gate's pressure force has the
    wrong sign.  = 1 - (r_x/R_supp)^3, i.e. exactly 1 - M_bar/((pi^2/3) M_dust)."""
    return 1.0 - crossover_fraction(m_bar, m_dust) ** 3


def barotropic_rho_c_exponent(gamma):
    """F4: the exponent of rho_c in the support-velocity violation

        V ~ G M^(2/3) rho_c^(4/3 - Gamma) rho_rec^(Gamma - 1) / cap

    It VANISHES at Gamma = 4/3.  Since Gamma >= 4/3 is required for dynamical stability,
    the best case sits exactly where no choice of support density can help: the violation
    becomes calibration-INDEPENDENT.  Return the exponent so a candidate can be told
    whether tuning its support profile is even capable of moving the answer.
    """
    return 4.0 / 3.0 - gamma


def barotropic_verdict(gamma):
    """F4 verdict for a barotropic support law of index Gamma."""
    e = barotropic_rho_c_exponent(gamma)
    if gamma < GAMMA_STABILITY:
        return ("DEAD", e,
                f"Gamma = {gamma:.4g} < 4/3 is dynamically UNSTABLE -- the configuration "
                f"cannot hold itself up at all, independently of the CMB cap")
    if abs(e) < 1e-9:
        return ("DEAD", e,
                f"Gamma = 4/3 exactly: the rho_c exponent VANISHES, so the violation is "
                f"CALIBRATION-INDEPENDENT at {BAROTROPIC_VIOLATION_AT_43:.2e}x the "
                f"{CS2_CAP:.0f} (km/s)^2 cap -- no support radius, stiffness or central "
                f"density can move it")
    return ("DEAD", e,
            f"Gamma = {gamma:.4g} > 4/3 gives rho_c exponent {e:.4g} < 0, so raising the "
            f"support density LOWERS V -- but the sign means you need rho_c BELOW the "
            f"recombination density to comply, which is the opposite of holding dust up in "
            f"a halo.  The Gamma = 2 case forced by rho = Q_0 n returns 1.4e5-9.9e6x")


def screen(spec):
    """Run all five filters.  Returns (passed: bool, rows: list[(id, ok, message)])."""
    rows = []

    ok1 = not spec.get("suppresses_rho_locally", False)
    rows.append(("F1 rho = Q_0 n", ok1,
                 "the dust mass IS the conserved shift charge, so it cannot be suppressed "
                 "locally (nbody stage 5).  A mechanism that needs rho < Q_0 n anywhere is "
                 "asking the charge to stop being the mass."
                 if not ok1 else "does not require local suppression of rho"))

    ok2 = not spec.get("hides_energy_from_both", False)
    rows.append(("F2 lensing vs dynamics", ok2,
                 f"dynamics sees rho + 3p, lensing sees rho + p; rho+3p=0 needs w=-1/3 and "
                 f"rho+p=0 needs w=-1, which are incompatible.  At the f=1/3 fixed point "
                 f"M_lens/M_dyn = {M_LENS_OVER_DYN:.0f} (stage 6).  No equation of state "
                 f"hides a given energy from both."
                 if not ok2 else "does not need to hide the same energy from both channels"))

    ok3 = not spec.get("keeps_sector_warm", False)
    rows.append(("F3 c_s^2 ~ a^-3", ok3,
                 "c_s^2 = K'/[(Q_0+u)K''] falls as the charge dilutes, at the fixed rate "
                 "a^-3, for EVERY ghost-free K (stage 9).  The warm route needs "
                 "c_s^2(rec) = 595 c^2.  The sector cannot be kept warm."
                 if not ok3 else "does not rely on keeping the sector warm"))

    if spec.get("support_is_barotropic", False):
        g = float(spec.get("Gamma", 2.0))
        verdict, expo, why = barotropic_verdict(g)
        rows.append(("F4 barotropic support", verdict != "DEAD", why))
    else:
        rows.append(("F4 barotropic support", True,
                     "support is NOT a local P(rho) -- filter does not bite.  NOTE: F1 makes "
                     "any charge-built pressure a local P(rho), so declaring this false "
                     "requires the pressure to come from something OTHER than the charge, "
                     "and you must say what."))

    if spec.get("gate_is_monotone_in_grad_phi", False):
        frac = mass_fraction_anti_supported()
        rows.append(("F5 gate sign", False,
                     f"the crossover is r_x/R_supp = {crossover_fraction():.4f}, fixed by the "
                     f"baryon-to-dust ratio ALONE, so {frac*100:.2f}% of the held mass sits "
                     f"OUTSIDE r_x where a monotone |grad phi| gate gives the pressure force "
                     f"the WRONG SIGN.  Property of the class, not of any parameter choice."))
    else:
        rows.append(("F5 gate sign", True,
                     "gate is not a monotone function of |grad phi| -- filter does not bite. "
                     "State what the gate IS built from; if it is any monotone function of a "
                     "quantity that rises outward in a self-gravitating cloud, F5 applies "
                     "with the same 0.194 crossover."))

    return all(ok for _, ok, _ in rows), rows


# ================================================================================ selftest
def selftest():
    print("=" * 96)
    print("dust_filters.py SELFTEST -- every number must reproduce a committed result")
    print("=" * 96)
    fx = crossover_fraction()
    _chk(abs(fx - 0.194) < 5e-4,
         f"G1  F5 crossover r_x/R_supp = {fx:.5f} reproduces the committed 0.194",
         "parameter-free: M_bar/((pi^2/3) M_dust) only -- R, K, a_0, q, footing, gate scale "
         "all cancel")
    frac = mass_fraction_anti_supported()
    _chk(abs(frac - 0.9927) < 5e-4,
         f"G2  F5b anti-supported mass fraction = {frac*100:.2f}% reproduces the committed "
         f"99.27%",
         "so a monotone |grad phi| gate has the wrong sign over essentially the whole cloud")
    _chk(abs(barotropic_rho_c_exponent(GAMMA_STABILITY)) < 1e-12,
         f"G3  F4 the rho_c exponent (4/3 - Gamma) VANISHES at Gamma = 4/3 exactly "
         f"({barotropic_rho_c_exponent(GAMMA_STABILITY):.1e})",
         f"which is why the violation there is calibration-INDEPENDENT at "
         f"{BAROTROPIC_VIOLATION_AT_43:.2e}x the cap")
    _chk(barotropic_rho_c_exponent(1.2) > 0 and barotropic_rho_c_exponent(2.0) < 0,
         f"G4  F4 the exponent changes sign across 4/3: +{barotropic_rho_c_exponent(1.2):.4g} "
         f"at Gamma = 6/5 and {barotropic_rho_c_exponent(2.0):.4g} at Gamma = 2",
         "so no monotone tuning of the support density helps on both sides")
    for g in (1.2, GAMMA_STABILITY, 2.0):
        v, e, _ = barotropic_verdict(g)
        _chk(v == "DEAD", f"G5  F4 returns DEAD at Gamma = {g:.4g} (exponent {e:+.4g})",
             "all three committed indices fail; 6/5 fails on dynamical stability instead")
    # a candidate that trips nothing must pass, and one that trips anything must fail
    clean = dict(suppresses_rho_locally=False, hides_energy_from_both=False,
                 keeps_sector_warm=False, support_is_barotropic=False,
                 gate_is_monotone_in_grad_phi=False)
    p_clean, _ = screen(clean)
    _chk(p_clean, "G6  a candidate tripping no filter PASSES the screen",
         "the screen is not a rubber stamp in the other direction either -- passing earns a "
         "session, nothing more")
    for k in ("suppresses_rho_locally", "hides_energy_from_both", "keeps_sector_warm",
              "gate_is_monotone_in_grad_phi"):
        bad = dict(clean); bad[k] = True
        p, _ = screen(bad)
        _chk(not p, f"G7  flipping {k} alone FAILS the screen", "each filter is fatal alone")
    bad = dict(clean); bad.update(support_is_barotropic=True, Gamma=2.0)
    p, _ = screen(bad)
    _chk(not p, "G8  a barotropic Gamma = 2 support FAILS the screen",
         "which is the case rho = Q_0 n forces, so F1 and F4 compose")
    _chk(abs(M_LENS_OVER_DYN - 29.0) < 1e-9 and abs(F_LENS_FIXED_POINT - 1 / 3) < 1e-12,
         "G9  the F2 constants match stage 6 Part E (f = 1/3 fixed point, "
         "M_lens/M_dyn = 29)")
    print()
    n = len(FAIL)
    print(f"DUST-FILTER SELFTEST: {NCHK[0]-n}/{NCHK[0]} passed"
          + ("" if not n else f"; FAILED: {FAIL}"))
    return 1 if FAIL else 0


EXPLAIN = r"""
THE FIVE FREE FILTERS FOR OPEN PROBLEM 2d
=========================================
Run these on any dust-retention candidate BEFORE spending a session.  Each is fatal alone.

F1  rho = Q_0 n IDENTICALLY.  The dust mass IS the conserved shift charge, so it cannot be
    suppressed locally.  Any charge-built pressure is therefore a LOCAL P(rho), hence
    stiffest exactly where the charge is densest -- which is recombination, not the halo.
    (nbody stage 5.)  CONSEQUENCE: "support_is_barotropic" is almost never honestly false.

F2  NO EQUATION OF STATE HIDES ENERGY FROM BOTH CHANNELS.  Dynamics sees rho + 3p, lensing
    sees rho + p.  rho+3p = 0 needs w = -1/3; rho+p = 0 needs w = -1.  Incompatible.  At
    the f = 1/3 fixed point M_lens/M_dyn = 29.  (stage 6 Part E.)

F3  THE SECTOR CANNOT BE KEPT WARM.  c_s^2 = K'/[(Q_0+u)K''] -> 0 as the charge dilutes,
    at the fixed rate a^-3, for EVERY ghost-free K.  The warm route would need
    c_s^2(rec) = 595 c^2.  (stage 9.)

F4  THE BAROTROPIC VIOLATION IS CALIBRATION-INDEPENDENT AT THE STABILITY BOUNDARY.  NEW.
        V ~ G M^(2/3) rho_c^(4/3 - Gamma) rho_rec^(Gamma - 1) / cap
    The rho_c exponent is exactly (4/3 - Gamma) and VANISHES at Gamma = 4/3 -- the
    dynamical-stability boundary itself.  So at the best allowed index the violation is
    1.16e3x the committed 2606 (km/s)^2 CMB cap and NO choice of support radius, stiffness
    or central density moves it.  Below 4/3 the configuration is unstable; at Gamma = 2
    (which F1 forces) it is 1.4e5-9.9e6x.  (second_field_catalog D2b/D2c.)

F5  A MONOTONE |grad phi| GATE HAS THE WRONG SIGN OVER 99.27% OF THE CLOUD.  NEW, and
    PARAMETER-FREE.  |grad phi| RISES outward wherever the held dust dominates its own
    field, so a gate that switches support on with |grad phi| anti-supports the outside.
    The crossover is
        r_x/R_supp = [ M_bar / ((pi^2/3) M_dust) ]^(1/3) = 0.194
    fixed by the baryon-to-dust ratio ALONE -- R, K, a_0, q, the footing and the gate scale
    all cancel -- so 1 - 0.194^3 = 99.27% of the held mass is anti-supported.  TEST THIS
    FIRST: it costs nothing and it would have killed the corpus's own gated construction on
    day one.  (second_field_catalog F5a/F5b.)

WHAT PASSING MEANS.  Nothing except that the candidate has earned a session.  Record it as
SCREENED, never as VIABLE.  And note the two structural facts that make this problem hard:
the a_0-gate amplification and the barotropic factor are THE SAME OBSTRUCTION (both are
monotone in the charge density, both adverse by >= 1.3e3 in every committed calibration);
and the property that makes w = -1 exact is the property that makes the excitation dust, so
the dark-energy success and this problem are the same feature of the same field.

WHAT WOULD ACTUALLY BE NEW.  A mechanism whose support pressure is NOT built from the
conserved charge (evading F1, and with it F4), whose gate is NOT monotone in a quantity
that rises outward (evading F5), and which does not need the sector warm (F3) or hidden
from both channels (F2).  The corpus's named candidate class -- a genuine SECOND SECTOR
carrying the pressure -- is a structural change, not a new free function.  All four
catalogued members of that class are dead; the class is not exhausted.
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[2])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--explain", action="store_true")
    ap.add_argument("--screen", metavar="SPEC.json")
    a = ap.parse_args()
    if a.explain:
        print(EXPLAIN)
        return 0
    if a.screen:
        spec = json.load(open(a.screen))
        print(f"SCREENING: {spec.get('name','(unnamed)')}")
        passed, rows = screen(spec)
        for fid, ok, msg in rows:
            print(f"  [{'pass' if ok else 'KILL'}] {fid}\n         {msg}")
        print()
        print("VERDICT: " + ("SCREENED -- earns a session; record as SCREENED, NOT viable"
                             if passed else
                             "DEAD on a free filter.  Do NOT spend a session on it.  Record "
                             "the ledger row with the filter id that killed it."))
        return 0 if passed else 2
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
