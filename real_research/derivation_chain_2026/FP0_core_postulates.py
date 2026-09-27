#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FP0 -- THE TOP OF THE DERIVATION CHAIN: the framework's postulates and what follows from them by algebra alone.

WHY.  The derivation chain is built from the framework's own first principles: one action at the root, every observable
varied out of it, nothing posited by hand below the postulates.  Before the action, the chain has a top that needs no
action at all: the acceleration postulate, the galaxy law, and the a0(z) reading.  This lane fixes that top, machine-checks
every consequence that is pure algebra, and labels each link DERIVED / POSTULATED / FITTED / CONSTRAINT, so the first link
that needs the action is explicit.

THE POSTULATES (the inputs; nothing below them is added by hand):
  P1  the acceleration scale is set by the vacuum:  a0 = kappa c sqrt(G rho_Lambda)  (kappa = 1/2; rho_Lambda = Omega_L rho_c).
  P2  the galaxy law:  g_obs = sqrt(g_bar^2 + g_bar a0)  (the framework's interpolation; its form is Milgrom 1999, Eq. 9).
  P3  the canonical reading of P1 in time: a0 tracks sqrt(rho_DE(z)), never H(z); with w = -1 (a true constant) a0 is flat.
CHECKS
  C1 CONTROL (uniqueness): the only acceleration built from (G, c, rho) is G^(1/2) c rho^(1/2) -- the exponent matrix is
     nonsingular with |det| = 2 -- so P1's FORM is forced; kappa and the choice of rho are not.
  C2 the numbers of P1 on both footings (H0 = 67.4, Omega_L = 0.6847): a0 = 9.36e-11 (rho_Lambda) and 1.13e-10 (rho_total);
     Z = c H_Lambda / a0 = sqrt(32 pi / 3) and kappa Z = sqrt(8 pi / 3) are identities, not data.
  R1 P2's consequences (DERIVED from P2): the deep limit g -> sqrt(a0 g_bar); the baryonic Tully-Fisher law v^4 = G M a0
     exactly in that limit; the landmark slope s(y) = (2y+1)/(2(y+1)), y = g_bar/a0, with the sum rule s(y) + s(1/y) = 3/2.
  R2 P2's high-acceleration tail (a DERIVED CONSTRAINT on the root action): g_obs - g_bar -> a0/2 as g_bar -> infinity, a
     constant sunward anomaly of 4.68e-11 m/s^2 at the Sun, far above the Earth ephemeris bound read from the committed
     real_research/reviews/mi_alpha1_solar_system_2026.out (Sereno & Jetzer 2006 / EPM2004, 2 sigma).  So P2 is an
     infrared law: the action's kernel must reach Newton faster than 1/(2y) (alpha >~ 1.5), invisible in galaxies.
  R3 P3's a0(z) (DERIVED from P1 + P3): a0(z)/a0(0) = 1 exactly at every z on the canonical reading; the rival rho_total
     reading gives a0 proportional to H(z) (a factor E(z) = 3.77 at z = 2.5), so the flat law is a distinguishing prediction.
  R3b P1 with EVOLVING dark energy (DERIVED from P1 + the measured w(z)): a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)); for DESI's
     CPL fits a ~0.1 dex decline at z = 2.5 (reproducing the committed fable_independent_2026/L273_desi_a0z_band.out).
  W  the ledger of this lane's links and their status.
MUTATE=1 replaces P2 by the exponential RAR kernel g = g_bar / (1 - exp(-sqrt(g_bar/a0))): the sum rule and the a0/2 tail are
properties of the framework's own law, so R1 and R2 must FAIL (rc = 1).

