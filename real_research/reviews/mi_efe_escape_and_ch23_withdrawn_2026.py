#!/usr/bin/env python3
r"""mi_efe_escape_and_ch23_withdrawn_2026.py -- TWO MANUFACTURED WINS, WITHDRAWN WITH THE ARITHMETIC.

Both of these make the framework look better than it is, and both were caught by the 2026-08-02 closure
audit. Neither is a physics failure of the framework; both are bookkeeping errors in OUR OWN documents.

(1) THE "EFE ESCAPE" DOES NOT EXIST. mi_alpha1_solar_system_2026.py:127-133 computes the post-EFE residual
    as   a_tot = (g_in + g_ex)(1 + a0/2(g_in+g_ex)),  a_obs = a_tot - a_ex,  anom = a_obs - g_in
    -- i.e. it SCALAR-ADDS the Galactic external field to the sunward internal field and then scalar-
    subtracts the host's own boost. That points g_ext permanently sunward. It does not: g_ext is fixed in
    INERTIAL space while the a0/2 anomaly rides -r_hat and rotates with orbital phase. Done as vectors and
    averaged over the orbit, the g_ext terms average to ZERO and the sunward anomaly is the bare a0/2.
    So STANDING.md's "the framework's own derived EFE (Thm 5) suppresses it only to 119-189x over" is wrong;
    post-EFE = bare, and the number is 1278x (canonical) / 1543x (alt).

(2) BOOK CH.23's CKN CURVE IS HARD-NORMALIZED TO MANUFACTURE ITS OWN PUNCHLINE.
    book/figures/ch23_two_roads_to_half.py:17 is literally  ckn_energy = 0.5 * g**(-0.25),  commented
    "normalized so the single-dof (g_*=1) geometric limit lands at exactly 1/2". The g_*=1 coefficient is
    (3/8pi)^(1/4) = 0.5877875, which the same chapter prints 25 lines earlier. Substituting 1/2 for it is a
    17.56% change, and it is the change that makes the figure's "two roads to one half" land.

  E1  the EFE escape, done as vectors over orbital phase -- both footings, several g_ext directions
  E2  what the script's scalar construction actually computed (the phase MINIMUM), and the sign claim
  E3  the Ch.23 substitution, and whether the "two roads" are independent
  E4  the exact withdrawals

Exit 0 = ran and every internal check held. No hard-coded verdicts, no check(True).
"""
from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp

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


GM_SUN = 1.32712440018e20
AU = 1.495978707e11
FOOTINGS = {"canonical": 9.36e-11, "alt": 1.13e-10}
# the two g_ext conventions the alpha=1 script carries
G_EXT = {"primary 1.8e-10": 1.8e-10, "alt 2.1456e-10": 2.1456e-10}
# published Earth/Mars 2-sigma anomalous-acceleration bounds used by STANDING
BOUND_EARTH = 3.66e-14


def nu1(g, a0):
    """alpha=1: g_obs = nu(g_bar) g_bar with nu = sqrt(1 + a0/g_bar)."""
    return np.sqrt(1.0 + a0 / g)


banner("E1  THE EFE ESCAPE, DONE AS VECTORS OVER ORBITAL PHASE")

print("""  Correct construction. Both bodies obey the framework's law in the TOTAL field:
      planet:  a_p = nu(|g_in + g_ext|) (g_in + g_ext)
      Sun:     a_s = nu(|g_ext|) g_ext                       (host CoM; g_ext/a0 ~ 2, so nu ~ 1.24, O(1))
      observable relative acceleration  a_rel = a_p - a_s ,  anomaly  d_a = a_rel - g_in
  g_in = -GM/r^2 r_hat rotates with the planet; g_ext is FIXED in inertial space. Averaging the sunward
  component of d_a over one orbit is the observable an ephemeris fit constrains.\n""")

NPH = 200000
phase = np.linspace(0.0, 2 * math.pi, NPH, endpoint=False)
r = 1.5237 * AU                                   # Mars, as the alpha=1 script uses
g_in_mag = GM_SUN / r**2

print(f"  {'footing':<10}{'g_ext':<18}{'bare a0/2':>12}{'<sunward>':>12}{'ratio':>9}{'min over phase':>16}")
print("  " + "-" * 78)
res = {}
for fn, a0 in FOOTINGS.items():
    for gn, gex in G_EXT.items():
        # geometry: r_hat rotates; put g_ext along +x
        rx, ry = np.cos(phase), np.sin(phase)
        gin_x, gin_y = -g_in_mag * rx, -g_in_mag * ry     # sunward
        Gx, Gy = gin_x + gex, gin_y                        # total field on the planet
        Gmag = np.hypot(Gx, Gy)
        nuG = nu1(Gmag, a0)
        apx, apy = nuG * Gx, nuG * Gy
        asx, asy = nu1(gex, a0) * gex, 0.0                 # Sun: external field only
        # anomaly = relative acceleration minus the Newtonian internal field
        dax, day = (apx - asx) - gin_x, (apy - asy) - gin_y
        sunward = -(dax * rx + day * ry)                   # component along -r_hat
        mean, mn = float(sunward.mean()), float(sunward.min())
        res[(fn, gn)] = (mean, mn)
        print(f"  {fn:<10}{gn:<18}{a0/2:>12.4e}{mean:>12.4e}{mean/(a0/2):>9.5f}{mn:>16.4e}")

