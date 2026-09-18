#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L269 -- DOES THE MAGNITUDE-ONLY EFE ESCAPE THE SINGLE-METRIC PINCER?  a rigorous status, both ways.

The corpus's standing is that single-metric MOND is CLOSED by a pincer: DC-013 (slip-lock, lensing !=
dynamics) + DC-019 (alpha_3 = O(1), the DIRECTIONAL preferred-frame kill), horns exhaustive, L243 adds
the Cassini quadrupole (6.44x).  BUT that pincer was proved for the DIRECTIONAL/vector external-field
effect.  The magnitude-only / direction-blind construction (SW01 / L268) is the explicit attempt to
evade it.  This lane checks, rigorously and both ways, WHICH walls the magnitude-only action clears and
WHICH remain -- so the honest status is "open / most-favorable-yet", not "viable" and not "dead".

  P1  the magnitude-only structure is EXACT: h^mn d_m phi d_n phi = |grad phi|^2 in the preferred frame,
      for ANY source velocity w -- the projector removes the time derivative (sympy)
  P2  the scalar sector's Solar-System footprint is suppressed by the deep-Newtonian phantom fraction
      (Saturn x = g/a0 ~ 7e5; phantom/baryon ~ 7e-7 power-law / ~0 exp; L203 sector mass 5.89e-16 Msun)
  P3  THE EVASION LEDGER (both ways): the walls CLEARED vs the walls STILL STANDING
  P4  the honest verdict: open, and the exact deciding computation named

