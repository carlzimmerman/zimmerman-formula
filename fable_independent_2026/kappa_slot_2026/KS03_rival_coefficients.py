#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
KS03_rival_coefficients.py -- every published a_0-Lambda coefficient as (kappa, eps_tot), on both
footings, and what measurement separates them.

kappa == a_0/(c sqrt(G rho_Lambda)), eps_tot == kappa^2/(8 pi).  Rate-form proposals a_0 = X * cH are
converted with cH_Lambda = sqrt(8 pi/3) c sqrt(G rho_Lambda) (canonical footing) and
cH0 = sqrt(8 pi/3) c sqrt(G rho_Lambda)/sqrt(Om_Lambda) (alt footing).

  C1  which candidates are inside 2 sigma of each measurement (BTFR, distance-free, MLS16 g-dagger)
  C2  the minimum precision on kappa to separate 1/2 from its nearest DISTINCT surviving rival at 3 sigma
  C3  the H0-tension degeneracy: kappa = 1/2 on Planck H0 and kappa = 0.461 on SH0ES H0 predict the same a_0

Run:  python3 fable_independent_2026/kappa_slot_2026/KS03_rival_coefficients.py
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "KS03_rival_coefficients"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "KS03", "checks": {}, "numbers": {}, "table": []}


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


# constants / footings
c = 2.99792458e8; G = 6.674e-11; MPC = 3.0857e22
H0 = 67.4e3 / MPC; OmL = 0.685
rho_c = 3 * H0**2 / (8 * math.pi * G); rho_L = OmL * rho_c
sq = math.sqrt(G * rho_L)                     # sqrt(G rho_Lambda)
kUNIT = c * sq                                # a_0 = kappa * kUNIT
S83 = math.sqrt(8 * math.pi / 3)              # cH_Lambda / (c sqrt(G rho_L))
S83_H0 = S83 / math.sqrt(OmL)                 # cH0     / (c sqrt(G rho_L))
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

KAPPA_MEAS = [("BTFR", 0.465, 0.076), ("distance-free", 0.551, 0.043)]
# MLS16 g-dagger = 1.20 +- 0.02(rand) +- 0.24(syst) x 1e-10 m/s^2, converted to kappa:
gdag = 1.20e-10; gdag_r, gdag_s = 0.02e-10, 0.24e-10
kap_MLS = gdag / kUNIT; kap_MLS_r = gdag_r / kUNIT; kap_MLS_s = gdag_s / kUNIT
MEAS = KAPPA_MEAS + [("MLS16 g-dagger (syst-dom)", kap_MLS, math.hypot(kap_MLS_r, kap_MLS_s))]

P(__doc__)
P(f"  kUNIT = c sqrt(G rho_L) = {kUNIT:.4e} m/s^2;  sqrt(8pi/3) = {S83:.4f};  /sqrt(Om) = {S83_H0:.4f}")
P(f"  MLS16 g-dagger -> kappa = {kap_MLS:.4f} +- {kap_MLS_r:.4f}(rand) +- {kap_MLS_s:.4f}(syst)")

banner("THE TABLE -- every proposal as kappa (both footings) and eps_tot")
# proposal: (name, kind, X)   kind in {'cHL' (rate on H_Lambda), 'cH0' (rate on H0), 'density' (kappa given)}
PROP = [
    ("Framework, kappa = 1/2",                 "density", 0.5),
    ("Milgrom 1983, a0 ~ cH0/2pi",             "cH0",     1 / (2 * math.pi)),
    ("Milgrom 2020, a0 = c^2/(2pi L_dS)=cHL/2pi","cHL",   1 / (2 * math.pi)),
    ("Deser-Levin/Unruh, a0 = 2 cH_Lambda",    "cHL",     2.0),
    ("Verlinde 2016, a0 = cH0/6",              "cH0",     1 / 6),
    ("graviton norm B (eps=1/12)",             "density", 1.4472),
    ("graviton norm B x 2 pol (eps=1/6)",      "density", 2.0467),
    ("CKN/seesaw a0 = Lambda_DE^2/(2 M_Pl)",   "seesaw",  None),
]


def kappa_both(kind, X):
    if kind == "density":
        return X, X
    if kind == "cHL":
        return X * S83, X * S83                    # H_Lambda footing (same both, it IS the Lambda rate)
    if kind == "cH0":
        return X * S83, X * S83_H0                 # canonical uses H_Lambda-equiv; alt uses cH0
    return None, None


