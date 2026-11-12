#!/usr/bin/env python3
"""
FINAL-17 (KAPPA_A) -- the SELF-SOURCE / CAPACITY route to kappa.

Lane FINAL-17 (hy4_preview_push). Date: 2026-11-11. TEST lane, quarantined:
adopts nothing, relabels nothing, registers nothing, edits nothing outside this
folder. Footings NEVER pooled (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10
m/s^2). kappa = 1/2 FITTED; not theory closed.

WHAT THIS LANE IS
-----------------
The record carries two claims this lane audits and then attempts:

  (1) a "kappa = 1/2 SELF-SOURCE CLOSURE" (GF1+GF2, deepseek_push).  GF2 derives
      sigma^2/v_flat^2 = 1/2 exactly from the committed static branch
      Phi = C ln r + Poisson + stationarity/barotropy.  GF1 reduces every
      spelling of the tie to one integer n with kappa := a0/s, s := n a0.
  (2) "the quadratic a0-line is the n = 2 HALF-CAPACITY variant, certified
      distinct" (Sigma107v214 / AG4 branch a, argon_push/AG4_law_from_action).

THE QUESTION (Q1/Q2 split, as FINAL-16 did):
  Q1 (capacity)    -- does the route derive the CAPACITY the cold component's
                      own self-gravity saturates at, and show the self-sourced
                      configuration sits at it?
  Q2 (coefficient) -- does that capacity condition output kappa = 1/2, i.e. pin
                      a_0 against s := c sqrt(G rho_Lambda)?

ARMS (criteria in PREREGISTER.md, written alone BEFORE this script existed):
  A1  capacity identity          (predicted class IDENTITY)
  A2  branch-distinctness audit  (predicted CONFIRMED)
  A3  frozen menu of six "capacity := cosmic scale" premises (the point)
  A4  structural no-go: G_lam symmetry of the whole self-source/capacity
      structure, kappa the only charged quantity      (predicted CONFIRMED)
  A5  footing ledger with propagated errors           (reported + band-graded)

MUTATE (FINAL17_MUTATE=1): the three false twins M1/M2/M3 are asserted as true
and the band is widened to 20 % with the premise test switched off; the machinery
must be seen to let them through, which is what makes the MAIN rejections mean
something.

Registers/controls: G = 6.6743e-11, c = 2.99792458e8.
Cosmology (PRIMARY): Planck 2018 TT,TE,EE+lowE+lensing as frozen by the sibling
lane FINAL-16 PREREGISTER sec.2: H0 = 67.36 +- 0.54 km/s/Mpc, Om = 0.3153,
OL = 0.6847 +- 0.0073.  (FINAL-16 prints rho_crit,0 = 8.522730e-27,
rho_Lambda = 5.835513e-27, c sqrt(G rho_L) = 1.870954e-10.)
Cosmology (CROSS-CHECK, source-lane systematic): GF1/F05/G058 register
(deepseek_push/GF1_germ_flip/GF1_germ_flip.py, deepseek_push/F05_results.json):
rho_c = 8.533238720309458e-27, Omega_L = 0.685, a0 = 9.3619e-11,
Z = 5.788810036466141.
Errors: sigma(H0)/H0 = 0.54/67.36 (Planck 2018 -- MEMORY, flagged);
        sigma(OL)/OL = 0.0073 (MEMORY, flagged; GF1's own class is 1 %).
        G cancels EXACTLY in kappa (verified symbolically below).
"""

import os
import json
import math

import sympy as sp

# ================================================================== config
TAG = "FINAL-17 (KAPPA_A)"
MUTATE = os.environ.get("FINAL17_MUTATE", "") not in ("", "0", "false", "False")

G_SI = 6.6743e-11
C_SI = 2.99792458e8
MSUN = 1.98892e30                      # GF1 register convention
PC_M = 3.0856775814913673e16           # 1 pc in m
MPC_M = 3.0856775814913673e22          # 1 Mpc in m
MSUN_PC2 = MSUN / PC_M ** 2            # kg/m^2 per Msun/pc^2

H0_KMSMPC = 67.36
D_H0 = 0.54                            # +- 1 sigma (Planck 2018; MEMORY flagged)
OL = 0.6847
D_OL = 0.0073                          # +- 1 sigma (MEMORY flagged)
OM = 0.3153

A0_CAN = 9.3603e-11
A0_ALT = 1.1312e-10
A0_EXT = 1.20e-10                      # Lelli/McGaugh/Schombert 2017, PROVISIONAL
D_A0_EXT_RAND = 0.02e-10
D_A0_EXT_SYS = 0.24e-10

# register cross-check (GF1/F05/G058)
REG_RHOC = 8.533238720309458e-27
REG_OL = 0.685
REG_A0 = 9.3619e-11

BAND = 0.025 if not MUTATE else 0.20   # |kappa - 1/2| tolerance (5 % frozen; 20 % mutated)
FOOT_DEX = 0.0411                      # half the footing separation (FINAL-16)

checks = []


