#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L273 -- RECONCILIATION + SELF-CORRECTION: my L268-L272 vs the glm_moe swarm's SW04-SW07.

The glm_moe/fable swarm ran the direction-blind ("cap law") covariant programme to completion (SW03-SW07,
CK01) while I was writing L268-L272.  Reading their committed work back against mine, my chain was PARTLY
FLAWED and PARTLY SUPERSEDED.  This lane records the correction on its own terms (I do NOT edit the
swarm's files; astra/glm_moe lead this).

  C1 [MY ERROR, verified] L268 as written is NOT direction-blind.  X_loc = h^mn d_m phi d_n phi with phi
     the TOTAL field = |grad phi_int + grad phi_ext|^2 carries the cross term 2 x eta cos(theta); adding
     X_env = eta^2 gives x^2 + 2 eta^2 + 2 x eta cos(theta), d/dtheta != 0.  My B1 assigned x^2 + eta^2 by
     hand and "verified" a quadrupole evasion that does not hold (SW05: quadrupole ~4.8x Cassini).
  C2 [SWARM SW04, reproduced] for the SMOOTHED-TOTAL-SWITCH structure, gamma=1 without gravitomagnetism
     gives alpha_1 = -8(nu(eta_gal)-1)/nu = -1.4 to -2.1 = 2e4x the bound: a KILL, and no ell-window.
  C3 [SWARM SW05, reproduced] the one-substitution REPAIR X_loc = |grad(phi - phibar)|^2 IS direction-
     blind; the internal field at Saturn is x ~ 7e5 so the scalar is off, |alpha_1| <= 9e-11 (PASSES PPN),
     open window ell in [0.05 pc, 2.1 kpc].  My L270-L272 "alpha_1 passable" happens to match THIS, but I
     analysed the flawed L268 (not the repair) and never wrote the repair.
  C4 [SWARM SW06, the gate I SKIPPED] the repaired action's LENSING is dead on EVERY route (GW170817
     differential Shapiro; conformal-drops-from-null-cone; the Lean local no-go; fifth-force; AeST alpha_1)
     EXCEPT A4 = the standing candidate's structure.  So it passes PPN but cannot give lensing=dynamics
     except by BECOMING the pre-existing candidate.  I checked alpha_1 across L268-L272 and never checked
     lensing -- and lensing is where it dies.
  C5 [VERDICT, SWARM SW07] the direction-blind / cap-law covariant programme is CLOSED: no covariant
     realisation with lensing on the record.  The live construction is the STANDING single-metric
     candidate (clock host + xi-screened scalar, FINAL_THEORY_CANDIDATE_2026-09-05 / L223), whose EFE is
     xi-smoothed AQUAL (directional), NOT the cap law.  DR4 three-way: candidate 1.000 / cap law
     1.086-1.155 / AQUAL 1.16-1.23.