# CKN/seesaw: a0 = Lambda_DE^2/(2 M_Pl), Lambda_DE = (rho_L c^2 (hbar c)^3)^{1/4} (energy, J),
# M_Pl = sqrt(hbar c^5/G) (NON-reduced Planck energy, J).  A natural-units acceleration = energy;
# restore SI with a_SI = (c/hbar) * a_nat.  This reproduces kappa=1/2 EXACTLY only with the non-reduced
# M_Pl (the reduced one, /sqrt(8pi), gives kappa = sqrt(8pi)/2 = 2.507): itself a convention subtlety.
hbar = 1.054571817e-34
Lam_DE_J = (rho_L * c**2 * (hbar * c)**3) ** 0.25             # dark-energy scale, J (~2.3 meV)
M_Pl_J = math.sqrt(hbar * c**5 / G)                          # non-reduced Planck energy, J
a0_seesaw = (c / hbar) * (Lam_DE_J**2 / (2 * M_Pl_J))        # SI m/s^2
kap_seesaw = a0_seesaw / kUNIT
OUT["numbers"]["a0_seesaw"] = a0_seesaw
OUT["numbers"]["kappa_seesaw"] = kap_seesaw
P(f"  CKN/seesaw a0 = Lambda_DE^2/(2 M_Pl) = {a0_seesaw:.4e} m/s^2  ->  kappa = {kap_seesaw:.4f} "
  f"(non-reduced M_Pl; reduced gives sqrt(8pi)/2 = {math.sqrt(8*math.pi)/2:.3f})")

rows = []
for name, kind, X in PROP:
    if kind == "seesaw":
        kc, ka = kap_seesaw, kap_seesaw
    else:
        kc, ka = kappa_both(kind, X)
    ec = kc**2 / (8 * math.pi)
    rows.append(dict(name=name, kind=kind, kc=kc, ka=ka, eps=ec))
    OUT["table"].append(dict(name=name, kappa_canon=kc, kappa_alt=ka, eps_tot=ec))

P(f"  {'proposal':<44}{'kappa(HL)':>10}{'kappa(H0/alt)':>14}{'eps_tot':>11}")
P("  " + "-" * 80)
for r in rows:
    P(f"  {r['name']:<44}{r['kc']:>10.4f}{r['ka']:>14.4f}{r['eps']:>11.5f}")

# --- C1: in-band membership ---------------------------------------------------------------------
banner("C1 -- which candidates are inside 2 sigma of each measurement")
inband = {}
for mname, mval, msig in MEAS:
    hits = [r["name"] for r in rows if abs(r["kc"] - mval) <= 2 * msig or abs(r["ka"] - mval) <= 2 * msig]
    inband[mname] = hits
    P(f"  {mname} ({mval:.3f} +- {msig:.3f}), 2sigma [{mval-2*msig:.3f},{mval+2*msig:.3f}]:")
    for h in hits:
        P(f"       - {h}")
n_btfr = len(inband["BTFR"])
check("C1 multiple distinct candidates sit inside 2 sigma of the BTFR band (the coefficient is NOT "
      "isolated by the data): count them",
      f"{n_btfr} candidates in the BTFR 2sigma band (of {len(rows)} listed)", n_btfr >= 4,
      "1/2, Milgrom 2020 (0.461), Milgrom 1983 (0.557), Verlinde (0.583/0.482), CKN (0.500) all fit; "
      "Deser-Levin (5.79) and the graviton norms (1.45/2.05) do not")
OUT["numbers"]["n_in_BTFR_2sig"] = n_btfr

# --- C2: separation power ------------------------------------------------------------------------
banner("C2 -- precision on kappa to separate 1/2 from its nearest DISTINCT surviving rival at 3 sigma")
half = 0.5
rivals = [(r["name"], r["kc"]) for r in rows if abs(r["kc"] - half) > 1e-6]  # distinct from 1/2
rivals_sorted = sorted(rivals, key=lambda t: abs(t[1] - half))
nearest_name, nearest_k = rivals_sorted[0]
dkap = abs(nearest_k - half)
sig_needed = dkap / 3.0                       # 3 sigma separation: Delta/sigma = 3
pct_needed = 100 * sig_needed / half
P(f"  nearest distinct rival to 1/2: {nearest_name} at kappa = {nearest_k:.4f}, Delta = {dkap:.4f}")
P(f"  3-sigma separation needs sigma(kappa) <= {sig_needed:.4f} = {pct_needed:.2f}% of kappa")
# today's precision from the distance-free band applied at kappa~1/2:
sig_today = 0.043
sep_today = dkap / sig_today
check("C2 the nearest DISTINCT rival to 1/2 is closer than today's kappa error, so the data do not "
      "separate them at 3 sigma",
      f"Delta = {dkap:.4f}, needs {pct_needed:.2f}% (sigma<= {sig_needed:.4f}); best band sigma ~ {sig_today} "
      f"gives {sep_today:.2f} sigma", sep_today < 3.0,
      f"reproduces k03: ~2.8% on a_0 needed for 3 sigma vs a 9.47% mass-budget floor; here {pct_needed:.1f}% needed")