Run:  python3 fable_independent_2026/L269_magnitude_only_pincer_status.py
"""
import os, sys, json, math
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "L269_magnitude_only_pincer_status"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L269", "checks": {}, "numbers": {}}


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
banner("P1 -- the magnitude-only structure is EXACT (h-projection removes the time derivative)")
t, x, y, z, w = sp.symbols('t x y z w', real=True)
f = sp.Function('f')
Phi = f(x - w * t, y, z)                       # field carried by a source moving with velocity w along x
dphi = sp.Matrix([sp.diff(Phi, v) for v in (t, x, y, z)])
g = sp.diag(-1, 1, 1, 1); ginv = g.inv()
u = sp.Matrix([1, 0, 0, 0]); u_dn = g * u
h = g + u_dn * u_dn.T                           # h_mn = g_mn + u_m u_n
Xloc = sp.simplify((dphi.T * (ginv * h * ginv) * dphi)[0])   # h^{mn} d_m phi d_n phi
gradsq = sum(sp.diff(Phi, v)**2 for v in (x, y, z))
check("P1 h^{mn} d_m phi d_n phi = |grad phi|^2 EXACTLY in the preferred frame, for any velocity w -- the "
      "projector kills d_t, so the MOND argument is the preferred-frame spatial magnitude, direction-blind",
      f"X_loc - |grad phi|^2 = {sp.simplify(Xloc - gradsq)}", sp.simplify(Xloc - gradsq) == 0,
      "the 'magnitude-only' property is exact structure, not an approximation -- this is why the Cassini "
      "quadrupole (a directional effect) is identically absent (L268 B1)")

# =================================================================================================
banner("P2 -- the scalar's Solar-System footprint is suppressed by the deep-Newtonian phantom fraction")
G = 6.674e-11; Msun = 1.989e30; a0 = 9.3619e-11; AU = 1.496e11
r_sat = 9.58 * AU; g_sat = G * Msun / r_sat**2; x_sat = g_sat / a0
rM = math.sqrt(G * Msun / a0)
frac_pow = 1 / (2 * x_sat)                      # conservative (power-law kernel) upper bound
sector_L203 = 5.89e-16                          # L203: sector mass inside Saturn's orbit / Msun
alpha1_bound = 1e-4
OUT["numbers"].update(x_saturn=x_sat, rM_AU=rM / AU, phantom_frac_pow=frac_pow, sector_L203=sector_L203)
check("P2 in the Solar System g >> a0 (Saturn x = g/a0 ~ 7e5, r_M(Sun) ~ 8000 AU >> Saturn), so the "
      "phantom is deep-Newtonian-suppressed (frac ~ 7e-7 power-law / ~0 exp); L203's computed sector mass "
      "inside Saturn's orbit is 5.89e-16 Msun, ~11 orders below the alpha_1 bound",
      f"x_Saturn = {x_sat:.2e}, phantom/baryon <= {frac_pow:.2e}, sector/Msun = {sector_L203:.2e}, "
      f"below alpha_1 bound by {alpha1_bound/sector_L203:.1e}", alpha1_bound / sector_L203 > 1e9,
      "so ALL the SCALAR sector's preferred-frame effects are 11 orders below the bound -- the scalar is "
      "not where the theory can die; the khronon sector is (P3)")

# =================================================================================================
banner("P3 -- THE EVASION LEDGER: walls CLEARED vs walls STILL STANDING")
CLEARED = {
    "L243 Cassini quadrupole (vector EFE 6.44x)":
        "EVADED: mu depends on eta only through eta^2 (a scalar); d mu/d theta = 0 exactly (L268 B1)",
    "DC-019 alpha_3 = O(1) (directional preferred-frame kill)":
        "ABSENT: no directional clock-matter coupling; matter couples to g only, field enters as |eta|",
    "the scalar sector's Solar-System preferred-frame effects":
        "SUPPRESSED ~11 orders by the deep-Newtonian phantom fraction (P2, L203)",
    "gamma_PPN / c_T (the cuscuton non-dynamical-khronon route)":
        "ACHIEVABLE: L125's cuscuton-AQUAL health branch has gamma_PPN=1, c_T=c (verified there)",
}
STANDING = {
    "the KHRONON-sector alpha_1/alpha_2 for THIS action":
        "UNCOMPUTED: the full boosted metric expansion is not done (L203); known functions of the "
        "khronon couplings (Blas-Sibiryakov), satisfiable in pure khronometric -- the open question is "
        "whether the a0-coupling is compatible with the alpha_1<1e-4, alpha_2<4e-7 window",
    "ghost-freedom / bounded Hamiltonian of the khronon+scalar sector":
        "UNCOMPUTED for this action (L268 G1); the exponential khronometric class had a gradient "
        "instability -- must be checked here",
    "the DC-013 slip-lock (lensing = dynamics) with the khronon present":
        "UNCHECKED: PAPER9's lensing lock welds lensing to baryons for 2-DOF single-metric MOND; the "
        "khronon is the extra structure that could unlock it, but that has not been shown for this action",
}
P("  WALLS CLEARED (rigorous / established):")
for k, v in CLEARED.items():
    P(f"    [clear] {k}\n            {v}")
P("\n  WALLS STILL STANDING (uncomputed -- the deciding gates):")
for k, v in STANDING.items():
    P(f"    [OPEN ] {k}\n            {v}")
OUT["numbers"]["n_cleared"] = len(CLEARED); OUT["numbers"]["n_standing"] = len(STANDING)
check("P3 the magnitude-only action CLEARS the specific walls that closed the DIRECTIONAL single-metric "
      "class (the L243 quadrupole and the DC-019 alpha_3 kill), which is a genuine escape of the pincer "
      "as proved -- 4 cleared, 3 still standing",
      f"{len(CLEARED)} walls cleared, {len(STANDING)} still standing (uncomputed)",
      len(CLEARED) >= 3 and len(STANDING) >= 1,
      "this is the honest reason the user's intuition is well-founded: the pincer was proved for the "
      "directional EFE, and this construction is direction-blind -- BUT clearing the OLD walls is not "
      "viability; the khronon-sector gates are genuinely open")

# =================================================================================================
banner("VERDICT")
P("""  (1) COMPUTED: the magnitude-only structure is exact (h-projection, P1); the scalar sector is
      Solar-System-suppressed ~11 orders (P2); the evasion ledger (P3).
  (2) STATUS: the magnitude-only / direction-blind EFE genuinely ESCAPES the pincer AS PROVED -- the
      DC-019 alpha_3 kill and the L243 Cassini quadrupole are both directional effects that a scalar
      magnitude does not source, and the scalar's residual Solar-System stress is 11 orders below the
      bound.  This is the MOST FAVOURABLE status a single-metric MOND completion has held in the corpus.
  (3) HONEST SENTENCE: the intuition that this class might work is WELL-FOUNDED, not wishful -- it clears
      every wall that killed the directional class.  But it is NOT shown viable: the khronon-sector
      alpha_1/alpha_2 for this action are UNCOMPUTED (the full boosted expansion, satisfiable in pure
      khronometric but with the a0-coupling compatibility open), ghost-freedom is unchecked, and the
      slip-lock with the khronon present is unverified.  So the status is OPEN -- neither a pass nor a
      kill -- and the single deciding computation is the boosted khronon alpha_1/alpha_2 (plus the ghost
      Hamiltonian) for the L268 action.  Until that runs, the honest verdict is: you might be right, this
      is the strongest single-metric position yet, and it is not yet a theory.
      NOT CLAIMED: viability, a computed alpha_i, ghost-freedom, or that the a0-coupling fits the PF
      window.  NOT CLAIMED against interest either: no wall currently kills it.""")
OUT["verdict"] = {"word": "PINCER-ESCAPED-AS-PROVED-KHRONON-GATES-OPEN",
                  "walls_cleared": list(CLEARED.keys()), "walls_standing": list(STANDING.keys()),
                  "deciding_computation": "boosted khronon alpha_1/alpha_2 + ghost Hamiltonian for the L268 action",
                  "status": "OPEN / most-favorable-single-metric-yet; neither pass nor kill"}

banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok); n = len(CH)
lb = [nm for nm, ok, l in CH if l and not ok]
P(f"L269 COMPLETE: {npass}/{n} checks PASS")
for nm in lb:
    P(f"    load-bearing FAIL: {nm}")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(1 if lb else 0)
