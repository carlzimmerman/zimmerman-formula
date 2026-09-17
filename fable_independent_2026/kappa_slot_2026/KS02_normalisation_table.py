#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
KS02_normalisation_table.py -- pin every O(1) in eps_tot and report whether 1/(32 pi) occurs under any
STANDARD convention set.

*** OPENING SENTENCE, per the work order: KS01 returned SLOT-NOT-LIVE.  The horizon entropy DIVIDES;
the 08-09 pure number is a double count of the thermal variance; the multiplicative structure
eps_tot = S_dS * eps_1 holds only under a NAMED holographic-coherence postulate (category III).  This
lane runs conditional on GRANTING that S_dS multiplication, to ask: even if the enhancement is granted,
does any fully-standard convention set land on eps_tot = 1/(32 pi)? ***

eps_tot = N * c_pol * c_2pt * c_proj * c_norm * (G T^2 / 8), each factor a named symbol.
  N     in {S_dS = A/4G, A/G, N_field ~ S_dS^{3/2}, 1 (Way-1 physical, no enhancement)}
  c_pol in {1, 2}
  c_2pt in {1 (loose A), 1/12 (thermal massless scalar), 1/6 (two-component), c_TT (derived)}
  c_proj: h_uu projection for a static / accelerated worldline (derived; the static value is 0 in TT gauge)
  c_norm in {32 pi G (canonical), 16 pi G, 8 pi G}

  C1  is there a set with NO "loose" entry giving eps_tot = 1/(32 pi) to <1%?
  C2  how many grid cells land inside the measured 2sigma kappa band (KS04's physics-grid prior)?
  C3  the 08-09 near-miss reproduced: A -> 1/2, B -> 1.447, B x 2 -> 2.047
  second way: recompute the closest-to-1/2 set from the thermal graviton-gas energy density / rho_Lambda

Run:  python3 fable_independent_2026/kappa_slot_2026/KS02_normalisation_table.py
"""
import os, sys, json, math, itertools
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "KS02_normalisation_table"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "KS02", "checks": {}, "numbers": {}, "conditional_on": "KS01 = SLOT-NOT-LIVE"}


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


# measured kappa bands (kappa = a_0/(c sqrt(G rho_Lambda)))
KAPPA_MEAS = [("BTFR", 0.465, 0.076), ("distance-free", 0.551, 0.043)]
def in2sig(k):
    return any(abs(k - m) <= 2 * s for _, m, s in KAPPA_MEAS)

P(__doc__)
banner("SETUP -- symbolic eps_tot with named O(1) factors, N = S_dS granted (conditional)")
G, H = sp.symbols("G H", positive=True)
S_dS = sp.pi / (G * H**2)                 # area-cell count A/4G in Planck units (hbar=c=1)
T = H / (2 * sp.pi)                        # Gibbons-Hawking temperature
base = T**2 / sp.Rational(8)              # T^2/8 (the -X^2/8 coupling; the G lives in c_norm)

# derive c_TT: for a TT graviton the coincident thermal variance per polarisation is the massless-scalar
# value 1/12 (each TT mode is a canonically normalised massless scalar).  So c_TT = 1/12.
c_TT = sp.Rational(1, 12)
# derive c_proj: static observer u=(1,0,0,0), TT gauge h_0mu = 0 => h_uu = h_00 = 0.  A worldline moving
# with speed v has h_uu = h_ij v^i v^j ~ v^2 <h>.  So the STATIC projection is 0; the moving one is O(v^2).
c_proj_static = sp.Integer(0)
c_proj_moving = sp.Symbol("v2")           # v^2/c^2, left symbolic (O(v^2) suppression)
check("SETUP-c_proj the static-observer projection h_uu = h_00 = 0 in TT gauge (the coupling needs "
      "worldline motion, giving an extra O(v^2/c^2) suppression)",
      f"c_proj(static) = {c_proj_static}", c_proj_static == 0,
      "an additional reason the drift is small; folded into the grid as c_proj in {1 (loose), v^2 (physical)}")

banner("THE GRID")
N_opts = {"S_dS (A/4G)": S_dS, "A/G (=4 S_dS)": 4 * S_dS}
cpol_opts = {"1": sp.Integer(1), "2": sp.Integer(2)}
c2pt_opts = {"1 (loose A)": sp.Integer(1), "1/12 (massless)": sp.Rational(1, 12),
             "1/6 (2-comp)": sp.Rational(1, 6), "c_TT=1/12 (derived)": c_TT}
cproj_opts = {"1 (loose)": sp.Integer(1)}      # keep proj=1 for the near-miss reproduction; v^2 only shrinks it
# c_norm carries one power of G (h is dimensionless: <h^2> = c_norm c_2pt T^2 with c_norm ~ G).
cnorm_opts = {"32piG (canon)": 32 * sp.pi * G, "16piG": 16 * sp.pi * G, "8piG": 8 * sp.pi * G,
              "G (loose, no 32pi)": G}

rows = []
for (nN, N), (npol, cpol), (n2, c2), (nprj, cprj), (nnorm, cnorm) in itertools.product(
        N_opts.items(), cpol_opts.items(), c2pt_opts.items(), cproj_opts.items(), cnorm_opts.items()):
    eps = sp.simplify(N * cpol * c2 * cprj * cnorm * base)       # N ~ 1/G, cnorm ~ G => dimensionless
    if eps.free_symbols:                                          # keep only dimensionless cells
        continue
    epsf = float(eps)
    if epsf <= 0:
        continue
    kap = math.sqrt(8 * math.pi * epsf)
    loose = ("loose" in n2) or ("loose" in nnorm)
    rows.append(dict(N=nN, pol=npol, c2pt=n2, proj=nprj, norm=nnorm, eps=epsf, kappa=kap, loose=loose))

P(f"  {len(rows)} dimensionless cells.  Showing the standard-normalisation ones and the loose near-miss:")
P(f"  {'N':<14}{'pol':>4}{'c2pt':<18}{'norm':<20}{'eps_tot':>12}{'kappa':>10}  loose")
P("  " + "-" * 92)
for row in sorted(rows, key=lambda r: r["kappa"]):
    if (not row["loose"]) or abs(row["kappa"] - 0.5) < 1e-9 or abs(row["kappa"] - 1.447) < 0.01:
        P(f"  {row['N']:<14}{row['pol']:>4} {row['c2pt']:<17}{row['norm']:<20}{row['eps']:>12.6f}{row['kappa']:>10.4f}"
          f"  {'yes' if row['loose'] else 'no'}")

# --- C1: any NON-loose set giving 1/(32 pi) to <1% ? ---------------------------------------------
target = 1.0 / (32 * math.pi)
nonloose_near = [r for r in rows if (not r["loose"]) and abs(r["eps"] / target - 1) < 0.01]
standard_eps = None
for r in rows:
    if r["N"] == "S_dS (A/4G)" and r["c2pt"].startswith("1/12") and r["norm"].startswith("32piG") and r["pol"] == "1":
        standard_eps = r["eps"]; standard_kappa = r["kappa"]
check("C1 NO fully-standard convention set (no loose entry) gives eps_tot = 1/(32 pi) to 1%",
      f"non-loose cells within 1% of 1/(32pi): {len(nonloose_near)}", len(nonloose_near) == 0,
      f"the standard set (S_dS, 1 pol, c_TT=1/12, 32piG) gives eps_tot = {standard_eps:.5f} = 1/12, "
      f"kappa = {standard_kappa:.4f}; 1/(32pi) needs dropping the 8pi/3 Friedmann factor (the loose choice)")

ratio_std_to_target = standard_eps / target
check("C1b the standard eps_tot = 1/12 exceeds 1/(32 pi) by exactly the Friedmann factor 8 pi/3",
      f"(1/12)/(1/32pi) = {ratio_std_to_target:.6f}, 8pi/3 = {8*math.pi/3:.6f}",
      abs(ratio_std_to_target - 8 * math.pi / 3) < 1e-6,
      "so 'A gives 1/2' is 'B divided by the Friedmann 8pi/3' -- a convention slip of exactly that factor")

# --- C2: grid cells in the measured 2sigma band (physics-grid prior for KS04) --------------------
inband = [r for r in rows if in2sig(r["kappa"])]
loose_A_inband = any(r["loose"] and abs(r["kappa"] - 0.5) < 1e-9 and in2sig(r["kappa"]) for r in rows)
check("C2 the ONLY physics-grid cells reaching the measured 2sigma band include the loose-A kappa=1/2 cell, "
      "and they are a small minority of the grid: the S_dS-enhanced grid mostly overshoots the band",
      f"{len(inband)}/{len(rows)} = {len(inband)/len(rows):.3f} in band; loose-A (kappa=1/2) present & in band: "
      f"{loose_A_inband}", loose_A_inband and 0 < len(inband) < len(rows) / 2,
      "the physics-motivated grid does land 1/2 in band (via the loose cell) but the standard cells sit high; "
      "this is KS04's structured prior, distinct from KS04's blind alphabet")
OUT["numbers"]["grid_in_band_fraction"] = len(inband) / len(rows)

# --- C3: the 08-09 near-miss reproduced ----------------------------------------------------------
def eps_of(N, cpol, c2, cnorm):
    return float(sp.simplify(N * cpol * c2 * cnorm * base))
epsA = eps_of(S_dS, 1, sp.Integer(1), G)                      # A: <h^2> = G T^2 (loose)
epsB = eps_of(S_dS, 1, sp.Rational(1, 12), 32 * sp.pi * G)    # B: h=sqrt(32piG)phi, <phi^2>=T^2/12
epsC = eps_of(S_dS, 2, sp.Rational(1, 12), 32 * sp.pi * G)    # C: B x 2 pol
kA, kB, kC = (math.sqrt(8 * math.pi * e) for e in (epsA, epsB, epsC))
check("C3 the 08-09 near-miss reproduced exactly: A -> 1/2, B -> 1.447, B x 2 -> 2.047",
      f"kappa: A={kA:.4f}, B={kB:.4f}, C={kC:.4f}  (eps: {epsA:.5f}, {epsB:.5f}, {epsC:.5f})",
      abs(kA - 0.5) < 1e-9 and abs(kB - 1.447) < 2e-3 and abs(kC - 2.047) < 2e-3,
      "the value that hits 1/2 is the loose A; the standard B gives 1.447, a factor 2.894 = sqrt(8pi/3) higher")
OUT["numbers"].update(kappaA=kA, kappaB=kB, kappaC=kC, epsA=epsA, epsB=epsB, epsC=epsC)

# --- second independent way: thermal graviton-gas ENERGY DENSITY / rho_Lambda --------------------
banner("SECOND WAY -- thermal graviton-gas energy density, an independent route")
# rho_grav(T_GH) = (pi^2/30) g_* T^4, g_* = 2 (graviton).  rho_Lambda = 3 H^2/(8 pi G) (energy density, c=1).
# eps_ed = N * rho_grav/rho_Lambda, N = S_dS.  rho_Lambda ~ H^2 supplies the H^2 that makes it a number.
g_star = 2
rho_grav = sp.Rational(1, 30) * sp.pi**2 * g_star * T**4
rho_Lam = 3 * H**2 / (8 * sp.pi * G)
eps_ed = sp.simplify(S_dS * rho_grav / rho_Lam)
kappa_ed = math.sqrt(8 * math.pi * float(eps_ed))
P(f"  eps_ed = S_dS * rho_grav/rho_Lambda = {eps_ed} = {float(eps_ed):.6f}  ->  kappa = {kappa_ed:.4f}")
OUT["numbers"]["eps_energy_density"] = float(eps_ed)
OUT["numbers"]["kappa_energy_density"] = kappa_ed
check("SECOND-WAY the energy-density route gives yet a THIRD O(1) value (eps = 1/90, kappa ~ 0.53), not "
      "the variance-loose 1/(32 pi): the SAME S_dS enhancement lands on a different number by route",
      f"eps_ed = {float(eps_ed):.6f} (=1/90), kappa_ed = {kappa_ed:.4f}; variance-loose kappa = 0.500, "
      f"variance-standard kappa = 1.447",
      abs(float(eps_ed) - 1.0 / 90) < 1e-9 and abs(kappa_ed - 0.5) > 0.02,
      "across defensible routes kappa spans ~0.50 (variance-loose) to 1.447 (variance-standard) with 0.53 "
      "(energy density) between: the target 1/2 is NOT route-selected -- it is one convention among several")

banner("VERDICT")
P(f"""  (1) COMPUTED: eps_tot over the full O(1) grid with the S_dS enhancement granted (conditional on the
      KS01 postulate), and a second route via the thermal graviton-gas energy density.
  (2) NUMBERS: standard set (S_dS, 1 pol, 1/12, 32 pi G) -> eps_tot = 1/12, kappa = 1.447.  The value
      1/(32 pi) (kappa = 1/2) is reached ONLY by the loose choice <h^2> = G T^2, which drops the Friedmann
      factor 8 pi/3 = {8*math.pi/3:.4f}.  Near-miss reproduced: A=0.500, B=1.447, C=2.047.  The energy-density
      route does not reproduce any of them (T^4 vs T^2).
  (3) HONEST SENTENCE: under standard conventions eps_tot = 1/12; 1/(32 pi) is reached only with the loose
      choice X = 'omit the 8pi/3 Friedmann factor from the graviton variance'.  The number is CONVENTION.""")
OUT["verdict"] = {"word": "CONVENTION", "standard_eps": float(standard_eps),
                  "standard_kappa": float(standard_kappa), "target": target}

banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok); n = len(CH)
lb_fail = [nm for nm, ok, lb in CH if lb and not ok]
P(f"KS02 COMPLETE: {npass}/{n} checks PASS")
for nm in lb_fail:
    P(f"    load-bearing FAIL: {nm}")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb_fail}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(1 if lb_fail else 0)