OUT["numbers"].update(nearest_rival=nearest_name, nearest_kappa=nearest_k, delta_kappa=dkap,
                      pct_needed_3sig=pct_needed, sep_today_sigma=sep_today)

# note the CKN/seesaw exact degeneracy
seesaw_row = next(r for r in rows if "CKN" in r["name"])
check("C2b the CKN/seesaw a0 = Lambda_DE^2/(2 M_Pl) is EXACTLY kappa = 1/2 (a restatement of the density "
      "identity), so it can never be separated from the framework -- it carries no independent content",
      f"kappa_seesaw = {seesaw_row['kc']:.4f} (= 1/2 by construction)", abs(seesaw_row["kc"] - 0.5) < 1e-9,
      "consistent with L260: a0 = Lambda_DE^2/(2 M_Pl) is the density identity in seesaw notation")

# --- C3: H0-tension degeneracy -------------------------------------------------------------------
banner("C3 -- the H0-tension degeneracy (kappa = 1/2 on Planck vs 0.461 on SH0ES predict one a_0)")
H0_planck = 67.4; H0_shoes = 73.0
# a_0 = kappa * c * sqrt(G rho_L), rho_L = Om * 3 H0^2/(8 pi G) => sqrt(G rho_L) ∝ H0 (Om fixed)
a0_half_planck = 0.5 * H0_planck
a0_461_shoes = 0.4607 * H0_shoes
ratio = a0_half_planck / a0_461_shoes
check("C3 kappa = 1/2 with Planck H0 and kappa = 0.461 with SH0ES H0 predict the SAME a_0: the "
      "coefficient is degenerate with the H0 tension at fixed Om_Lambda",
      f"(1/2 * 67.4)/(0.461 * 73.0) = {ratio:.4f} (agree to {abs(1-ratio)*100:.2f}%)",
      abs(ratio - 1.0) < 0.01,
      "so 'deriving kappa = 0.461 vs 1/2' trades against a 8% cosmological systematic, not against data")
OUT["numbers"]["H0_degeneracy_ratio"] = ratio

# --- the decisive observation --------------------------------------------------------------------
banner("THE DECIDING MEASUREMENT")
P(f"""  Two observations bear on the coefficient:
   (a) a homogeneous kappa measurement to +-{pct_needed:.1f}% (sigma(kappa) <= {sig_needed:.4f}) separates 1/2 from
       its nearest DISTINCT rival ({nearest_name}, {nearest_k:.3f}) at 3 sigma.  +-5% is NOT enough
       ({dkap/(0.05*half):.1f} sigma).  This KILLS the graviton norms (1.45, 2.05) and Deser-Levin (5.79)
       already; it would decide 1/2 vs 0.461 only at the ~1% level.
   (b) the deep-MOND Tully-Fisher zero point at z ~ 2.5 to +-0.13 dex (already registered) tests the a_0(z)
       LAW (flat vs rising), FLAT 0.00 vs LCDM +0.33 dex -- it separates the framework from LCDM but NOT
       1/2 from 0.461 (both are flat-law, same z-dependence).  So (b) does not decide the coefficient.
  => the coefficient question is a precision problem, gated by the stellar M/L zero point, the absolute
     gas scale and H0; no registered measurement decides 1/2 vs 0.461, and CKN/seesaw is degenerate with
     1/2 by construction.""")

banner("VERDICT")
P(f"""  (1) COMPUTED: 8 published a_0-Lambda coefficients as (kappa, eps_tot) on both footings.
  (2) NUMBERS: {n_btfr} candidates inside the BTFR 2 sigma band; nearest distinct rival to 1/2 is
      {nearest_name} at {nearest_k:.3f} (Delta = {dkap:.3f}); 3 sigma separation needs {pct_needed:.1f}% on kappa;
      today ~{sep_today:.1f} sigma; kappa=1/2 (Planck) and 0.461 (SH0ES) agree on a_0 to {abs(1-ratio)*100:.1f}%.
  (3) HONEST SENTENCE: {n_btfr} candidates inside 2 sigma; 1/2 separated from its nearest distinct rival at
      {sep_today:.1f} sigma today; needs +-{pct_needed:.1f}% on kappa; degenerate with the H0 tension: YES.  CANDIDATE,
      not selected.""")
OUT["verdict"] = {"word": "CANDIDATE-NOT-SELECTED", "n_in_band": n_btfr,
                  "nearest_rival": nearest_name, "sep_today_sigma": sep_today,
                  "pct_needed_3sig": pct_needed, "H0_degenerate": True}

banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok); n = len(CH)
lb_fail = [nm for nm, ok, lb in CH if lb and not ok]
P(f"KS03 COMPLETE: {npass}/{n} checks PASS")
for nm in lb_fail:
    P(f"    load-bearing FAIL: {nm}")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb_fail}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(1 if lb_fail else 0)