Run:  python3 fable_independent_2026/L273_direction_blind_reconciliation.py
"""
import os, sys, json, math
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "L273_direction_blind_reconciliation"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L273", "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 100); P(t); P("=" * 100)


P(__doc__)
# =================================================================================================
banner("C1 [MY ERROR, verified] L268 as written is NOT direction-blind")
x, eta, th = sp.symbols('x eta theta', positive=True)
Xloc_total = x**2 + eta**2 + 2 * x * eta * sp.cos(th)          # |grad phi_total|^2 (phi = int + ext)
arg_asWritten = sp.simplify(Xloc_total + eta**2)              # + X_env = eta^2
check("C1 L268 as written (X_loc from the TOTAL field) gives argument x^2 + 2 eta^2 + 2 x eta cos(theta), "
      "which is DIRECTION-DEPENDENT -- my B1 'quadrupole evaded' was a tautology (I posited x^2+eta^2)",
      f"arg = {arg_asWritten}, d/dtheta = {sp.diff(arg_asWritten, th)} (!= 0)",
      sp.diff(arg_asWritten, th) != 0,
      "SW05 is correct: the unsmoothed L268 has a ~4.8x Cassini quadrupole; L269-L272 built on a false "
      "direction-blindness premise")

# =================================================================================================
banner("C2 [SWARM SW04, reproduced] the smoothed-total-switch alpha_1 is a KILL")
nu = lambda y: 1.0 / (1.0 - math.exp(-math.sqrt(y)))
a1 = {e: -8 * (nu(e) - 1) / nu(e) for e in (1.5, 1.8, 2.1)}
OUT["numbers"]["alpha1_smoothed_total"] = a1
check("C2 SW04's theorem gamma=1 without gravitomagnetism => alpha_1 = -8(nu(eta_gal)-1)/nu; at the Sun's "
      "galactic eta ~ 1.5-2.1 this is -1.4 to -2.4, i.e. ~2e4x the |alpha_1|<1e-4 bound -- reproduced",
      f"alpha_1(eta) = {{{', '.join(f'{e}:{v:.2f}' for e,v in a1.items())}}}",
      all(abs(v) > 1 for v in a1.values()),
      "the smoothed-total-switch structure (SW03) is killed on alpha_1, no ell-window (SW04)")

# =================================================================================================
banner("C3 [SWARM SW05, reproduced] the repair passes PPN -- but I analysed the wrong action")
G = 6.674e-11; Msun = 1.989e30; a0 = 9.3619e-11; AU = 1.496e11
x_sat = (G * Msun / (9.58 * AU)**2) / a0
arg_repair = sp.simplify(x**2 + eta**2)                      # X_loc = |grad(phi - phibar)|^2
check("C3 the REPAIR X_loc = |grad(phi - phibar)|^2 gives x^2 + eta^2 (direction-blind); the internal "
      "field at Saturn x ~ 7e5 switches the scalar off, so |alpha_1| <= 9e-11 (SW05, PASSES PPN). My "
      "L270-L272 'passable' matches this REPAIR -- but I analysed the flawed L268, not the repair",
      f"repaired arg = {arg_repair}, d/dtheta = {sp.diff(arg_repair, th)}; x_Saturn = {x_sat:.2e} (scalar off)",
      sp.diff(arg_repair, th) == 0 and x_sat > 1e4,
      "credit to the swarm: they wrote the repair and computed |alpha_1|<=9e-11; I did not")

# =================================================================================================
banner("C4 [SWARM SW06, the gate I SKIPPED] the repaired action's LENSING is dead")
routes = {"B conformal/disformal": "GW170817 differential Shapiro 3e7-1e8 s vs 1.7 s -- DEAD",
          "C null-cone": "conformal factor drops from the null cone => baryons-only bending -- DEAD",
          "A1 local scalar": "LOCAL no-go (sqrt(a0) w/(4 pi G sqrt(GM)) M-dependent), Lean-certified -- DEAD",
          "A2 matter-sourced": "fifth force, photons do not feel it -- DEAD",
          "A3 AeST": "alpha_1 = -2(K_B+2) -- DEAD on the record",
          "A4 khronon-sourced switched-off": "= the STANDING CANDIDATE's structure (the one live route)"}
for k, v in routes.items():
    P(f"    {k}: {v}")
dead = sum(1 for v in routes.values() if "DEAD" in v)
check("C4 across L268-L272 I checked alpha_1 and NEVER checked lensing; SW06 shows the repaired action's "
      "lensing is dead on all 5 routes except A4 = the standing candidate -- so it passes PPN but cannot "
      "give lensing=dynamics except by BECOMING the pre-existing candidate",
      f"{dead}/6 lensing routes DEAD; the only live one (A4) IS the standing candidate's structure", dead == 5,
      "THIS is the killer of the cap-law programme, and I missed it entirely -- the honest failure of my "
      "L268-L272 chain")

# =================================================================================================
banner("VERDICT")
P("""  (1) RECONCILED: my L268-L272 against the swarm's SW04-SW07 (glm_moe/astra lead).
  (2) THE CORRECTION: L268 as written is NOT direction-blind (my B1 was a tautology; ~4.8x Cassini
      quadrupole), so L269-L272's premise was false.  The swarm's REPAIR (X_loc = |grad(phi-phibar)|^2)
      IS direction-blind and passes PPN (|alpha_1| <= 9e-11) -- my 'alpha_1 passable' coincidentally
      matches it, but I analysed the flawed action and, decisively, NEVER checked the lensing gate.
  (3) HONEST SENTENCE: I overstated 'you might be right' across five lanes.  The direction-blind / cap-law
      covariant programme is CLOSED (SW07): the only PPN-passing form has its lensing dead on every route
      except by becoming the pre-existing standing candidate (clock host + xi-screened scalar, 09-05 /
      L223), whose EFE is xi-smoothed AQUAL (directional), NOT the cap law.  My L268 carried a real error;
      L269-L272 inherited it; and the actual killer -- lensing -- is the one gate I skipped.  The live
      construction is the standing single-metric candidate, and the whole class is a DR4 three-way
      (candidate 1.000 / cap law 1.086-1.155 / AQUAL 1.16-1.23).
      CREDIT: the swarm (SW03-SW07, CK01) did the complete and correct analysis; this lane records it and
      corrects my chain.  NOT CLAIMED: any part of the swarm's result as mine.""")
OUT["verdict"] = {"word": "L268-FLAWED-L269-272-SUPERSEDED-PROGRAMME-CLOSED",
                  "my_error": "L268 not direction-blind (B1 tautology); lensing gate never checked",
                  "repair_passes_ppn": True, "repair_lensing_dead": True,
                  "live_construction": "standing single-metric candidate (clock host + xi-screened scalar, 09-05/L223)",
                  "credit": "glm_moe/astra swarm SW03-SW07, CK01"}

banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok); n = len(CH)
lb = [nm for nm, ok, l in CH if l and not ok]
P(f"L273 COMPLETE: {npass}/{n} checks PASS")
for nm in lb:
    P(f"    load-bearing FAIL: {nm}")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(1 if lb else 0)