ratios = [res[k][0] / (FOOTINGS[k[0]] / 2) for k in res]
check(all(abs(x - 1.0) < 1e-3 for x in ratios),
      f"E1a *** THERE IS NO EFE SUPPRESSION OF THE a0/2 TAIL. *** The orbit-averaged sunward anomaly is "
      f"{min(ratios):.5f}-{max(ratios):.5f} x the bare a0/2 on all {len(res)} footing x g_ext combinations. "
      f"Post-EFE = bare, to within 0.1%")

# WHY: the g_ext terms are fixed-direction, so their projection on r_hat averages to zero over the orbit.
rx = np.cos(phase)
check(abs(float(rx.mean())) < 1e-12,
      f"E1b the mechanism, in one line: every g_ext-carried term enters the sunward projection through "
      f"<g_ext . r_hat>, and <cos(phase)> = {float(rx.mean()):.1e} over a full orbit. A fixed-direction force "
      f"cannot cancel a term that co-rotates with the radius vector. It produces a FORCED ECCENTRICITY "
      f"instead -- which is exactly the piece an ephemeris fit absorbs, so the 'escape' traded an "
      f"unobservable term against an observable one")

for fn, a0 in FOOTINGS.items():
    over = (a0 / 2) / BOUND_EARTH
    print(f"  {fn:<10} bare a0/2 = {a0/2:.4e} vs the Earth 2-sigma bound {BOUND_EARTH:.2e} -> {over:.0f}x over")
check(abs((FOOTINGS["canonical"] / 2) / BOUND_EARTH - 1278) < 5,
      f"E1c so the correct post-EFE figure is {(FOOTINGS['canonical']/2)/BOUND_EARTH:.0f}x (canonical) / "
      f"{(FOOTINGS['alt']/2)/BOUND_EARTH:.0f}x (alt) over the Earth bound -- identical to the BARE numbers, "
      f"not the 119-189x STANDING.md:669 claims")


banner("E2  WHAT THE SCALAR CONSTRUCTION ACTUALLY COMPUTED")

print("  Reproducing mi_alpha1_solar_system_2026.py:127-133 verbatim, then comparing to the phase curve:\n")
print(f"  {'footing':<10}{'g_ext':<18}{'script resid':>14}{'phase min':>13}{'match':>9}{'script supp':>13}")
print("  " + "-" * 78)
for fn, a0 in FOOTINGS.items():
    for gn, gex in G_EXT.items():
        a_ex = gex * float(nu1(gex, a0))
        a_tot = (g_in_mag + gex) * (1 + a0 / (2 * (g_in_mag + gex)))
        anom = (a_tot - a_ex) - g_in_mag
        mn = res[(fn, gn)][1]
        print(f"  {fn:<10}{gn:<18}{anom:>14.4e}{mn:>13.4e}{anom/mn:>9.4f}{abs(a0/2/anom):>13.1f}x")

sc = {}
for fn, a0 in FOOTINGS.items():
    for gn, gex in G_EXT.items():
        a_ex = gex * float(nu1(gex, a0))
        a_tot = (g_in_mag + gex) * (1 + a0 / (2 * (g_in_mag + gex)))
        sc[(fn, gn)] = (a_tot - a_ex) - g_in_mag
match = [sc[k] / res[k][1] for k in sc]
check(all(0.9 < m < 1.1 for m in match),
      f"E2a the script's 'post-EFE residual' reproduces the PHASE MINIMUM of the correct curve to "
      f"{min(match):.3f}-{max(match):.3f} -- i.e. it computed the single most favourable point of the orbit and "
      f"reported it as the orbit's value. Half an orbit later the same construction gives the phase MAXIMUM")
mx = {k: float(res[k][0]) for k in res}
check(all(v > 0 for v in mx.values()),
      f"E2b and the '.out NOTE THE SIGN FLIP ... leaving a net OUTWARD residual' is withdrawn too: all "
      f"{len(mx)} orbit-averaged residuals are POSITIVE (sunward). The sign flip was an artefact of the same "
      f"scalar subtraction -- there is no outward branch")


banner("E3  THE CH.23 SUBSTITUTION, AND WHETHER THE 'TWO ROADS' ARE INDEPENDENT")

CKN_TRUE = float((sp.Rational(3, 8) / sp.pi) ** sp.Rational(1, 4))
Z = math.sqrt(32 * math.pi / 3)
G_STAR_SM = 106.75
print(f"  the g_*=1 CKN energy coefficient is (3/8pi)^(1/4) = {CKN_TRUE:.7f}")
print(f"  the figure hard-codes                                {0.5:.7f}   (a "
      f"{100*(CKN_TRUE-0.5)/0.5:.2f}% substitution)")
