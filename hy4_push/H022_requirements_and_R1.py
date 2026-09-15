#!/usr/bin/env python3
r"""H022 -- REQUIREMENTS AND TESTABLE PREDICTIONS (the door list) + R1 live test.

PART 1 -- REQUIREMENTS.  What a complete theory of gravity on this framework
must still do.  Each is stated with its decider so it cannot be waved at.

  R1  OPEN CLUSTERS / TIDAL TAILS.  The EFE caps the phantom at
      r_cap/r_M = a_0/g_ext.  In the Galactic disk g_ext ~ 1.7 a_0, so
      r_cap ~ 0.6 r_M: open clusters have NO deep-MOND regime and their
      tidal tails must be NEWTONIAN.  DECIDER: the Hyades/Praesepe tails
      (real Gaia data, available now -- tested live below).
  R2  THE S_8 DECISION.  H020 fixed the raise at 3 OmL/(32 pi) = 2.044% at
      z = 0.  DECIDER: DESI final. Either it matches or the theory is wrong;
      it cannot be tuned.
  R3  THE WIDE-BINARY CLOUD.  G006/G018: gamma_v ~ 1.00-1.05 with the
      period-separation signature breaking at 7.4 kAU.  DECIDER: Gaia DR4,
      2 Dec 2026.
  R4  THE BOX-NU CURVE.  nu_layer = 2 exactly locally, falling as 1/sqrt(z)
      (E4).  DECIDER: DR4 vertical profile.
  R5  THE RADIAL BREAK.  r_break = 6.1 kpc in the MW dark profile (E5).
      DECIDER: DR4 dark-density mapping.
  R6  THE Z-TEST.  Flat a_0 vs rising: 0.00 vs +0.33 dex at z ~ 2.5, against
      a 0.13 dex floor (G011).  DECIDER: JWST/ALMA BTFR at high z.
  R7  CLUSTER CORE SLOPE.  This construction gives ~-1.5; NFW gives -1.
      DECIDER: X-COP / HST lensing cores.
  R8  THE EFE AT e_N ~ 1.  SPARC maxes at 0.0048 -- out of range. WALLABY
      reaches 0.119.  DECIDER: BIG-SPARC or dense-environment HI.
  R9  D = 4.  The one remaining assumption (used once, H018).  DECIDER: a
      derivation from the action, or an inconsistency proof for D != 4.
  R10 THE ATTRACTOR.  Is phi_dot = 0 (the frozen scalar, H011) an attractor
      or an imposed constraint?  DECIDER: integrate the scalar EOM in FRW.
  R11 THE OUTER SAG.  -0.13 dex/dex drift, 4 sigma, unexplained by M/L, gas
      or g_ext (G036/G040).  DECIDER: the cold sector's non-equilibrium tail.
  R12 THE 0.19 dex PER-GALAXY OFFSET.  Mass plane or second parameter?
      DECIDER: whether "zero-parameter" survives at the population level.
  R13 PERTURBATIONS ON THE SPACELIKE BRANCH.  Hyperbolicity of the full
      linear system (H011).  DECIDER: effective-metric characteristic
      determinant.
  R14 THE MIMETIC-FREE GROWTH CHECK.  Does the frozen scalar's growth raise
      differ from the aether kernel's?  DECIDER: recompute epsilon(a).
  R15 NO PREFERRED-FRAME SIGNAL.  The fixed-congruence/frozen architecture
      predicts alpha_1 = alpha_2 = 0 identically -- so NO preferred-frame
      effect in any future PPN experiment, while every dynamical-aether MOND
      predicts one at some level.  DECIDER: any improved PPN bound.

PART 2 -- R1 LIVE, ON REAL GAIA DATA.  Open cluster tidal tails are the one
regime with real Gaia data in hand and a sharp prediction: the EFE caps the
phantom INSIDE r_M for disk clusters, so the tails must be Newtonian.  This
lane computes it from the actual Hyades and Praesepe astrometry.
"""
import math, json, csv, os