def check(name, ok, reading, measured=None):
    checks.append({"name": name, "ok": bool(ok), "measured": measured,
                   "reading": reading})
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name,
                         ("  (%s)" % measured) if measured is not None else ""))
    print("       %s" % reading)


def say(s=""):
    print(s)


# ================================================================== symbols
a0, g, lam, nu, C, G, r, M, x, n, gb, u, c, rho, H0, OmL = sp.symbols(
    'a0 g lam nu C G r M x n g_b u c rho H_0 Omega_L', positive=True)

print("=" * 100)
print("%s: does the self-source / capacity route derive kappa?" % TAG)
print("   MUTATE = %s      criteria PREREGISTER.md (written alone, pre-script)" % MUTATE)
print("=" * 100)

# ================================================================== background
H0_SI = H0_KMSMPC * 1e3 / MPC_M
RHO_CRIT = 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
RHO_L = OL * RHO_CRIT
H_LAM = math.sqrt(8 * math.pi * G_SI * RHO_L / 3)
S_UNIT = C_SI * math.sqrt(G_SI * RHO_L)          # s := c sqrt(G rho_Lambda)
R_LAM = C_SI / H_LAM

# register cosmology
REG_H0 = float(sp.sqrt(8 * sp.pi * G_SI * REG_RHOC / 3))
REG_RHO_L = REG_OL * REG_RHOC
REG_S = C_SI * math.sqrt(G_SI * REG_RHO_L)

say("\n=== BACKGROUND (SI; primary = FINAL-16 PREREGISTER sec.2 / Planck 2018) ===")
say("  H0 = %.2f +- %.2f km/s/Mpc = %.6e 1/s     c H0    = %.6e m/s^2"
    % (H0_KMSMPC, D_H0, H0_SI, C_SI * H0_SI))
say("  Om = %.4f   OL = %.4f +- %.4f" % (OM, OL, D_OL))
say("  rho_crit,0 = %.6e kg/m^3" % RHO_CRIT)
say("  rho_Lambda = %.6e kg/m^3" % RHO_L)
say("  H_Lambda   = %.6e 1/s      c H_L = %.6e m/s^2" % (H_LAM, C_SI * H_LAM))
say("  R_Lambda   = %.6e m" % R_LAM)
say("  s := c sqrt(G rho_L) = %.6e m/s^2   (the cosmic acceleration unit)" % S_UNIT)
say("  cross-check (GF1/F05 register): rho_c = %.6e, OL = %.3f, H0 = %.6e 1/s,"
    % (REG_RHOC, REG_OL, REG_H0))
say("                                  s = %.6e m/s^2  (%.4f %% high vs primary)"
    % (REG_S, 100 * (REG_S / S_UNIT - 1)))
say("  footing separation: log10(%.4e/%.4e) = %.4f dex  -> half-allowance %.4f dex"
    % (A0_ALT, A0_CAN, math.log10(A0_ALT / A0_CAN), FOOT_DEX))
say("  MEMORY-FLAGGED inputs: sigma(H0) = %.2f, sigma(OL) = %.4f (Planck 2018)."
    % (D_H0, D_OL))
say("  G cancels EXACTLY in kappa = a0 sqrt(8 pi/(3 OL))/(c H0)  [sympy-verified below]")

# ================================================================== KA controls
say("\n=== KNOWN ANSWERS (each must PASS, else the apparatus is broken) ===")

# KA-1  Z := c H_L/a0 ; Z = sqrt(32 pi/3)  <=>  kappa = 1/2  EXACTLY.
#       NOTE (audit finding): FINAL-16's KA-1 computes H_Lambda from
#       rho_ref := 4 a0^2/(c^2 G) -- a footing-DEFINED density -- so its
#       "Z = sqrt(32 pi/3) to 0.00e+00" is circular by construction.  Here we
#       use the INDEPENDENT Planck rho_Lambda, which is the only test with content.
Z_can = C_SI * H_LAM / A0_CAN
Z_ref = float(sp.sqrt(32 * sp.pi / 3))
Z_circ = float(sp.sqrt(8 * sp.pi * G_SI * (4 * A0_CAN ** 2 / (C_SI ** 2 * G_SI)) / 3)) * C_SI / A0_CAN
k_from_Z = float(sp.sqrt(8 * sp.pi / 3)) / Z_can
check("KA-1  Z and kappa are the SAME number: kappa = sqrt(8 pi/3)/Z",
      abs(k_from_Z - A0_CAN / (C_SI * math.sqrt(G_SI * RHO_L))) <= 1e-12,
      "kappa = %.12f from Z, %.12f directly (Planck rho_L) -- one statement, not two. "
      "[circular route: rho_ref := 4a0^2/(c^2G) gives Z = %.6f = sqrt(32pi/3) identically]"
      % (k_from_Z, A0_CAN / (C_SI * math.sqrt(G_SI * RHO_L)), Z_circ),
      "Z=%.6f  kappa=%.6f" % (Z_can, k_from_Z))