print(f"  at the Standard Model's g_* = {G_STAR_SM}:")
print(f"      as coded          0.5 * g^-1/4      = {0.5*G_STAR_SM**-0.25:.5f}   (BELOW the figure's own "
      f"annotated 0.18-0.41 band)")
print(f"      correctly         0.5878 * g^-1/4   = {CKN_TRUE*G_STAR_SM**-0.25:.5f}   (ON the band edge, "
      f"reproducing the source doc)")
check(abs(CKN_TRUE - 0.5877875) < 1e-6 and CKN_TRUE * G_STAR_SM**-0.25 > 0.18 > 0.5 * G_STAR_SM**-0.25,
      f"E3a the substitution is load-bearing, not cosmetic: with the correct {CKN_TRUE:.4f} the SM point lands "
      f"at {CKN_TRUE*G_STAR_SM**-0.25:.5f}, inside the figure's own annotated band; with the hard-coded 0.5 it "
      f"lands at {0.5*G_STAR_SM**-0.25:.5f}, outside it. The figure's conclusion depends on the wrong constant")

# the y-axis label claims "coefficient of a0/cH_Lambda". That value is 1/Z, not 0.5878.
check(abs(1.0 / Z - 0.172747) < 1e-5,
      f"E3b and the y-axis label is the wrong quantity: the coefficient of a0/cH_Lambda is 1/Z = "
      f"{1.0/Z:.6f}, not {CKN_TRUE:.4f}. The two differ by exactly sqrt(8pi/3) = "
      f"{math.sqrt(8*math.pi/3):.6f}, so the axis is the CKN O(1) slot, not the a0 coefficient")

# are the two roads independent? sqrt(2/Z) = sqrt(2 kappa) * (3/8pi)^(1/4)  =>  landing on (3/8pi)^(1/4)
# REQUIRES kappa = 1/2 as an input.
kap = sp.Symbol("kappa", positive=True)
Zsym = sp.sqrt(8 * sp.pi / 3) / kap                # a0 = k c sqrt(G rho_L) = cH_L/Z => Z = sqrt(8pi/3)/k
slot = sp.simplify(sp.sqrt(2 / Zsym))
target = (sp.Rational(3, 8) / sp.pi) ** sp.Rational(1, 4)
check(sp.simplify(slot / target - sp.sqrt(2 * kap)) == 0,
      f"E3c *** THE TWO ROADS ARE NOT INDEPENDENT. *** sqrt(2/Z) = sqrt(2 kappa) x (3/8pi)^(1/4) "
      f"identically, so the framework's slot equals the CKN geometric limit IF AND ONLY IF kappa = 1/2. "
      f"The 'coincidence' is the input. d ln slot / d ln kappa = "
      f"{sp.simplify(sp.diff(sp.log(slot), kap) * kap)}, not 0 -- so 'kappa cancels' is also false")


banner("E4  THE EXACT WITHDRAWALS")

print(f"""  1. STANDING.md:668-669  "the framework's *own* derived EFE (Thm 5) suppresses it only to 119-189x over"
        -> "there is NO EFE suppression of the a0/2 tail: the orbit-averaged sunward anomaly is
           1.000 x a0/2 on all four footing x g_ext combinations (E1), so post-EFE = bare =
           {(FOOTINGS['canonical']/2)/BOUND_EARTH:.0f}x (canonical) / {(FOOTINGS['alt']/2)/BOUND_EARTH:.0f}x (alt) over the Earth 2-sigma bound. The
           scalar construction that produced 119-189x pointed g_ext permanently sunward and reported the
           orbit's phase MINIMUM (E2a)."
     and the .out "NOTE THE SIGN FLIP ... net OUTWARD residual" sentence is struck (E2b).

  2. STANDING.md:621 / :631 / :924  s^TX Front B advertised LIVE at margin 1.50x / 1.24x
        -> NOT A LIVE FRONT. Under the alpha=2 kernel in force the prediction collapses by a0/g at Saturn
           and the margin goes to 1.03e6x / 7.09e5x; PREREGISTRATION_DR4 Amendment 5 voids the DETECT/KILL
           bands. The stale directive at :631 is the line a reader acts on, so it is struck, not annotated.

  3. book/figures/ch23_two_roads_to_half.py:17  ckn_energy = 0.5 * g**(-0.25)
        -> {CKN_TRUE:.7f} * g**(-0.25), and the chapter's "collapses to exactly kappa = 1/2" /
           "two roads, one number" claims are withdrawn: the two roads are the SAME road (E3c).

  WHAT NONE OF THIS TOUCHES: the alpha=1 liability was already known and already priced -- these three fixes
  make it WORSE by removing a false escape, and make one book figure honest. The framework's a0 claim, the
  RAR/BTFR results and the alpha=2 migration's other findings are unaffected. And the alpha=1 kernel is
  retired anyway; what this corrects is the RECORD of why.""")

banner("RESULT")
n = sum(1 for x, _ in ok if x)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for x, m in ok:
        if not x:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: the EFE escape does not exist (post-EFE = bare); Ch.23's two roads are one road.")