Run from the repository root:  python3 real_research/derivation_chain_2026/FP0_core_postulates.py
"""
import os, re, sys, json, math
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "FP0_core_postulates" + ("_MUTATE" if MUTATE else "")
OUT = {"lane": "FP0", "mutate": MUTATE, "checks": {}, "numbers": {}, "ledger": []}
CH = []

# inputs (the corpus's canonical pair; a0 = 9.36e-11 uses exactly these)
c, G = 299792458.0, 6.67430e-11
MPC = 3.0856775814913673e22
H0_KMS, OM_L, OM_M = 67.4, 0.6847, 0.3153
KAPPA = sp.Rational(1, 2)


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)


def check(name, measured, ok, load_bearing=True):
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": bool(ok), "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: P2 replaced by the exponential RAR kernel -- R1 (sum rule) and R2 (a0/2 tail) must FAIL ***")

# ---------------------------------------------------------------------------------------------- C1 uniqueness
banner("C1  CONTROL: the form of P1 is forced by (G, c, rho)")
a_, b_, d_ = sp.symbols("a b d")
# dimensions [m, kg, s]: G = m^3 kg^-1 s^-2, c = m s^-1, rho = kg m^-3; target a0 = m s^-2
M = sp.Matrix([[3, 1, -3], [-1, 0, 1], [-2, -1, 0]])
sol = sp.solve(list(M * sp.Matrix([a_, b_, d_]) - sp.Matrix([1, 0, -2])), [a_, b_, d_], dict=True)
det = M.det()
uniq = len(sol) == 1 and sol[0] == {a_: sp.Rational(1, 2), b_: 1, d_: sp.Rational(1, 2)} and abs(det) == 2
check("C1 CONTROL: G^a c^b rho^d = acceleration has the single solution (1/2, 1, 1/2); the exponent matrix has |det| = 2",
      f"solution {sol}; det {det}", uniq)
OUT["numbers"]["exponents"] = {str(k): str(v) for k, v in sol[0].items()} if sol else None

# ---------------------------------------------------------------------------------------------- C2 numbers
banner("C2  P1 in numbers, both footings; Z is kappa")
H0 = H0_KMS * 1e3 / MPC
rho_c = 3 * H0 ** 2 / (8 * math.pi * G)
rho_L = OM_L * rho_c
a0_can = float(KAPPA) * c * math.sqrt(G * rho_L)
a0_tot = float(KAPPA) * c * math.sqrt(G * rho_c)
H_L = H0 * math.sqrt(OM_L)
Z_num = c * H_L / a0_can
Zs = sp.sqrt(sp.Rational(32, 3) * sp.pi)
ident = sp.simplify(KAPPA * Zs - sp.sqrt(sp.Rational(8, 3) * sp.pi)) == 0
ok2 = abs(a0_can / 9.36e-11 - 1) < 1e-3 and abs(a0_tot / 1.131e-10 - 1) < 2e-3 and abs(Z_num / float(Zs) - 1) < 1e-12 and ident
check("C2 a0 = 9.36e-11 (rho_Lambda) / 1.13e-10 (rho_total); Z = c H_Lambda / a0 = sqrt(32 pi/3) and kappa Z = sqrt(8 pi/3) exactly",
      f"a0 {a0_can:.4e} / {a0_tot:.4e} m/s^2; Z {Z_num:.10f} vs sqrt(32pi/3) {float(Zs):.10f}; kappa Z identity {ident}", ok2)
OUT["numbers"].update(a0_canonical=a0_can, a0_rho_total=a0_tot, Z=Z_num, rho_Lambda=rho_L, H_Lambda=H_L)

# ---------------------------------------------------------------------------------------------- R1 galaxy law
banner("R1  P2's consequences: deep limit, BTFR, the landmark slope and its sum rule")
y = sp.symbols("y", positive=True)
g_hat = (y / (1 - sp.exp(-sp.sqrt(y)))) if MUTATE else sp.sqrt(y ** 2 + y)          # g_obs / a0 as a function of y = g_bar/a0
deep = sp.limit(g_hat / sp.sqrt(y), y, 0)
Mb, r, v, a0s, Gs = sp.symbols("M r v a_0 G", positive=True)
btfr = sp.solve(sp.Eq(v ** 2 / r, sp.sqrt(a0s * Gs * Mb / r ** 2)), v)
v4 = sp.simplify(btfr[0] ** 4) if btfr else None
s = sp.simplify(y * sp.diff(sp.log(g_hat), y))
sum_dev = max(abs(float((s + s.subs(y, 1 / y)).subs(y, yy)) - 1.5) for yy in (0.03, 0.2, 1.0, 3.7, 40.0))
s_closed = sp.simplify(s - (2 * y + 1) / (2 * (y + 1))) == 0
ok_r1 = deep == 1 and v4 == Gs * Mb * a0s and sum_dev < 1e-12 and s_closed
check("R1 DERIVED from P2: g -> sqrt(a0 g_bar) deep; v^4 = G M a0 exactly there; s(y) = (2y+1)/(2(y+1)); s(y) + s(1/y) = 3/2",
      f"deep-limit ratio {deep}; v^4 = {v4}; slope closed form {s_closed}; max |sum rule - 3/2| over 5 y = {sum_dev:.1e}", ok_r1)
OUT["numbers"]["sum_rule_max_dev"] = sum_dev

# ---------------------------------------------------------------------------------------------- R2 high-acceleration tail
banner("R2  P2's high-acceleration tail: a derived constraint on the root action")
tail = sp.limit(g_hat - y, y, sp.oo)
anom = float(tail) * a0_can
src = os.path.join(REPO, "real_research", "reviews", "mi_alpha1_solar_system_2026.out")
m = re.search(r"^\s*Earth\s+\S+\s+([0-9.]+e-\d+)", open(src).read(), re.M) if os.path.exists(src) else None
bound = float(m.group(1)) if m else float("nan")
ratio = anom / bound if m else float("nan")
ok_r2 = tail == sp.Rational(1, 2) and m is not None and ratio > 100
check("R2 CONSTRAINT: g_obs - g_bar -> a0/2 as g_bar -> infinity; at the Sun that is far above the Earth ephemeris bound, so "
      "the root action's kernel must reach Newton faster than 1/(2y) (P2 is an infrared law)",
      f"tail {tail} a0 = {anom:.3e} m/s^2; Earth bound {bound:.2e} m/s^2 (from {os.path.relpath(src, REPO)}); ratio {ratio:.0f}x", ok_r2)
OUT["numbers"].update(tail_over_a0=str(tail), sunward_anomaly=anom, earth_bound=bound, over_bound=ratio)

# ---------------------------------------------------------------------------------------------- R3 a0(z)
banner("R3  P1 + P3: a0(z) is flat on the canonical reading; the rival follows H(z)")
zs = [0.5, 1.0, 2.5, 5.0, 1100.0]
E = lambda z: math.sqrt(OM_M * (1 + z) ** 3 + OM_L)
flat = {z: 1.0 for z in zs}                                             # rho_Lambda with w = -1 is the same at every z
rival = {z: E(z) for z in zs}                                           # rho_total(z) = rho_c E(z)^2  =>  a0 proportional to H(z)
ok_r3 = all(v_ == 1.0 for v_ in flat.values()) and abs(rival[2.5] - 3.769) < 5e-3
check("R3 DERIVED from P1 + P3: a0(z)/a0(0) = 1 at every z (canonical); the rho_total rival gives E(z) -- the flat law is a "
      "distinguishing prediction, decided at z >~ 2 (the pre-registered test)",
      "canonical 1.000 at z = " + ", ".join(f"{z:g}" for z in zs) + "; rival " + ", ".join(f"{rival[z]:.3f}" for z in zs[:4])
      + f" (+{math.log10(rival[2.5]):.3f} dex at z = 2.5)", ok_r3)
OUT["numbers"]["a0z_rival_E"] = rival

# ---------------------------------------------------------------------------------------------- R3b a0(z) under evolving dark energy
banner("R3b P1 with EVOLVING dark energy: a0(z) tracks sqrt(rho_DE(z)); w = -1 is the flat special case")
# P1 says a0 ~ sqrt(rho_DE). For CPL w(z) = w0 + wa z/(1+z): rho_DE(z)/rho_DE(0) = (1+z)^(3(1+w0+wa)) exp(-3 wa z/(1+z)).
a0z_cpl = lambda z, w0, wa: (1 + z) ** (1.5 * (1 + w0 + wa)) * math.exp(-1.5 * wa * z / (1 + z))
src73 = os.path.join(REPO, "fable_independent_2026", "L273_desi_a0z_band.out")
m73 = re.search(r"banked \((-?[0-9.]+), (-?[0-9.]+)\); a0\(2\.5\)/a0\(0\) = ([0-9.]+)", open(src73).read()) \
    if os.path.exists(src73) else None
if m73:
    w0_, wa_, ref_ = float(m73.group(1)), float(m73.group(2)), float(m73.group(3))
    r25 = a0z_cpl(2.5, w0_, wa_)
    lam = a0z_cpl(2.5, -1.0, 0.0)
    ok_r3b = abs(r25 - ref_) < 1e-3 and abs(lam - 1.0) < 1e-12 and r25 < 1.0 < rival[2.5]
    meas = (f"DESY5 CPL (w0, wa) = ({w0_}, {wa_}) from {os.path.relpath(src73, REPO)}: a0(2.5)/a0(0) = {r25:.4f} "
            f"({math.log10(r25):+.3f} dex) vs the committed {ref_}; w = -1 gives {lam:.4f} (flat); the rho_total rival "
            f"+{math.log10(rival[2.5]):.3f} dex -- the scaling predicts a small DECLINE under DESI, the rival a large rise")
    OUT["numbers"].update(a0z_desy5_z25=r25, a0z_desy5_pair=[w0_, wa_])
else:
    ok_r3b, meas = False, f"could not read the DESY5 pair from {src73}"
check("R3b DERIVED from P1 (a0 ~ sqrt rho_DE) + measured w(z): a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)); flat for w = -1, a "
      "~0.1 dex decline at z = 2.5 under DESI's evolving dark energy (reproduces L273)", meas, ok_r3b)

# ---------------------------------------------------------------------------------------------- W ledger
banner("W  THE LEDGER: what this top of the chain derives, and where the action has to take over")
LEDGER = [
    ("L0a", "the FORM a0 ~ c sqrt(G rho)", "DERIVED", "C1: unique from (G, c, rho), |det| = 2"),
    ("L0b", "which density: rho_Lambda", "POSTULATED", "physics input; the same form on rho_m or rho_local spans 609x"),
    ("L0c", "kappa = 1/2 (equivalently Z = 5.7888)", "FITTED", "not derived by any route tried; the data prefer kappa ~ 0.56-0.64"),
    ("L1a", "the galaxy law g_obs = sqrt(g_bar^2 + g_bar a0)", "POSTULATED", "form = Milgrom 1999 Eq. 9; the coefficient is the framework's"),
    ("L1b", "deep limit, BTFR v^4 = G M a0, slope s(y), sum rule 3/2", "DERIVED", "R1, from L1a"),
    ("L1c", "the a0/2 tail vs the planets", "CONSTRAINT", "R2: the action's kernel must reach Newton faster (alpha >~ 1.5)"),
    ("L2a", "a0(z) flat (rho_Lambda, w = -1)", "DERIVED", "R3, from L0 + P3"),
    ("L2a'", "a0(z) ~ sqrt(rho_DE(z)) for evolving dark energy: -0.10 dex at z = 2.5 under DESI (vs the rival +0.58)",
     "DERIVED", "R3b, from P1 + the measured w(z); reproduces L273"),
    ("L2b", "a0 as a field (a0^2 = kappa^2 G (-p_Q))", "POSTULATED", "a chosen promotion; the action has to produce it"),
    ("L3", "the covariant action (root)", "OPEN", "next lane: chosen after the candidate map; everything below is varied out of it"),
    ("L4-L10", "static limit/kernel, lensing, PPN, c_T = 1, stability, cosmology, clusters", "OPEN", "each derived from L3 or it fails"),
]
for k, what, status, why in LEDGER:
    P(f"    {k:7s} {status:11s} {what}  --  {why}")
OUT["ledger"] = [dict(link=k, what=w, status=s_, basis=b) for k, w, s_, b in LEDGER]
check("W (reported) the ledger of the chain's top", f"{len(LEDGER)} links", True, load_bearing=False)

# ---------------------------------------------------------------------------------------------- verdict
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
banner("VERDICT")
P(f"  The top of the chain is fixed: P1's form is forced, its density and coefficient are inputs; P2's deep-regime laws follow"
  f"\n  exactly; P2 must be an infrared law (its a0/2 tail is {ratio:.0f}x the Earth bound); a0(z) is flat on the canonical"
  f"\n  reading.  Everything from the static limit down is owed by the root action (L3).")
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results.json".replace("_MUTATE_results", "_results_MUTATE")), "w"), indent=1)
P(f"\n  {len(CH) - n_fail}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote "
  f"{SLUG.replace('_MUTATE', '')}_results{'_MUTATE' if MUTATE else ''}.json")
sys.exit(0 if n_fail == 0 else 1)