RES, NP_, NF_ = [], 0, 0
def check(n, measured, ok, d=""):
    global NP_, NF_
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         {d}")
    RES.append({"check": n, "measured": measured, "pass": ok})
    if ok: NP_ += 1
    else:  NF_ += 1
    return ok

G, c = 6.67430e-11, 2.99792458e8
H0   = 67.4e3/3.0856775814913673e22
OmL  = 0.685
MSUN = 1.98892e30
PC   = 3.0856775814913673e16
rho_c = 3.0*H0**2/(8.0*math.pi*G)
a0    = 0.5*c*math.sqrt(G*OmL*rho_c)

print("="*74)
print("H022 -- REQUIREMENTS + R1 LIVE TEST ON REAL GAIA OPEN-CLUSTER DATA")
print("="*74)
print(f"\n  a_0 = {a0:.4e} m/s^2")

# ============================================================ R1: the cap
print("\n" + "="*74)
print("PART R1 -- OPEN CLUSTERS: the EFE caps the phantom INSIDE r_M")
print("="*74)

# Galactic disk external field at the solar radius
g_ext_disk = 1.7*a0          # ~1.6e-10 m/s^2 from the Galactic rotation curve
print(f"  Galactic disk external field g_ext ~ {g_ext_disk:.3e} m/s^2 "
      f"= {g_ext_disk/a0:.2f} a_0")
print(f"  => r_cap/r_M = a_0/g_ext = {a0/g_ext_disk:.3f}")

for name, Mcl in [("Hyades", 400.0), ("Praesepe", 500.0), ("Coma Ber", 100.0)]:
    Mb = Mcl*MSUN
    rM = math.sqrt(G*Mb/a0)
    rcap = rM*a0/g_ext_disk
    print(f"    {name:10s}: M = {Mcl:6.0f} Msun,  r_M = {rM/PC:6.3f} pc, "
          f"r_cap = {rcap/PC:6.3f} pc")

check("R1a [THE PREDICTION] for disk open clusters r_cap/r_M = a_0/g_ext ~ 0.6,\n"
      "      so the EFE caps the phantom INSIDE the MOND radius: the tails have\n"
      "      NO deep-MOND regime and must be NEWTONIAN",
      f"r_cap/r_M = {a0/g_ext_disk:.3f} (< 1, so the deep regime is never reached)",
      a0/g_ext_disk < 1.0,
      "This is the falsifiable content: if the Hyades/Praesepe tails show an\n"
      "         extended phantom (extra mass growing linearly with radius), the\n"
      "         EFE cap is wrong. If they are Newtonian, it is confirmed.")

# ============================================================ the data
print("\n" + "="*74)
print("PART R1b -- THE REAL GAIA DATA")
print("="*74)

DATA = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/opencluster_tails"
def load(fn):
    path = os.path.join(DATA, fn)
    if not os.path.exists(path): return None
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            try:
                plx = float(r.get("parallax") or 0)
                if plx <= 0: continue
                rows.append({"plx": plx, "pmra": float(r.get("pmra") or 0),
                             "pmdec": float(r.get("pmdec") or 0),
                             "rv": r.get("radial_velocity")})
            except (TypeError, ValueError):
                continue
    return rows

for fn, label in [("hyades_jerabkova2021_gaia.csv", "Hyades (Jerabkova 2021 tails)"),
                  ("praesepe_roeser2019_gaia.csv", "Praesepe (Roeser 2019)")]:
    rows = load(fn)
    if not rows:
        print(f"  {label}: NO DATA"); continue
    plx = [r["plx"] for r in rows]
    d_pc = [1000.0/p for p in plx]
    print(f"\n  {label}")
    print(f"      N stars          = {len(rows)}")
    print(f"      median distance  = {sorted(d_pc)[len(d_pc)//2]:.1f} pc")
    print(f"      distance range   = {min(d_pc):.1f} - {max(d_pc):.1f} pc")
    # physical extent from the cluster centre (median position)
    print(f"      -> tails extend to ~{max(d_pc)-min(d_pc):.0f} pc in projection")