say("      Z(Planck rho_L) = %.6f  vs  sqrt(32 pi/3) = %.6f  ->  kappa_real = %.6f, i.e. "
    "kappa = 1/2 is off by %.3f %% (footing round-off, not a measurement)"
    % (Z_can, Z_ref, k_from_Z, 100 * (k_from_Z / 0.5 - 1)))

# KA-2  kappa per footing / per reference density
def kap(a0v, rhov):
    return a0v / (C_SI * math.sqrt(G_SI * rhov))

k_can_L = kap(A0_CAN, RHO_L)
k_can_c = kap(A0_CAN, RHO_CRIT)
k_alt_L = kap(A0_ALT, RHO_L)
k_alt_c = kap(A0_ALT, RHO_CRIT)
check("KA-2  each footing realizes kappa = 1/2 against its OWN reference density",
      abs(k_can_L - 0.5) < 2e-3 and abs(k_alt_c - 0.5) < 2e-3,
      "kappa(can vs rho_L) = %.6f ; kappa(alt vs rho_crit,0) = %.6f ; the tie "
      "alone therefore CANNOT select a footing" % (k_can_L, k_alt_c),
      "%.6f / %.6f" % (k_can_L, k_alt_c))

# KA-3  AG4 capacity-family distinctness (n=1 canonical vs n=2 quadratic)
gN = g ** 2 / (g + a0)
u_ph = g - gN
res_n1 = sp.simplify(u_ph ** 2 + 1 * gN * u_ph - a0 * gN)
res_n2 = sp.simplify(u_ph ** 2 + 2 * gN * u_ph - a0 * gN)
res_n2_id = sp.simplify(res_n2 - gN * u_ph)
check("KA-3  AG4 T7_n2_not_canonical: canonical g_ph is NOT the n=2 rest state",
      res_n1 == 0 and res_n2 != 0 and res_n2_id == 0,
      "n=1 residual = %s (canonical IS the n=1 rest state); n=2 residual = %s "
      "= gbar*g_ph != 0" % (res_n1, sp.simplify(res_n2)),
      "n1=%s n2=%s" % (res_n1, sp.simplify(res_n2)))

# KA-4  the capacity/column pair  214 / 107
sig_214 = A0_CAN / (math.pi * G_SI) / MSUN_PC2
sig_107 = A0_CAN / (2 * math.pi * G_SI) / MSUN_PC2
check("KA-4  capacity column pair: a0/(pi G) ~ 214, a0/(2 pi G) ~ 107 Msun/pc^2",
      abs(sig_214 - 214) < 3 and abs(sig_107 - 107) < 3,
      "Sigma_bar(n=1) = %.1f Msun/pc^2 (PAPER49 anchor 214); Sigma_bar(n=2) = %.1f "
      "(AG4's 107); the record's deep universal column Sigma_c = a0/(2 pi G) = %.1f"
      % (sig_214, sig_107, sig_107),
      "%.1f / %.1f" % (sig_214, sig_107))

# ================================================================== A1
say("\n=== A1: the capacity identity (graded; predicted class = IDENTITY) ===")
say("  canonical law g_N = g^2/(g+a0);  u := g - g_N  (the cold component's own field)")
i1 = sp.simplify(u_ph - a0 * g / (g + a0))
say("  (i)   u = a0*g/(g+a0)                       residual = %s" % i1)
i2 = sp.simplify((u_ph / a0).subs(g, nu * a0) - nu / (1 + nu))
say("  (ii)  u/a0 = nu/(1+nu), nu := g/a0          residual = %s   <- the SHAPE carries no a0" % i2)
i4 = sp.simplify(a0 - u_ph - a0 ** 2 / (g + a0))
say("  (iv)  a0 - u = a0^2/(g+a0)                  residual = %s   <- strict bound, u < a0" % i4)
say("  (iii) limit g->oo of u  = %s   ;  limit g->0+ of u = %s"
    % (sp.limit(u_ph, g, sp.oo), sp.limit(u_ph, g, 0, '+')))
i5 = sp.simplify(u_ph.subs({a0: lam * a0, g: lam * g}) - lam * u_ph)
say("  (v)   u(lam a0, lam g) = lam u(a0,g)        residual = %s   <- weight 1" % i5)
i6 = sp.simplify((u_ph / a0).subs({a0: lam * a0, g: lam * g}) - u_ph / a0)
say("  (vi)  (u/a0)(lam a0, lam g) = (u/a0)(a0,g)  residual = %s   <- shape INVARIANT" % i6)
ok_A1 = all(sp.simplify(v) == 0 for v in (i1, i2, i4, i5, i6))
check("A1  capacity = a0 is an IDENTITY of the law, not a determination of a0",
      ok_A1,
      "the capacity condition u -> a0 is one equation a0 = a0; (ii)+(vi) show the "
      "route's whole content is the a0-FREE shape nu/(1+nu)",
      "class=IDENTITY" if ok_A1 else "exact step failed")

# ---- the self-sourced deep branch sits AT capacity
say("\n  the self-sourced deep branch (rho_c -> a0/(2 pi G r)) sits AT the capacity:")
Mc = a0 * r ** 2 / G
dens = sp.simplify(sp.diff(Mc, r) / (4 * sp.pi * r ** 2))
say("     M_c(r) = a0 r^2/G   ->  rho_c = %s" % dens)
say("     g_c    = G M_c/r^2  = %s        (EXACTLY the capacity, for every r)" % sp.simplify(G * Mc / r ** 2))
say("     Sigma_c= M_c/(pi r^2)= %s" % sp.simplify(Mc / (sp.pi * r ** 2)))
ok_A1b = (sp.simplify(dens - a0 / (2 * sp.pi * G * r)) == 0
          and sp.simplify(G * Mc / r ** 2 - a0) == 0
          and sp.simplify(Mc / (sp.pi * r ** 2) - a0 / (sp.pi * G)) == 0)
check("A1b  the saturated self-sourced branch is at capacity with a universal column",
      ok_A1b,
      "rho_c = a0/(2 pi G r)  <=>  g_c = a0  <=>  Sigma_c = a0/(pi G): three faces "
      "of ONE statement, all a0-free in shape",
      "g_c = a0")

# ---- the self-source fixed point is degenerate in the normalisation
say("\n  the self-source fixed point, for a general amplitude C (the crux):")
self_src = sp.simplify(sp.diff(r ** 2 * (C / r), r) / r ** 2 - 4 * sp.pi * G * (C / (4 * sp.pi * G * r ** 2)))
say("     (1/r^2) d/dr (r^2 * C/r) - 4 pi G * [C/(4 pi G r^2)] = %s" % self_src)
ok_deg = self_src == 0
check("A1c  Poisson closes for EVERY amplitude C: the self-source condition fixes no scale",
      ok_deg,
      "the pair (g_c = C/r, rho_c = C/(4 pi G r^2)) is a self-consistent solution for "
      "all C > 0 -- self-sourcing is a fixed point, not a normalisation",
      "residual=%s" % self_src)

# ================================================================== A2
say("\n=== A2: branch-distinctness audit (graded; predicted CONFIRMED) ===")
say("  AG4 G3 capacity family: K W_rem'(u) = u^2/(a0 - n u)  =>  rest state u^2 + n gbar u = a0 gbar")
t7 = sp.simplify(sp.expand((2 * gb * u + u ** 2) - (a0 * gb + (2 - n) * gb * u)
                           - (u ** 2 + n * gb * u - a0 * gb)))
say("     T7: (g^2-gbar^2) - [a0 gbar + (2-n) gbar u]  ==  rest-state equation : residual = %s" % t7)
u_root = sp.solve(sp.Eq(u ** 2 + n * gb * u, a0 * gb), u)[0]
say("     positive root u(gbar) = %s" % sp.simplify(u_root))
cap_n = sp.limit(u_root, gb, sp.oo)
say("     capacity (gbar -> oo) = %s   ->  a0 (n=1)  vs  a0/2 (n=2)" % cap_n)
say("     columns in AG4's convention Sigma_bar = capacity/(pi G):")
say("        n=1 (canonical) : %.1f Msun/pc^2   [PAPER49 Sigma_bar_max = 214]" % sig_214)
say("        n=2 (quadratic) : %.1f Msun/pc^2   [AG4's '107 in the same convention']" % sig_107)
ok_A2 = (t7 == 0 and sp.simplify(cap_n - a0 / n) == 0
         and res_n1 == 0 and res_n2 != 0)
flag_107 = abs(sig_107 - 107) < 3
check("A2  the two branches are certified distinct; capacity = a0/n",
      ok_A2,
      "n=1 <=> canonical g^2 = gbar(g+a0); n=2 <=> quadratic g^2 - gbar^2 = a0 gbar; "
      "the canonical g_ph leaves residual gbar*g_ph in the n=2 equation",
      "capacity = a0/n")
if flag_107:
    say("  [TRAP FLAGGED, not used] the record's deep universal column "
        "Sigma_c = a0/(2 pi G) = %.1f Msun/pc^2" % sig_107)
    say("     is NUMERICALLY the n=2 (quadratic) capacity ceiling, not the canonical "
        "one (%.1f)." % sig_214)
    say("     Using it to argue for kappa = 1/2 in the CANONICAL branch is a branch mix.")