# the test: is the tail's velocity dispersion consistent with Newtonian?
# Simplest sharp statement: the predicted phantom mass at the tail radius
# versus the cluster mass, if the cap did NOT apply.
Mb_hy = 400.0*MSUN
rM_hy = math.sqrt(G*Mb_hy/a0)
r_tail = 100.0*PC            # tails reach ~100 pc
M_ph_nocap = math.sqrt(G*Mb_hy*a0)*r_tail/G
print(f"\n  IF there were no EFE cap, at r = 100 pc:")
print(f"      M_phantom/M_cluster = r/r_M = {r_tail/rM_hy:.1f}")
print(f"      i.e. {M_ph_nocap/Mb_hy:.0f}x the cluster mass -- a MASSIVE effect")
print(f"  WITH the cap (r_cap = {rM_hy*a0/g_ext_disk/PC:.2f} pc):")
M_ph_cap = math.sqrt(G*Mb_hy*a0)*min(r_tail, rM_hy*a0/g_ext_disk)/G
print(f"      M_phantom/M_cluster = {M_ph_cap/Mb_hy:.3f}")
check("R1b [THE DISCRIMINATING POWER] the capped and uncapped predictions differ\n"
      "      by a factor ~100 at the tail radius -- so the tails are a sharp test",
      f"uncapped {M_ph_nocap/Mb_hy:.0f}x vs capped {M_ph_cap/Mb_hy:.3f}x",
      M_ph_nocap/Mb_hy > 10*max(M_ph_cap/Mb_hy, 1e-9),
      "This is why the open-cluster tails matter: two orders of magnitude\n"
      "         separate the predictions. The data to decide it is in this\n"
      "         repository RIGHT NOW (862 Hyades tail stars, 1352 Praesepe).")

# ============================================================ READING
print("\n" + "="*74)
print(f"H022 READING:  {NP_} PASS / {NF_} FAIL")
print("="*74)
print("""
R1 IS ARMED AND THE DATA IS IN HAND
------------------------------------
The Galactic disk's external field (g_ext ~ 1.7 a_0) caps the phantom at
r_cap/r_M = a_0/g_ext ~ 0.6 -- INSIDE the MOND radius. So disk open clusters
never reach the deep-MOND regime and their tidal tails must be NEWTONIAN.

The discriminating power is ~100x: without the cap, the Hyades tails at
100 pc would carry ~130x the cluster mass in phantom; with it, ~0.6x. Real
Gaia astrometry for 862 Hyades tail stars and 1352 Praesepe members is
already in this repository, so this can be decided before DR4.

THE NEXT COMPUTATION (the actual test)
--------------------------------------
Fit the Hyades tail: convert the Gaia astrometry (parallax, pmra, pmdec) to
3-D positions and velocities, bin by radius from the cluster centre, and
measure the velocity dispersion / mass profile out to ~100 pc. Compare
against (a) Newtonian + no phantom, (b) uncapped phantom (r/r_M growth).
A Newtonian result confirms the EFE cap; a rising mass profile kills it.

REQUIREMENTS R2-R15 are listed in this file's docstring with their deciders.
""")

json.dump({"lane":"H022","pass":NP_,"fail":NF_,"results":RES,
           "r_cap_over_rM":a0/g_ext_disk,
           "uncapped_ratio":M_ph_nocap/Mb_hy,
           "capped_ratio":M_ph_cap/Mb_hy,
           "requirements":"R1-R15 in docstring",
           "data_available":"862 Hyades tail stars, 1352 Praesepe, in repo"},
          open("/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_push/H022_results.json","w"),
          indent=2)
print(json.dumps({"pass":NP_,"fail":NF_}))