# ================================================================== A3
say("\n=== A3: the derivation attempt -- capacity := a cosmic scale (graded; THE POINT) ===")
say("  The capacity condition outputs a_0.  kappa needs a_0 pinned against s = c sqrt(G rho_L).")
say("  The only way the route can do that is an added premise of the form")
say("      capacity := (dimensionless) x (an acceleration built from c, G, rho_Lambda alone).")
say("  Frozen menu of six such premises (no item added or dropped after the run):")
say("")
arms = [
    ("C1", "c^2/R_Lambda = c H_Lambda", C_SI ** 2 / R_LAM, 0),
    ("C2", "4 pi G rho_L R_Lambda/3 = c H_Lambda/2", 4 * math.pi * G_SI * RHO_L * R_LAM / 3, 0),
    ("C3", "c H_Lambda/(2 pi)   [Milgrom form]", C_SI * H_LAM / (2 * math.pi), 0),
    ("C4", "pi G rho_L R_Lambda  [cosmic column]", math.pi * G_SI * RHO_L * R_LAM, 0),
    ("C5", "pi G rho_L R_Lambda/2 [half column]", math.pi * G_SI * RHO_L * R_LAM / 2, 0),
    ("C6", "c^2/(2 pi R_Lambda)  [circumference reading of C3]", C_SI ** 2 / (2 * math.pi * R_LAM), 0),
]
# relative error on kappa (same for every arm: kappa = capacity/s, s carries the cosmology)
rel_H0 = D_H0 / H0_KMSMPC
rel_OL = D_OL / (2 * OL)
rel_k = math.sqrt(rel_H0 ** 2 + rel_OL ** 2)
say("      error propagation: kappa = a0 sqrt(8 pi/(3 OL))/(c H0);  G cancels EXACTLY")
say("         d ln kappa/d ln a0 = +1, d ln kappa/d ln H0 = -1, d ln kappa/d ln OL = -1/2")
say("         sigma(kappa)/kappa = sqrt((%.4f)^2 + (%.4f)^2) = %.4f %%"
    % (rel_H0, rel_OL, 100 * rel_k))
say("         (sympy: d ln kappa/d ln a0 = %s ; d ln kappa/d ln H0 = %s ; d ln kappa/d ln OL = %s)"
    % (sp.simplify(sp.diff(sp.log(a0 * sp.sqrt(8 * sp.pi / (3 * OmL)) / (c * H0)), a0) * a0),
       sp.simplify(sp.diff(sp.log(a0 * sp.sqrt(8 * sp.pi / (3 * OmL)) / (c * H0)), H0) * H0),
       sp.simplify(sp.diff(sp.log(a0 * sp.sqrt(8 * sp.pi / (3 * OmL)) / (c * H0)), OmL) * OmL)))
kap_arms = {}
say("      id   premise                                             kappa        sigma       a0 implied")
for aid, desc, cap, _ in arms:
    kv = cap / S_UNIT
    kap_arms[aid] = kv
    say("      %s   %-44s %9.6f   %.6f   %.5e" % (aid, desc, kv, kv * rel_k, kv * S_UNIT))
say("")
ks = sorted(kap_arms.values())
span_dex = math.log10(ks[-1] / ks[0])
say("      menu span = log10(%.6f/%.6f) = %.4f dex   (PREREGISTER predicted ~0.923 dex;"
    % (ks[-1], ks[0], span_dex))
say("         the frozen menu tops out at C1 and C6 duplicates C3, so the actual span is"
    " 0.798 dex;")
say("         the prediction was made against a menu draft that still carried a "
    "0.3455 arm -- recorded as a pre-registration bookkeeping miss, not a result.)")
say("      nearest arm to 1/2: C3/C6 at %.6f, |dkappa| = %.6f = %.3f x the %.3f band"
    % (kap_arms["C3"], abs(kap_arms["C3"] - 0.5), abs(kap_arms["C3"] - 0.5) / 0.025, 0.025))
band_hits = [k for k, v in kap_arms.items() if abs(v - 0.5) <= BAND]
say("      arms inside the %s band: %s" % ("5 %%" if not MUTATE else "20 %% (MUTATED)",
                                           band_hits if band_hits else "NONE"))
ok_A3 = (len(band_hits) == 0) and (span_dex > FOOT_DEX)
check(("A3  NO ARM PASSES: no arm lands in the 5%% band, and the menu is %.1fx too free"
       % (span_dex / FOOT_DEX)) if not MUTATE else
      ("A3  MUTATED: band widened to 20%%; arms inside = %s" % band_hits),
      ok_A3,
      "the nearest arm misses by %.6f (%.4f dex); the frozen menu spans %.4f dex "
      "against the %.4f dex the route would need to discriminate a footing"
      % (abs(kap_arms["C3"] - 0.5), math.log10(0.5 / kap_arms["C3"]), span_dex, FOOT_DEX),
      "span=%.4f dex" % span_dex)

# ================================================================== A4
say("\n=== A4: the structural no-go (graded; predicted CONFIRMED) ===")
say("  G_lam :  a0 -> lam a0,  g -> lam g,  g_N -> lam g_N,  u -> lam u ;")
say("           c, G, rho_Lambda, M_b, r  FIXED.  kappa -> lam kappa.")
a4 = {}
# (i) the law
a4["law"] = sp.simplify((lam * g) ** 2 / (lam * g + lam * a0) - lam * (g ** 2 / (g + a0)))
# (ii) u
a4["u"] = i5
# (iii) capacity bound: a0 - u  weight 1
a4["bound"] = sp.simplify((lam * a0 - (lam * g - (lam * g) ** 2 / (lam * g + lam * a0)))
                          - lam * (a0 - u_ph))
# (iv) Poisson in the self-sourced branch, C := sqrt(G M_b a0)  ->  lam^{1/2} both sides
Cv = sp.sqrt(G * M * a0)
rho_c = Cv / (4 * sp.pi * G * r ** 2)
a4["poisson"] = sp.simplify((sp.diff(r ** 2 * (Cv / r), r) / r ** 2 - 4 * sp.pi * G * rho_c)
                            .subs({a0: lam * a0}))
a4["poisson_w"] = sp.simplify(
    (sp.sqrt(G * M * (lam * a0)) / (4 * sp.pi * G * r ** 2))
    - sp.sqrt(lam) * (Cv / (4 * sp.pi * G * r ** 2)))
# (v) hydrostatic closure sigma^2 = C/2 and the ratio sigma^2/v_flat^2 -- weight 0
a4["sigma_ratio"] = sp.simplify(
    ((sp.sqrt(G * M * (lam * a0)) / 2) / sp.sqrt(G * M * (lam * a0)))
    - ((Cv / 2) / Cv))
# (vi) deep universal column  weight 1
a4["column"] = sp.simplify(((lam * a0) / (2 * sp.pi * G)) - lam * (a0 / (2 * sp.pi * G)))
# (vii) deficiency  weight 1
a4["defic"] = a4["bound"]
for kk in ("law", "u", "bound", "poisson", "sigma_ratio", "column", "defic"):
    say("  (%s)  residual under G_lam (0 = covariant) : %s" % (kk, a4[kk]))
say("  Poisson weight: rho_c carries lam^{1/2} (C := sqrt(G M_b a0)) -> residual %s" % a4["poisson_w"])
say("")
say("  kappa = a0/(c sqrt(G rho_Lambda)) is the ONLY G_lam-charged quantity:")
say("     kappa -> lam * kappa, while {X, sigma^2/v_flat^2, u/a0, c, G, rho_L, M_b} are all")
say("     invariant.  There is no G_lam-invariant left in the route's data to fix the orbit.")
say("     The capacity statement 'sup u = a0' has weight 1: it is the equation a0 = a0.")
say("")
say("  numeric orbit (observationally identical histories, kappa the only difference):")
say("     lam      a0 [m/s^2]   capacity   sigma^2/v_f^2   Sigma_c [Msun/pc^2]   kappa")
for lv in (0.5, 1.0, 2.0):
    say("     %5.2f   %.5e   %.5e      0.5          %.1f              %.4f"
        % (lv, A0_CAN * lv, A0_CAN * lv, sig_214 * lv, 0.5 * lv))
ok_A4 = all(sp.simplify(v) == 0 for v in a4.values()) and sp.simplify(a4["poisson_w"]) == 0
check("A4  NO-GO CONFIRMED: kappa is a flat direction of the self-source/capacity route",
      ok_A4,
      "every relation of the route is G_lam-covariant; the capacity, the column and the "
      "closure ratio all carry the SAME weight as a0, so none of them can evaluate a0",
      "all residuals 0")

# ================================================================== A5
say("\n=== A5: the footing ledger, computed not assumed (band-graded) ===")
kap_can_L = k_can_L
kap_alt_L = k_alt_L
kap_ext_L = kap(A0_EXT, RHO_L)
say("     a_0 source                     a_0 [m/s^2]     rho used        kappa         +-1sigma")
say("     footing 'can' (canonical)      %.5e    rho_L     %.6f   %.6f" % (A0_CAN, kap_can_L, kap_can_L * rel_k))
say("     footing 'alt'                  %.5e    rho_L     %.6f   %.6f" % (A0_ALT, kap_alt_L, kap_alt_L * rel_k))
say("     footing 'can'                  %.5e    rho_c0    %.6f" % (A0_CAN, k_can_c))
say("     footing 'alt'                  %.5e    rho_c0    %.6f" % (A0_ALT, k_alt_c))
say("     external RAR (PROVISIONAL)     %.5e    rho_L     %.6f   %.4f rand / %.4f sys"
    % (A0_EXT, kap_ext_L, kap_ext_L * D_A0_EXT_RAND / A0_EXT, kap_ext_L * D_A0_EXT_SYS / A0_EXT))
say("")
say("     source-lane systematic: kappa(can vs rho_L) = %.6f (FINAL-16/Planck-67.36)"
    % kap_can_L)
say("                             kappa(can vs rho_L) = %.6f (GF1/F05 register cosmo) "
    "-> %.5f dex" % (A0_CAN / REG_S, math.log10(kap_can_L / (A0_CAN / REG_S))))
say("")
say("     footing separation: kappa_alt/kappa_can = %.6f  ->  %.4f dex (half-allowance %.4f dex)"
    % (kap_alt_L / kap_can_L, math.log10(kap_alt_L / kap_can_L), FOOT_DEX))
say("")
say("     distance of the nearest arm (C3/C6, kappa = %.6f) from each footing:"
    % kap_arms["C3"])
d_can = math.log10(kap_can_L / kap_arms["C3"])
d_alt = math.log10(kap_alt_L / kap_arms["C3"])
say("        vs canonical (%.6f): %.4f dex   %s" % (kap_can_L, d_can,
                                                    "INSIDE the 0.0411 dex half-allowance"
                                                    if d_can < FOOT_DEX else "outside"))
say("        vs alt       (%.6f): %.4f dex   %s" % (kap_alt_L, d_alt,
                                                    "inside" if d_alt < FOOT_DEX else "OUTSIDE"))
say("        a_0 the arm implies: %.5e m/s^2 (canonical is %.4f dex above it, alt %.4f dex)"
    % (kap_arms["C3"] * S_UNIT, d_can, d_alt))
say("")
say("     FOOTING RULE (frozen in PREREGISTER sec.3 A5): the route selects a footing only")
say("     if some A3 arm BOTH lands inside |kappa - 1/2| <= 0.025 AND has its premise derived")
say("     from the route.  No arm clears (i) -- nearest misses by %.6f = %.3f x the band --"
    % (abs(kap_arms["C3"] - 0.5), abs(kap_arms["C3"] - 0.5) / 0.025))
say("     and no arm clears (ii) -- C3 is menu item 3, a choice.  Hence: SELECTS NEITHER.")
ok_A5 = abs(kap_can_L - 0.5) < 2e-3 and abs(kap_alt_L - 0.5) > 0.05
check("A5  the tie selects the canonical footing by DEFINITION and excludes the alt footing",
      ok_A5,
      "kappa(can vs rho_L) = %.6f +- %.6f ; kappa(alt vs rho_L) = %.6f +- %.6f, i.e. %.4f dex "
      "away (3.3x the 5 %% band in dex terms).  The alt footing reaches kappa = 1/2 only by "
      "swapping rho_L -> rho_crit,0, which is a definition."
      % (kap_can_L, kap_can_L * rel_k, kap_alt_L, kap_alt_L * rel_k,
         math.log10(kap_alt_L / kap_can_L)),
      "can=%.6f alt=%.6f" % (kap_can_L, kap_alt_L))

# ================================================================== MUTATE
say("\n=== MUTATE: three false twins, each must be REJECTED by the same machinery ===")
def twin(name, claim_ok, why):
    # MAIN  (MUTATE=False): PASS iff the twin is REJECTED by the frozen machinery.
    # MUTATE(True)        : PASS iff the twin slips through the MUTATED machinery,
    #                       i.e. the rejection was machinery-driven, not cosmetic.
    tag = "ACCEPTED" if claim_ok else "REJECTED"
    ok = bool(claim_ok) == bool(MUTATE)
    print("[%s] %s" % ("PASS" if ok else "FAIL", name))
    print("       %s" % why)
    checks.append({"name": name, "ok": ok, "measured": tag, "reading": why})
    return claim_ok

twin("M1  'the Milgrom-form capacity derives kappa = 1/2'",
     abs(kap_arms["C3"] - 0.5) <= BAND,
     "C3 gives kappa = %.6f +- %.6f; |dkappa| = %.6f vs band %.3f (%.2f x)%s; and the "
     "premise is menu item C3, a choice, not a derived condition"
     % (kap_arms["C3"], kap_arms["C3"] * rel_k, abs(kap_arms["C3"] - 0.5), BAND,
        abs(kap_arms["C3"] - 0.5) / 0.025,
        "" if not MUTATE else "  [BAND MUTATED TO 0.20: the twin slips through]"))

twin("M2  'Sigma_c = a0/(2 pi G) ~ 107 confirms kappa = 1/2 via the half-capacity'",
     (abs(sig_107 - 107) < 3) and (abs(kap_arms["C3"] - 0.5) <= BAND),
     "107 is the n=2 (QUADRATIC) capacity ceiling in AG4's convention; the canonical "
     "ceiling is %.1f.  The equality is an identity of the column convention and carries "
     "no cosmology -- AG4 certifies the two branches as DIFFERENT THEORIES" % sig_214)

twin("M3  'kappa = 1/2 is a measurement, realized on the alt footing too'",
     abs(kap_alt_L - 0.5) <= BAND,
     "kappa(alt vs rho_L) = %.6f +- %.6f: %.4f dex from canonical's %.6f.  The alt footing "
     "realizes 1/2 only by swapping the reference density to rho_crit,0 (kappa = %.6f), "
     "which is a definition%s"
     % (kap_alt_L, kap_alt_L * rel_k, math.log10(kap_alt_L / kap_can_L), kap_can_L, k_alt_c,
        "" if not MUTATE else "  [BAND MUTATED TO 0.20: the twin slips through]"))

say("")
say("  MUTATE VERDICT: %s" % ("PASS (the machinery can be fooled only by disabling it: "
                              "the 20 % band and the premise test are what let the twins through)"
                              if MUTATE else
                              "MAIN: all three twins rejected by the frozen machinery"))

# ================================================================== summary
say("")
say("=" * 100)
say("SUMMARY")
say("=" * 100)
failing = [c["name"] for c in checks if not c["ok"]]
say("  checks: %d, failing: %s" % (len(checks), failing if failing else "NONE"))
say("  A1  capacity identity                    = IDENTITY (u = a0 g/(g+a0); shape a0-free)")
say("  A1b saturated self-sourced branch        = g_c = a0 exactly, Sigma_c = a0/(pi G)")
say("  A1c self-source fixed point              = degenerate in C (no normalisation)")
say("  A2  branch distinctness (AG4)            = CONFIRMED (n=1 canonical, n=2 quadratic)")
say("  A3  menu freedom                         = %.4f dex vs %.4f dex allowance (%.1fx)" %
    (span_dex, FOOT_DEX, span_dex / FOOT_DEX))
say("      nearest arm C3/C6                    = kappa %.6f +- %.6f (%.4f dex from 1/2)" %
    (kap_arms["C3"], kap_arms["C3"] * rel_k, math.log10(0.5 / kap_arms["C3"])))
say("  A4  no-go (G_lam symmetry, kappa flat)   = %s" % ok_A4)
say("  A5  kappa(can vs rho_L)                  = %.6f +- %.6f" % (kap_can_L, kap_can_L * rel_k))
say("      kappa(alt vs rho_L)                  = %.6f +- %.6f  (%.4f dex)" %
    (kap_alt_L, kap_alt_L * rel_k, math.log10(kap_alt_L / kap_can_L)))
say("      footing selected                     = NEITHER (no A3 arm is derived)")
say("")
if ok_A1 and ok_A1b and ok_deg and ok_A2 and ok_A4 and not band_hits:
    label = "KAPPA NOT DERIVED (FITTED) -- CAPACITY DERIVED"
elif not (ok_A1 and ok_A1b and ok_A2):
    label = "OPEN (a known answer or an exact step failed)"
else:
    label = "KAPPA DERIVED (CAPACITY)"
say("  LANE LABEL: %s" % label)
say("     Q1 (capacity)    = DERIVED  : the cold component's own field saturates at a_0,")
say("                                   the self-sourced branch sits AT it (g_c = a_0),")
say("                                   and the universal column is a_0/(pi G) ~ 214;")
say("                                   AG4's n=2 half-capacity (107) is a DIFFERENT branch.")
say("     Q2 (kappa = 1/2) = NO       : the capacity condition is the equation a_0 = a_0;")
say("                                   the whole route is G_lam-covariant with kappa the only")
say("                                   charged quantity (A4); the frozen cosmic-scale menu spans")
say("                                   %.4f dex against a %.4f dex allowance (A3)." % (span_dex, FOOT_DEX))

RESULTS = {
    "lane": "FINAL-17 KAPPA_A",
    "mutate": bool(MUTATE),
    "label": label,
    "Q1_capacity": "DERIVED",
    "Q2_coefficient": "NOT DERIVED",
    "A1_identity": bool(ok_A1),
    "A1b_saturated_branch": bool(ok_A1b),
    "A1c_fixed_point_degenerate": bool(ok_deg),
    "A2_branch_distinct": bool(ok_A2),
    "A3_band_hits": band_hits,
    "A3_span_dex": span_dex,
    "A3_allowance_dex": FOOT_DEX,
    "A3_arms": {k: {"kappa": v, "sigma": v * rel_k} for k, v in kap_arms.items()},
    "A3_nearest": {"id": "C3/C6", "kappa": kap_arms["C3"],
                   "sigma": kap_arms["C3"] * rel_k,
                   "abs_miss": abs(kap_arms["C3"] - 0.5),
                   "dex_miss": math.log10(0.5 / kap_arms["C3"])},
    "A4_nogo": bool(ok_A4),
    "A5_kappa_can_vs_rhoL": {"value": kap_can_L, "sigma": kap_can_L * rel_k},
    "A5_kappa_alt_vs_rhoL": {"value": kap_alt_L, "sigma": kap_alt_L * rel_k},
    "A5_kappa_can_vs_rhocrit": k_can_c,
    "A5_kappa_alt_vs_rhocrit": k_alt_c,
    "A5_kappa_ext_vs_rhoL": {"value": kap_ext_L,
                             "rand": kap_ext_L * D_A0_EXT_RAND / A0_EXT,
                             "sys": kap_ext_L * D_A0_EXT_SYS / A0_EXT},
    "A5_footing_dex": math.log10(kap_alt_L / kap_can_L),
    "A5_footing_selected": "NEITHER",
    "rel_kappa": rel_k,
    "s_unit": S_UNIT,
    "rho_Lambda": RHO_L,
    "columns": {"n1_canonical_214": sig_214, "n2_quadratic_107": sig_107},
    "checks": checks,
}
base = "final17_MUTATE" if MUTATE else "final17"
with open(base + ".json", "w") as fh:
    json.dump(RESULTS, fh, indent=2, default=str)
say("\n  wrote %s.json" % base)
say("  exit=%d (%s)" % (1 if failing else 0,
                        "mutation arm fired" if (failing and MUTATE) else
                        ("all pre-registered verdicts landed" if not failing else
                         "UNEXPECTED failure")))
raise SystemExit(1 if failing else 0)
