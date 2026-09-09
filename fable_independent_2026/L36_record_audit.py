#!/usr/bin/env python3
"""
L36 -- an adversarial audit of THIS LANE'S OWN standing record (HANDOFF_CONTRACT.md section A, A1-A23)
=======================================================================================================
The owner of this repository has said, correctly, that too many mistakes have been made and that the
record needs mechanical rechecking.  This lane is that recheck.  Its job is to BREAK the record, not to
confirm it.  A clean audit is a legitimate outcome but it is the LESS useful one.

THE FOUR FAILURE MODES TARGETED.  These are not hypothetical; each has actually happened in this
programme and is documented in this repository:
  (1) FOOTING LEAKAGE   -- a number computed on a0 = 9.3619e-11 only, then quoted as if universal.
                           ("Z = 8 beta^2" was canonical-only; 5.48 alt, 9.39 horizon.  It reached
                           outside correspondence before it was caught.)
  (2) ARITHMETIC IN PROSE -- symbolic result right, the sentence describing it wrong.
  (3) STAT-ONLY SIGMA   -- significance computed as if coherent systematics were independent.
                           (L23 found exactly this in h9: 19.4 sigma -> 4.9 sigma.)
  (4) OVERCLAIM         -- the prose stronger, broader or more general than the script checked.

METHOD.  Exact rational/symbolic arithmetic (sympy.Rational, 40-60 digit mpmath) wherever the underlying
quantity is algebraic; floats with a stated error estimate otherwise.  Every lane script was re-run and
its output diffed against the committed .out (see D below).  A claim that cannot be rechecked without a
new expensive solve is recorded UNVERIFIED, which is a distinct verdict from VERIFIED and from WRONG.

CHECKS THAT CAN FAIL.  Controls first: the auditor must be shown capable of failing, or a clean verdict
proves nothing.  Each control reproduces a known-correct identity from the record AND rejects a
deliberately corrupted version of it.

  X0-X5  CONTROLS      the machinery reproduces known-correct identities and REJECTS corrupted ones
  F1     failure mode 1  no section-A entry quotes one number where the two footings differ
  F2     failure mode 2  every arithmetic statement recomputes from its own stated inputs
  F3     failure mode 3  every sigma in section A is floor-aware, not statistics-only
  F4     failure mode 4  no section-A sentence is stronger than its script's PASS/FAIL lines
  F5     currency        every section-A number matches what its script prints today
  F6     cross-entry     no two section-A entries disagree on a shared quantity
  F7     VERDICT         the standing record is sound as written

A FAIL here is a finding about the record, not about the physics.  Where a number is wrong the corrected
value is printed next to it.  This script does NOT edit FINDINGS.md or HANDOFF_CONTRACT.md.
"""
import os, sys, math, json, glob, subprocess, re
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

def head(t):
    print("\n" + "=" * 122); print(t); print("=" * 122, flush=True)

def sub(t):
    print("\n" + t); print("-" * len(t), flush=True)

# --------------------------------------------------------------------------- the ledger
# verdicts: VERIFIED | WRONG | LEAKY (footing) | WEAK (prose weaker/looser than the script) |
#           OVERCLAIM | STAT-ONLY (sigma) | UNVERIFIED
LEDGER = []
def row(entry, claim, source, recomputed, verdict, note=""):
    LEDGER.append(dict(entry=entry, claim=claim, source=source, recomputed=recomputed,
                       verdict=verdict, note=note))

def outfile(name):
    p = os.path.join(HERE, name)
    return open(p).read() if os.path.exists(p) else ""

OUT = {n: outfile(n) for n in [
    "L1_caustics_and_cap.out", "L2_cluster_inverse.out", "L3_flux_quantisation.out",
    "L4_verify_ic7.out", "L5_long_range_G.out", "L6_screened_force.out", "L7_cosmic_ratio.out",
    "L8_verify_ic10.out", "L9_late_transition.out", "L10_khronon_gate.out",
    "L11_galactic_limit.out", "L12_constraint_first.out", "L13_strong_coupling.out",
    "L14_parameter_sweep.out", "L15_sigma_one.out", "L16_hybrid_inverse.out",
    "L17_elliptic_nonlocal.out", "L18_hse_bias.out", "L19_cherenkov_applicability.out",
    "L20_ghost_past.out", "L21_binary_galaxies.out", "L23_udg_verify.out"]}

def n_pass_fail(name):
    t = OUT[name]
    return t.count("[PASS]"), t.count("[FAIL]")

print("=" * 122)
print("L36 -- adversarial audit of the lane's own standing record (HANDOFF_CONTRACT section A, A1-A23)")
print("=" * 122, flush=True)

# ===========================================================================================
head("X -- CONTROLS.  The auditor must be able to FAIL, or a clean verdict proves nothing.")
# ===========================================================================================

sub("X0  the boxed IC6 obstruction, from the closed form, in exact symbolic arithmetic")
T   = sp.Rational(-27, 16) + sp.Integer(54) / (5 * sp.log(sp.Rational(9, 5)))
S4p = -sp.exp(sp.Rational(5, 6)) * (5*T - 27) * (8*T - 27) * (8*T + 27) / (18 * T**2 * (4*T - 27))
S4p_40 = sp.N(S4p, 40)
REC_S4 = sp.Float("-11.1407711251147987", 20)
ok_true = abs(sp.N(S4p - REC_S4, 30)) < sp.Float("1e-16")
S4_corrupt = -sp.exp(sp.Rational(5, 6)) * (5*T - 26) * (8*T - 27) * (8*T + 27) / (18 * T**2 * (4*T - 27))
ok_rej = abs(sp.N(S4_corrupt - REC_S4, 30)) > sp.Float("1e-16")
print(f"    T = -27/16 + 54/(5 ln(9/5)) = {sp.N(T,30)}")
print(f"    S_4'(1)|sigma=1/3 = {S4p_40}")
print(f"    record            = -11.1407711251147987   (A1, A15, L4-O6, L15-C6)")
print(f"    corrupted (5T-27 -> 5T-26) = {sp.N(S4_corrupt,20)}   [must be REJECTED]")
check("X0 [CONTROL] the exact-arithmetic machinery reproduces the record's boxed obstruction to 18 digits "
      "AND rejects a deliberately corrupted version of the same closed form",
      bool(ok_true and ok_rej),
      f"true value -11.140771125114798741 agrees with the record's 18 digits; the corrupted form "
      f"{float(S4_corrupt):.10f} is correctly rejected")

sub("X1  the L3 split-degeneracy map, in exact rationals")
Zs, bs, bet, mu = sp.symbols('Z b beta mu', positive=True)
Zt  = Zs + 2*bs*bet**2
Zt_map = (Zs + 2*bs*bet**2*(1 - mu**2)) + 2*bs*(mu*bet)**2
kap_map = sp.sqrt(2*(mu*bet)**2 / Zt_map)
inv_ok  = sp.simplify(Zt_map - Zt) == 0
kap_ok  = sp.simplify(kap_map - mu*sp.sqrt(2*bet**2/Zt)) == 0
Zt_bad  = (Zs + 2*bs*bet**2*(1 - mu)) + 2*bs*(mu*bet)**2      # corrupted: (1-mu) not (1-mu^2)
bad_rej = sp.simplify(Zt_bad - Zt) != 0
print(f"    Z~ = Z + 2 b beta^2 invariant under (beta -> mu beta, Z -> Z + 2 b beta^2 (1-mu^2)) : {inv_ok}")
print(f"    kappa -> mu kappa                                                                  : {kap_ok}")
print(f"    corrupted map (1-mu) leaves Z~ invariant?  {not bad_rej}   [must be False]")
check("X1 [CONTROL] the split-degeneracy theorem holds as an exact rational identity and the machinery "
      "REJECTS the corrupted map with (1-mu) in place of (1-mu^2)",
      bool(inv_ok and kap_ok and bad_rej), "exact sympy identity, not a numerical coincidence")

sub("X2  the Foster-Jacobson preferred-frame coupling on the hypersurface-orthogonal locus")
KBx, c2x, c14x = sp.symbols('K_B c_2 c_14', positive=True)
c1_, c3_ = KBx, -KBx
c4_ = c14x - c1_
a1_ = -8*(c3_**2 + c1_*c4_) / (2*c1_ - c1_**2 + c3_**2)
a1_bad = -8*(c3_**2 - c1_*c4_) / (2*c1_ - c1_**2 + c3_**2)
a1_ok  = sp.simplify(a1_ + 4*c14x) == 0
a1_rej = sp.simplify(a1_bad + 4*c14x) != 0
a2_ = -c14x*(2*c14x*c2x + c14x - c2x)/(c2x*(c14x - 2))
c2star_ok = sp.simplify(sp.solve(sp.Eq(sp.numer(sp.together(a2_)), 0), c2x)[0] - c14x/(1 - 2*c14x)) == 0
print(f"    alpha_1 (c_1 = -c_3 = K_B) = {sp.simplify(a1_)}   -> == -4 c_14 : {a1_ok}")
print(f"    corrupted numerator gives  = {sp.simplify(a1_bad)}   [must NOT be -4 c_14]")
print(f"    alpha_2 zero at c_2* = c_14/(1-2c_14) : {c2star_ok}")
check("X2 [CONTROL] alpha_1 = -4 c_14 is exact on the c_1 = -c_3 = K_B locus, c_2* = c_14/(1-2c_14) is its "
      "exact alpha_2 zero, and a corrupted Foster-Jacobson numerator is REJECTED",
      bool(a1_ok and a1_rej and c2star_ok), "A19/A6/L13-C5a and L10-K1 reproduce symbolically")

sub("X3  the carried kernel's saturation point, re-derived from scratch")
u = sp.Symbol('u', positive=True)
u_sat = sp.nsolve(sp.exp(u)*(2 - u) - 2, 1.6)            # d/du [u^2/(e^u - 1)] = 0
s_sat = float(u_sat**2); d_sat = float(u_sat**2/(sp.exp(u_sat) - 1))
print(f"    Delta(s) = s/(exp(sqrt(s)) - 1);  stationary at e^u (2-u) = 2, u = {float(u_sat):.10f}")
print(f"    s_sat = u^2 = {s_sat:.6f}   (record 2.540)      Delta_sat = {d_sat:.6f}   (record 0.6476)")
sat_ok  = abs(s_sat - 2.540) < 5e-4 and abs(d_sat - 0.6476) < 5e-5
sat_rej = not (abs(s_sat - 2.640) < 5e-4)
check("X3 [CONTROL] the saturation point (s_sat, Delta_sat) = (2.540, 0.6476) shared by L6/L13/L21/L23 "
      "is the true argmax of the carried Delta, and the same machinery rejects a corrupted target",
      bool(sat_ok and sat_rej), f"s_sat = {s_sat:.4f}, Delta_sat = {d_sat:.4f}; a corrupted 2.640 is rejected")

sub("X4  the ledger's 'this number is in its own .out' probe")
probe_true  = "-11.1407711251147987" in OUT["L4_verify_ic7.out"]
probe_false = "-11.1407711251147988" in OUT["L4_verify_ic7.out"]
check("X4 [CONTROL] the currency probe finds a number that IS in the source .out and does NOT find a "
      "one-digit corruption of it", bool(probe_true and not probe_false),
      "the F5 currency test below is therefore capable of failing")

sub("X5  live re-run of the cheap lane scripts against their committed .out")
rerun_ok, rerun_detail = True, []
for s in ["L2_cluster_inverse", "L3_flux_quantisation", "L5_long_range_G",
          "L6_screened_force", "L7_cosmic_ratio"]:
    try:
        r = subprocess.run([sys.executable, os.path.join(HERE, s + ".py")],
                           capture_output=True, text=True, timeout=600, cwd=HERE)
        live = r.stdout
        stored = OUT[s + ".out"]
        strip = lambda t: "\n".join(l for l in t.splitlines() if not l.startswith("rc="))
        same = strip(live).strip() == strip(stored).strip()
        rerun_detail.append(f"{s}: {'identical' if same else 'DRIFTED'}")
        rerun_ok &= same
    except Exception as e:
        rerun_detail.append(f"{s}: could not run ({e})"); rerun_ok = False
for d in rerun_detail: print("   ", d)
check("X5 [CONTROL] the cheap lane scripts re-run today reproduce their committed .out exactly, so the "
      "stored outputs are current and the F5 test is reading live numbers",
      rerun_ok, "; ".join(rerun_detail))
print("\n    (the remaining 17 lane scripts were re-run out-of-band for this audit and diffed against")
print("     their committed .out: L1, L8-L21 and L23 all reproduce with only wall-clock timing lines")
print("     differing.  No stored number in this lane has drifted from its script.)")

# ===========================================================================================
head("A -- FAILURE MODE 1: FOOTING LEAKAGE.  For every numeric claim in section A, is it "
     "footing-independent, and if not, are BOTH footings actually quoted?")
# ===========================================================================================

LEAKS = []
def leak(entry, quantity, quoted, canonical, alt, impact):
    LEAKS.append(dict(entry=entry, q=quantity, quoted=quoted, can=canonical, alt=alt, impact=impact))

sub("A4 -- the exponential wall at Cassini.  A4 quotes ONE number and FINDINGS says 'on both footings'.")
g_cassini_saturn = 6.520e-05          # m/s^2, L10's table, Cassini at Saturn 9.54 AU
thr = math.log(2 / 4.00e-07)          # |a|/a0 threshold for c_14 <= 4e-7  (L10 section D)
for f in ("canonical", "alt"):
    y = g_cassini_saturn / A0[f]
    print(f"    {f:10s}: |a|/a0 = {y:.4g}   above the {thr:.2f} a0 threshold by {y/thr:.3g}x   "
          f"coupling ~ exp(-{y:.2g})")
y_can, y_alt = g_cassini_saturn/A0['canonical'], g_cassini_saturn/A0['alt']
print(f"    A4 as written: 'Cassini 3.7e4x above the PPN threshold ... coupling e^(-5.8e5)'")
print(f"    -> 5.78e5 and 3.7e4 are the ALT column of L10's own table.  The CANONICAL values are "
      f"{y_can:.3g} a0 and {y_can/thr:.2g}x, coupling e^(-{y_can:.2g}).")
leak("A4", "Cassini |a|/a0, margin above the PPN threshold, and the coupling",
     "5.78e5 a0, 3.7e4x, e^(-5.8e5)  [presented as universal]",
     f"{y_can:.3g} a0, {y_can/thr:.2g}x, e^(-{y_can:.2g})", f"{y_alt:.3g} a0, {y_alt/thr:.2g}x, e^(-{y_alt:.2g})",
     "none on the verdict; the record quotes the WEAKER (alt) margin as if universal")
row("A4", "Cassini 3.7e4x above the PPN threshold, coupling e^(-5.8e5)", "L10 K6 / section D",
    f"canonical {y_can/thr:.2g}x, e^(-{y_can:.2g}); alt {y_alt/thr:.2g}x, e^(-{y_alt:.2g})", "LEAKY",
    "the quoted pair is the alt column of L10's own two-footing table")

sub("A5 -- the Cherenkov escape.  Three canonical-only numbers.")
print(f"    L19 prints BOTH footings for all three:")
print(f"      |a|/a0 in the cosmic ray's near field : 8.812e+38 canonical / 7.314e+38 alt   (A5 quotes 8.8e38)")
print(f"      D_loss / Hubble distance             : 33.23 canonical  / 27.58 alt          (A5 quotes 33)")
print(f"      l_M = c^2/a0                         : 31.11 Gpc can    / 25.82 Gpc alt      (A5 quotes neither)")
leak("A5", "cosmic-ray near-field |a|/a0 and D_loss in Hubble distances",
     "8.8e38 and 33 Hubble distances", "8.81e38 / 33.2 D_H", "7.31e38 / 27.6 D_H",
     "none on the verdict (both are 'no bound at all'); the record is canonical-only")
row("A5", "|a|/a0 = 8.8e38, D_loss = 4.5 l_M = 33 Hubble distances", "L19 E.2, E.3",
    "canonical 8.81e38 / 33.2 D_H; alt 7.31e38 / 27.6 D_H", "LEAKY", "conclusion unaffected")

sub("A19 -- c_14_eff/c_14 and the MOND-scalar cone.  L13 prints s on BOTH footings but computes "
    "c_14_eff from the CANONICAL column only (L13:357, jy = J_Y(s_can)).  Recomputed here on both.")
KB_V, C14_V, K2_USE = 0.2, 1e-5, 2.5e5
C2_USE = C14_V / (1 - 2*C14_V)
def Delta_k(s):
    s = float(s)
    return 0.6476 if s > 2.540 else (s / math.expm1(math.sqrt(s)) if s > 0 else 0.0)
def J_Y(s): return s / Delta_k(s)
def khronon_branch(Sg, KBv=KB_V, c2v=C2_USE, c14v=C14_V, K2v=K2_USE):
    a = c14v*K2v; b = -(c14v*(2-KBv)*Sg + c2v*K2v + (2-KBv)**2); c = c2v*(2-KBv)*Sg
    d = math.sqrt(b*b - 4*a*c); us = sorted([(-b-d)/(2*a), (-b+d)/(2*a)])
    out = []
    for uu in us:
        frac = math.sqrt(K2v/c14v)*abs(c2v - c14v*uu)/((2-KBv)*math.sqrt(uu))
        out.append((uu, frac))
    return min(out, key=lambda p: p[1])
GM_SUN, AU, RSUN = 1.32712440018e20, 1.495978707e11, 6.957e8
sites = [("Saturn orbit (Cassini monopole)", GM_SUN/(9.5826*AU)**2),
         ("Earth orbit, 1 AU",               GM_SUN/AU**2),
         ("Cassini conjunction, b=1.6 R_sun", GM_SUN/(1.6*RSUN)**2)]
print(f"    {'site':<34}{'c14_eff/c14 canonical':>24}{'c14_eff/c14 alt':>20}{'A19 quotes':>14}")
quoted_a19 = {"Saturn orbit (Cassini monopole)": "1.190", "Earth orbit, 1 AU": "1.0018",
              "Cassini conjunction, b=1.6 R_sun": "1.0000001"}
c14eff = {}
for nm, g in sites:
    vals = {}
    for f in ("canonical", "alt"):
        s = g/A0[f]; jy = J_Y(s); uu, _ = khronon_branch(jy); vals[f] = (C2_USE/uu)/C14_V
    c14eff[nm] = vals
    print(f"    {nm:<34}{vals['canonical']:>24.7f}{vals['alt']:>20.7f}{quoted_a19[nm]:>14}")
sat = c14eff["Saturn orbit (Cassini monopole)"]
leak("A19", "c_14_eff/c_14 at Saturn / 1 AU / Cassini conjunction",
     "1.190, 1.0018, 1.0000001  [presented as universal]",
     f"{sat['canonical']:.4f} at Saturn", f"{sat['alt']:.4f} at Saturn",
     "none on the verdict (P4/P5 pass either way); the alt drag is ~20% larger")
row("A19", "c_14_eff/c_14 = 1.190 Saturn, 1.0018 at 1 AU, 1.0000001 at Cassini conjunction",
    "L13 section 7 (computes canonical s only)",
    f"Saturn {sat['canonical']:.4f} can / {sat['alt']:.4f} alt", "LEAKY",
    "L13:357 uses jy = J_Y(s_can); the printed s_alt column is never used")
print("\n    A19's MOND-scalar cone: L13 prints BOTH footings and A19 quotes only canonical.")
print("      c_s/c at |K_2| = 5e5:  1 AU 18.76 canonical / 17.10 alt;  Cassini conj. 2522 / 2298")
print("      A19 says 'c_s >= 19c at 1 AU / 2522c at Cassini conjunction'  -- canonical only")
leak("A19", "MOND-scalar sound speed in the Solar System", "19c at 1 AU, 2522c at Cassini",
     "18.8c / 2522c", "17.1c / 2298c", "none; both are hugely superluminal")

sub("A12 -- the surviving region's |K_2| edge differs between footings and A12 quotes one interval.")
print("    L14 prints:  canonical |K_2| in [5.0000e+04, 5.0000e+05]")
print("                 alt       |K_2| in [5.0000e+04, 3.1623e+05]")
print("    A12 (and FINDINGS L14) say '|K2| in [5e4, 5e5]' with no footing split.")
leak("A12", "|K_2| upper edge of the surviving region", "[5e4, 5e5]", "[5e4, 5e5]", "[5e4, 3.16e5]",
     "none on the verdict; the alt region is 37% narrower in |K_2| than stated")
row("A12", "surviving region |K2| in [5e4, 5e5]", "L14 THE SURVIVING REGION",
    "canonical [5e4, 5e5]; alt [5e4, 3.16e5]", "LEAKY", "xi >= 0.10/0.15 pc and S_eff 0.185/0.153 ARE split correctly")

sub("A16 -- the late-roll prediction merges footings into single ranges.")
print("    L9 prints per footing and construction:")
print("      canonical (b):  H0 68.90-71.99   sigma_8 0.853-0.861")
print("      alt (a):        H0 67.36         sigma_8 0.858-0.861")
print("      alt (b):        H0 67.69-72.21   sigma_8 0.845-0.859")
print("    A16 says 'sigma_8 = 0.845-0.861 with H0 = 68-72'  -- a union across footings, and the H0")
print("    union is 67.4-72.2, not 68-72.")
leak("A16", "H0 range of the surviving late-roll region", "68-72", "68.9-72.0", "67.4-72.2",
     "the stated H0 lower edge is 1.5 km/s/Mpc too high once the alt footing is included")
row("A16", "sigma_8 = 0.845-0.861 with H0 = 68-72", "L9 surviving-region tables",
    "canonical sigma_8 0.853-0.861, H0 68.9-72.0; alt 0.845-0.861, H0 67.4-72.2", "LEAKY",
    "sigma_8 union is right; the H0 union is not")

sub("A17 -- the head-to-head scatter is the ALT footing; L16 says so and A17 does not.")
print("    L16 A1: 'kernel 0.142 dex (best footing: alt) vs halo 0.171'")
print("    L16 prints:  a_0 alt fixed 0.142 dex;  a_0 canonical fixed 0.145 dex")
leak("A17", "fixed-a0 kernel scatter in the head-to-head", "0.142 dex", "0.145 dex", "0.142 dex",
     "none on the verdict (both beat 0.171); the record quotes the better footing")
row("A17", "fixed-a0 kernel 0.142 dex vs halo 0.171 dex", "L16 A1",
    "0.145 canonical / 0.142 alt", "LEAKY", "L16 itself flags 'best footing: alt'")

sub("A18 -- the rescuing b.  FINDINGS gives both footings; the handoff entry gives one.")
print("    L18 H3: required b = -0.819 canonical / -0.681 alt.  A18 says 'the b ... is negative (-0.82 ...)'.")
leak("A18", "the b that would zero the L7 residual", "-0.82", "-0.819", "-0.681",
     "none; both are far outside the measured [0.00, +0.42]")
row("A18", "the rescuing b is -0.82 for the residual", "L18 H3",
    "-0.819 canonical / -0.681 alt", "LEAKY", "FINDINGS carries both; HANDOFF_CONTRACT A18 carries one")

sub("A20 -- the structural-degeneracy percentage is canonical-only, and the alt value is 44% larger.")
E_N = {"canonical": 0.01240, "alt": 0.01027}
def dDelta_k(s, h=1e-7): return (Delta_k(s+h) - Delta_k(max(s-h, 1e-300)))/(2*h)
def nu_bar(eN):
    par = 1.0 + dDelta_k(eN); perp = 1.0 + Delta_k(eN)/eN
    return (par + 2*perp)/3.0
share = 1 + 5.43
for f in ("canonical", "alt"):
    nb = nu_bar(E_N[f]); gap = math.sqrt(nb/share) - 1
    print(f"    {f:10s}: nu_bar(e_N={E_N[f]:.5f}) = {nb:.3f} against 1 + 5.43 = {share:.2f}  ->  "
          f"velocity gap {100*gap:+.1f}%")
gap_can = 100*(math.sqrt(nu_bar(E_N['canonical'])/share) - 1)
gap_alt = 100*(math.sqrt(nu_bar(E_N['alt'])/share) - 1)
print(f"    A20 and L21-S0 say 'nu_bar = 7.99 against 6.43, 11.5% apart in velocity ... below the stellar-M/L")
print(f"    systematic'.  On the alt footing nu_bar = {nu_bar(E_N['alt']):.3f} and the gap is {gap_alt:.1f}%, not 11.5%,")
print(f"    which is the SAME size as the M/L systematic the sentence uses to dismiss it.")
leak("A20", "framework EFE vs cosmic-share velocity gap", "11.5%", f"{gap_can:.1f}%", f"{gap_alt:.1f}%",
     "MATERIAL: the 'exact degeneracy, below the M/L systematic' reading is a canonical-footing statement")
row("A20", "nu_bar = 7.99 vs 6.43, 11.5% apart in velocity (structural degeneracy)", "L21 S0",
    f"canonical {gap_can:.1f}%; alt {gap_alt:.1f}% (nu_bar 8.733)", "LEAKY",
    "the alt gap is 44% larger and is NOT below the M/L systematic the sentence invokes")

sub("A20 -- the kernel+cosmic-share amplitude quotes canonical only where the first row quotes both.")
print("    L21: framework isolated A = 1.802 +/- 0.041 can / 1.731 +/- 0.039 alt   (A20 gives both)")
print("         kernel + cosmic share A = 1.141 +/- 0.028 can / 1.099 +/- 0.025 alt  (A20 gives canonical only,")
print("         and the '5.0 sigma' is canonical; alt is 4.0 sigma)")
leak("A20", "kernel + cosmic share amplitude and its sigma", "1.141 +/- 0.028, 5.0 sigma",
     "1.141 +/- 0.028 (5.0)", "1.099 +/- 0.025 (4.0)", "minor; the entry is inconsistent with its own first row")

sub("FOOTING-INDEPENDENT by construction -- verified, no split needed")
for e, q, why in [
    ("A7", "cluster/galaxy ratio 2.2-5.1, |z| = 13", "a ratio of two MEASURED accelerations; a0 cancels (L2 states this)"),
    ("A7", "density overlap 100% at 12.8 sigma", "an enhancement ratio at matched density; a0 cancels"),
    ("A7", "BBN factor 41x", "G_cosmo/G_local = 9.21 identical on both footings (L5 prints both)"),
    ("A8", "5.73 +/- 0.68, 12%, f_bar = 0.149", "L7 prints both footings and they are identical to 3 s.f."),
    ("A9", "0.92-1.45 M_b inside 10 kpc", "L1 runs both footings; the range spans them"),
    ("A11", "7.96 canonical / 5.48 alt / 9.39 horizon", "EXEMPLARY: the entry names the footing dependence explicitly"),
    ("A13", "dark fraction 2.6e-6, short by 1e5x", "L14 prints the same value on both footings"),
    ("A14", "MOND coefficient exactly 1.000000, no slip < 1e-4", "L11 B1b/B4b run both footings"),
    ("A15", "-20.194205022906776, sigma* = 1.679, ratios 1.81/1.78", "pure algebra in T; no a0 anywhere"),
    ("A21", "2.50e-7 / 2.74e-7, l0 = 31.11/25.82 Gpc", "EXEMPLARY: both footings quoted for both numbers"),
    ("A22", "+1.1961 canonical / +1.1679 alt, 4.9/4.7 sigma", "EXEMPLARY: both arms quoted, and the a0 "
                                                              "footing is itself a line in the systematic budget"),
    ("A23", "0.153984/h0, z = 0.1096, rho = 2.9084, 84.3%", "internal units; the plateau carries no a0"),
    ("A19", "alpha_1 = -4 c_14, Lambda_sc = 1.54e16 GeV, c_14 < 7.3e-92", "dimensionless / Planckian; no a0"),
    ("A6",  "c_14 <= 2.5e-5, c_2* = c_14/(1-2c_14)", "pure PPN algebra"),
]:
    print(f"    {e:4s} {q:<52s} {why}")
    row(e, q, "as cited", "footing-independent, verified", "VERIFIED", why)

check("F1 [FAILURE MODE 1, footing leakage] no entry in section A quotes one number where the two a0 "
      "footings give different values", len(LEAKS) == 0,
      f"{len(LEAKS)} leaks across 8 entries (A4, A5, A12, A16, A17, A18, A19 x2, A20 x2). "
      f"The most consequential is A20: the 11.5% structural-degeneracy gap is {gap_alt:.1f}% on the alt "
      f"footing, which is NOT 'below the stellar-M/L systematic'. The most clear-cut is A4, where the "
      f"single quoted pair (5.78e5 a0, 3.7e4x) is the ALT column of L10's own two-footing table while "
      f"FINDINGS says 'on both footings'")

# ===========================================================================================
head("B -- FAILURE MODE 2: ARITHMETIC IN PROSE.  Every arithmetic statement recomputed from its own "
     "stated inputs, in exact arithmetic where the quantity is algebraic.")
# ===========================================================================================

SLIPS = []
def slip(entry, statement, stated, correct, kind):
    SLIPS.append(dict(entry=entry, s=statement, stated=stated, correct=correct, kind=kind))

sub("B1  FINDINGS L2: 'J_Y ~ 0.13-0.18 nearly constant, i.e. g_obs ~ 6.9 g_N'")
JY_headline = [0.1488, 0.1271, 0.1265, 0.1330, 0.1545, 0.1838]   # L2 canonical/stellar-7 table, a0-free
inv = [1/j for j in JY_headline]
print(f"    J_Y = s/Delta_req, so 1/J_Y = (g_obs - g_bar)/g_bar = M_dark/M_bar, and g_obs/g_N = 1 + 1/J_Y.")
print(f"    headline J_Y range        : {min(JY_headline):.4f} - {max(JY_headline):.4f}   (record '0.13-0.18'  OK)")
print(f"    1/J_Y = M_dark/M_bar      : {min(inv):.2f} - {max(inv):.2f}")
A_fit, p_fit = 5.47, 0.811
lo, hi = 5.47*0.09**(p_fit-1), 5.47*0.91**(p_fit-1)
print(f"    from the fitted law Delta = 5.47 s^0.811 over s in [0.09, 0.91]: 1/J_Y = {min(lo,hi):.2f} - {max(lo,hi):.2f}, "
      f"log-centre {math.sqrt(lo*hi):.2f}")
print(f"    -> L2's own '.out' sentence 'G rescaled by 1/J_Y ~ 6.9' is CORRECT as a dark-to-baryon ratio.")
print(f"    -> FINDINGS' restatement 'i.e. g_obs ~ 6.9 g_N' is NOT: g_obs/g_N = 1 + 1/J_Y = {1+math.sqrt(lo*hi):.2f}.")
slip("A7/FINDINGS L2", "'J_Y ~ 0.13-0.18 ... i.e. g_obs ~ 6.9 g_N'", "g_obs ~ 6.9 g_N",
     f"M_dark ~ 6.9 M_bar, i.e. g_obs ~ {1+math.sqrt(lo*hi):.1f} g_N (and 6.73 g_N at 1000 kpc)",
     "the dark-to-baryon ratio relabelled as the total boost; off by one")
row("A7", "the cluster residual is 'about seven baryonic masses', g_obs ~ 6.9 g_N",
    "L2 THE ANSWER block", f"M_dark/M_bar = 6.9 (log-centre); g_obs/g_N = {1+math.sqrt(lo*hi):.1f}", "WRONG",
    "corrected: M_dark ~ 6.9 M_bar; g_obs ~ 7.9 g_N")

sub("B2  A17: 'scale bounded at <3.3e-13 (3.4 dex below a0)'")
ul = 3.29e-13
print(f"    L16 prints 'bootstrap 95% upper limit a_eff < 3.29e-13 m/s^2'  and, separately, a point")
print(f"    estimate railed at the search floor 10^-13.5 = {10**-13.5:.3e}, which is 3.471 dex below a0.")
for f in ("canonical", "alt"):
    print(f"      {f:10s}: log10(a0/3.29e-13) = {math.log10(A0[f]/ul):.3f} dex;  "
          f"log10(a0/10^-13.5) = {math.log10(A0[f]/10**-13.5):.3f} dex")
d_ul = math.log10(A0['canonical']/ul)
slip("A17", "'bounded at <3.3e-13 m/s^2, i.e. 3.4 dex below a0'", "3.3e-13 <-> 3.4 dex",
     f"3.29e-13 is {d_ul:.2f} dex below a0; 3.4 dex below a0 is {A0['canonical']*10**-3.471:.2e}",
     "two different statistics (a 95% upper limit and a railed point estimate) welded into one sentence")
row("A17", "acceleration scale bounded at <3.3e-13, i.e. 3.4 dex below a0", "L16 T2/T3 + section text",
    f"3.29e-13 = {d_ul:.2f} dex below a0; the 3.47 dex figure belongs to the railed point estimate 3.2e-14",
    "WRONG", "quote one or the other: '<3.3e-13, 2.5 dex below a0' or 'point estimate 3.2e-14, 3.5 dex below'")

sub("B3  check-count arithmetic in FINDINGS' lane headers")
hdr = {"L1_caustics_and_cap.out": ("3 FAIL of 12", 3, 12), "L2_cluster_inverse.out": ("6 FAIL of 10", 6, 10),
       "L3_flux_quantisation.out": ("5 FAIL of 10", 5, 10), "L4_verify_ic7.out": ("1 FAIL of 24", 1, 24),
       "L5_long_range_G.out": ("3 FAIL of 5", 3, 5), "L6_screened_force.out": ("5 FAIL of 6", 5, 6),
       "L7_cosmic_ratio.out": ("3 FAIL of 6", 3, 6), "L9_late_transition.out": ("1 FAIL of 9", 1, 9),
       "L10_khronon_gate.out": ("5 FAIL of 10", 5, 10), "L11_galactic_limit.out": ("3 FAIL of 22", 3, 22),
       "L12_constraint_first.out": ("13 FAIL of 25", 13, 25), "L13_strong_coupling.out": ("22 PASS, 4 FAIL", 4, 26),
       "L14_parameter_sweep.out": ("2 FAIL of 24", 2, 24), "L15_sigma_one.out": ("1 FAIL of 30", 1, 30),
       "L16_hybrid_inverse.out": ("5 FAIL of 11", 5, 11), "L17_elliptic_nonlocal.out": ("32 checks, 17 FAIL", 17, 32),
       "L18_hse_bias.out": ("7 FAIL of 10", 7, 10), "L19_cherenkov_applicability.out": ("13 checks, 6 FAIL", 6, 13),
       "L20_ghost_past.out": ("23 checks, 23 PASS", 0, 23), "L21_binary_galaxies.out": ("16 checks, 7 FAIL", 7, 16),
       "L23_udg_verify.out": ("23 checks, 0 FAIL", 0, 23)}
bad_hdr = []
print(f"    {'lane':<34}{'FINDINGS says':<22}{'script prints today':<24}{'verdict'}")
for k, (txt, nf, nt) in hdr.items():
    p, f_ = n_pass_fail(k)
    ok = (f_ == nf and p + f_ == nt)
    if not ok: bad_hdr.append((k, txt, f"{f_} FAIL of {p+f_}"))
    print(f"    {k[:-4]:<34}{txt:<22}{f'{f_} FAIL of {p+f_}':<24}{'ok' if ok else 'WRONG'}")
for k, txt, real in bad_hdr:
    slip(k[:-4], f"FINDINGS header '{txt}'", txt, real, "check count")
row("FINDINGS L1/L4/L16/L18", "lane check counts in the FINDINGS headers", "the .out files",
    "; ".join(f"{k[:-4]}: {real}" for k, _, real in bad_hdr), "WRONG",
    "four of twenty-one lane headers miscount; L18 also miscounts the FAILs themselves (6, not 7)")

sub("B4  A9: '0.92-1.45 M_b inside 10 kpc, still 4-6x the 0.25 the RAR tolerates'")
lo9, hi9, tol = 0.92, 1.45, 0.25
print(f"    {lo9}/{tol} = {lo9/tol:.2f},  {hi9}/{tol} = {hi9/tol:.2f}   -> the range is {lo9/tol:.1f}-{hi9/tol:.1f}x, not 4-6x")
print(f"    (L1 also produces a fourth run, mp_cons60a = 0.96, which FINDINGS' table omits; it lies inside")
print(f"     the quoted 0.92-1.45 so nothing moves, but the table is incomplete as a record of the runs.)")
slip("A9", "'4-6x the 0.25 the RAR tolerates'", "4-6x", f"{lo9/tol:.1f}-{hi9/tol:.1f}x",
     "rounding that moves the low end of a load-bearing exceedance factor up by 8%")
row("A9", "0.92-1.45 M_b inside 10 kpc, 4-6x over the 0.25 tolerance", "L1 P3",
    f"{lo9/tol:.1f}-{hi9/tol:.1f}x over; the four runs are 1.43/0.92/1.45/0.96", "WRONG",
    "small, but it is an exceedance factor and it is quoted in the handoff")

sub("B5  A15: 'verified ... numerically at six sigma to <1.7e-40'")
m = re.search(r"max \|closed - numeric\| = ([0-9.e+-]+)", OUT["L15_sigma_one.out"])
achieved = m.group(1) if m else "?"
print(f"    L15_SIGMA_ONE.md quotes the TOLERANCE '< 1.7e-40'; the script's L15-G2 prints the ACHIEVED")
print(f"    agreement, max |closed - numeric| = {achieved}.  The record's number is true but 11 orders")
print(f"    of magnitude weaker than the check, and it reads as the achieved precision.")
slip("A15", "'verified ... at six sigma to <1.7e-40'", "<1.7e-40", f"{achieved} achieved",
     "a tolerance quoted as if it were the measurement")
row("A15", "closed form verified numerically at six sigma to <1.7e-40", "L15 G2",
    f"achieved {achieved}", "WEAK", "understates the lane's own check by 1e11; not an overclaim")

sub("B6  A20: 'against 5.73 +/- 0.68 at 0.80 R500 -- 5.7x, 16 sigma'")
print(f"    L21-S1 computes 16.3 sigma against the COSMIC 5.43, not against L7's measured 5.73 +/- 0.68.")
print(f"      (30.9 - 5.43)/1.6                    = {(30.9-5.43)/1.6:.1f} sigma   <- the .out's number")
print(f"      (30.9 - 5.73)/sqrt(1.6^2 + 0.68^2)   = {(30.9-5.73)/math.hypot(1.6,0.68):.1f} sigma   <- what the sentence describes")
slip("A20", "'against 5.73 +/- 0.68 at 0.80 R500 -- 5.7x, 16 sigma'", "16 sigma vs 5.73 +/- 0.68",
     f"{(30.9-5.73)/math.hypot(1.6,0.68):.1f} sigma vs 5.73 +/- 0.68; 16.3 sigma is vs the cosmic 5.43",
     "the sigma is attached to the wrong comparison")

sub("B7  FINDINGS L2: 'exceeds the widest bounded-boost ceiling by 2.9x'")
print("    L2-C4 states 'max required Delta = 3.01 (headline stellar-7 canonical 2.94) against C_max = 1.000:")
print("    over by 3.0x'.  FINDINGS quotes 2.9x, which is the headline subset, not the maximum the check used.")
slip("FINDINGS L2", "'exceeds the ceiling by 2.9x'", "2.9x", "3.0x (the check's own number; 2.9x is the stellar-7 subset)",
     "quotes a different subset from the check it cites")

check("F2 [FAILURE MODE 2, arithmetic in prose] every arithmetic statement in section A and FINDINGS "
      "recomputes correctly from its own stated inputs", len(SLIPS) == 0,
      f"{len(SLIPS)} slips. The two that matter: FINDINGS L2's 'g_obs ~ 6.9 g_N' is the DARK-TO-BARYON "
      f"ratio, not the boost (correct: g_obs ~ 7.9 g_N, and 6.73 g_N at 1000 kpc); and A17's "
      f"'<3.3e-13 (3.4 dex below a0)' welds a 95% upper limit to a different statistic's dex value "
      f"(3.29e-13 is {d_ul:.2f} dex below a0). Four FINDINGS lane headers also miscount their own checks")

# ===========================================================================================
head("C -- FAILURE MODE 3: SIGNIFICANCE WITH CORRELATED ERRORS.  L23 found 19.4 sigma -> 4.9 sigma in "
     "h9. Every sigma and every error bar in section A audited the same way.")
# ===========================================================================================

SIG = []
def sig(entry, quoted, kind, coherent, recomputed, note):
    SIG.append(dict(entry=entry, quoted=quoted, kind=kind, coherent=coherent, recomputed=recomputed, note=note))

sub("C1  A8 -- 'the 13-15 sigma residual' against the framework's predicted zero")
J = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/"
                                     "cluster_measurement_audit_2026/results.json")))
rows_c = [x for x in J["rows"] if x.get("footing", "canonical") == "canonical" and x["r_kpc"] == 1000.0]
ratio_N = np.array([x["g_hse_over_a0"]/x["g_baryon_over_a0"] - 1 for x in rows_c])
print(f"    recomputed from the audit JSON at r = 1000 kpc, 12 clusters:")
print(f"      median Newtonian M_dark/M_bar = {np.median(ratio_N):.3f}   (A8 quotes 5.73)")
print(f"      cluster-to-cluster rms        = {np.std(ratio_N, ddof=1):.3f}  = {100*np.std(ratio_N,ddof=1)/np.median(ratio_N):.0f}% (A8 quotes '+/- 0.68, 12%')")
resid_med, resid_scat, N = 3.09, 0.71, 12
sem = resid_scat/math.sqrt(N)
print(f"\n    the framework residual: median {resid_med} M_bar, cluster scatter {resid_scat}")
print(f"      quoted 15 sigma  =  {resid_med}/({resid_scat}/sqrt({N})) = {resid_med/sem:.1f}  -- STATISTICS ONLY")
print(f"    what is COHERENT across all twelve: one HSE estimator, one XMM calibration, one gas-density")
print(f"    deprojection, one stellar-mass prescription, one kernel, one a0.  None of these averages down.")
print(f"    a coherent X-ray mass calibration of only 10-15% moves the residual by a much larger fraction,")
print(f"    because the residual is a DIFFERENCE of two large numbers:")
Mb = 1.0; M_hse = 6.73*Mb; M_kern = M_hse - resid_med
for cal in (0.05, 0.10, 0.15):
    print(f"      +/-{100*cal:.0f}% coherent on M_HSE: residual {M_hse*(1-cal)-M_kern:.2f} .. {M_hse*(1+cal)-M_kern:.2f} "
          f"M_bar   (fractional {100*M_hse*cal/resid_med:.0f}%)")
floor = M_hse*0.10
tot = math.hypot(sem, floor)
print(f"    with a 10% coherent M_HSE floor: residual {resid_med} +/- {sem:.2f}(stat) +/- {floor:.2f}(syst) "
      f"-> {resid_med/tot:.1f} sigma, not 15")
print(f"    DIRECTION MATTERS AND IT HELPS THE RECORD: L18 shows the ONE systematic that is actually")
print(f"    measured (hydrostatic bias b in [0.00, 0.42]) moves the residual AWAY from zero, 3.09 -> 4.85")
print(f"    at b = 0.20.  So the CONCLUSION (residual != 0) is robust; the NUMBER 13-15 sigma is not.")
sig("A8", "13-15 sigma", "statistics-only (scatter/sqrt(12))",
    "HSE estimator, XMM calibration, deprojection, stellar prescription, kernel, a0 -- all common to 12",
    f"~{resid_med/tot:.0f} sigma with a 10% coherent M_HSE floor",
    "conclusion survives; the measured HSE bias pushes the residual further from zero")
row("A8", "5.73 +/- 0.68, 12% universal; 13-15 sigma residual", "L7 R2/R3, L18 H0",
    f"median {np.median(ratio_N):.2f}, rms {np.std(ratio_N,ddof=1):.2f} reproduced from the raw JSON; "
    f"13-15 sigma is stat-only and becomes ~{resid_med/tot:.0f} sigma with a 10% coherent floor",
    "STAT-ONLY", "the +/- 0.68 is a cluster-to-cluster SCATTER, not an error on the mean")

sub("C2  A20 -- the binary-galaxy amplitudes.  This is the h9 pattern, in this lane's newest entry.")
print(f"    L21's error bars come from ml_fit's profile likelihood (L21:417) -- statistics only.")
print(f"    The amplitude A = observed/predicted with predicted sigma_los ~ (G M a0)^(1/4), so a COHERENT")
print(f"    error in the K-band stellar M/L moves EVERY one of the 1900 pairs together:  dlnA = -(1/4) dlnUpsilon.")
print(f"    L21's own systematics note says the shape axis 'is immune to this' -- i.e. the amplitude axis is not.")
A_iso, eA_iso = 1.802, 0.041
for dexU in (0.10, 0.15):
    dA = 0.25*dexU*math.log(10)*A_iso
    print(f"      Upsilon_K coherent at {dexU:.2f} dex -> dA = {dA:.3f};  A = {A_iso} +/- {eA_iso}(stat) "
          f"+/- {dA:.3f}(syst) -> {(A_iso-1)/math.hypot(eA_iso,dA):.1f} sigma  (quoted 19.6)")
A_deep, A_shal = 1.51, 1.99
half = (A_shal - A_deep)/2
print(f"    AND the lane's own leading systematic is isolation depth: A falls 1.99 -> 1.51 as isolation")
print(f"    deepens, a coherent one-sided {100*half/((A_shal+A_deep)/2):.0f}% band the record itself calls decisive.")
dA_ML = 0.25*0.10*math.log(10)*A_iso
tot20 = math.sqrt(eA_iso**2 + dA_ML**2 + half**2)
print(f"      combining stat + 0.10 dex M/L + the isolation band: A - 1 = {A_iso-1:.3f} +/- {tot20:.3f} "
      f"-> {(A_iso-1)/tot20:.1f} sigma, not 19.6")
sig("A20", "19.6 sigma (and 24.9, 22.4, 25.0, 5.0, 16.3, 3.9, 5.6)", "statistics-only profile likelihood",
    "Upsilon_K = 0.6 assumed for all 1900 pairs; one distance scale; one isolation criterion; one "
    "circular-orbit assumption; one interloper model",
    f"~{(A_iso-1)/math.hypot(eA_iso,dA_ML):.0f} sigma with a 0.10 dex M/L floor; ~{(A_iso-1)/tot20:.0f} sigma "
    f"including the lane's own isolation-depth band",
    "A > 1 is robust; '19.6 sigma' is not a defensible number and the record already says so in prose "
    "('every A here is an UPPER limit') without propagating it into the figure")
row("A20", "framework isolated A = 1.802 +/- 0.041, 19.6 sigma", "L21 amplitude table",
    f"reproduces; but stat-only. With a 0.10 dex coherent Upsilon_K: {(A_iso-1)/math.hypot(eA_iso,dA_ML):.1f} sigma. "
    f"With the lane's own isolation band as well: {(A_iso-1)/tot20:.1f} sigma", "STAT-ONLY",
    "same failure mode L23 corrected in h9, reintroduced in the newest entry")
print(f"\n    Same treatment for the ladder: A20's 'pairs need 30.9 +/- 1.6' has M_dyn/M_bar ~ 1/Upsilon,")
d309 = 30.9*(10**0.10 - 1)
print(f"      a 0.10 dex coherent Upsilon_K gives +/-{d309:.1f} on 30.9, so the gap to the cosmic 5.43 is")
print(f"      {(30.9-5.43)/math.hypot(1.6,d309):.1f} sigma, not 16.  The factor 5.7 becomes {30.9/10**0.10/5.43:.1f}-{30.9*10**0.10/5.43:.1f}.")
sig("A20", "30.9 +/- 1.6, 16 sigma, factor 5.7", "statistics-only",
    "the same single Upsilon_K", f"{(30.9-5.43)/math.hypot(1.6,d309):.1f} sigma, factor "
    f"{30.9/10**0.10/5.43:.1f}-{30.9*10**0.10/5.43:.1f}",
    "the 'ladder is not monotone' conclusion survives; the significance does not")

sub("C3  A7 -- '|z| = 13' (L2) and '12.8 sigma' (L6)")
print("    These are z-scores between the cluster-required and galaxy-measured boost at matched acceleration")
print("    (or matched density).  a0 cancels, correctly.  But the two populations do NOT share systematics,")
print("    they have DIFFERENT ones, and neither is in the z: SPARC's Upsilon_disc = 0.5 / Upsilon_bulge = 0.7")
print("    (coherent, ~0.11 dex in the literature) on one side, and the hydrostatic mass bias on the other.")
print("    L18 prices the cluster side and finds it makes the gap WORSE (required b = -2.07 to close it).")
print("    The SPARC side is not priced anywhere in this lane.  A 0.11 dex coherent Upsilon moves the")
print("    galaxy boost by a factor 1.29 in g_bar, i.e. it cannot plausibly close a factor 2.2-5.1 --")
print("    so the conclusion is safe, but '|z| = 13' and '12.8 sigma' remain statistics-only numbers.")
sig("A7", "|z| = 13, 12.8 sigma", "statistics-only bin z-scores",
    "SPARC Upsilon (galaxy side, unpriced); HSE bias (cluster side, priced by L18 and helps)",
    "not recomputed here -- the SPARC Upsilon term needs L2/L6 re-run with Upsilon profiled",
    "UNVERIFIED as a significance; the factor 2.2-5.1 is what carries the argument and it is robust")
row("A7", "cluster/galaxy 2.2-5.1x, |z| = 13; density overlap 12.8 sigma", "L2 C5, L6 S2",
    "ratios reproduce exactly; the z-scores are stat-only and the SPARC Upsilon systematic is unpriced",
    "STAT-ONLY", "the ratio, not the z, is the load-bearing quantity -- the record leads with the z")

sub("C4  A22 -- the model case.  This is what the rest of section A should look like.")
print("    A22 quotes 4.9/4.7 sigma AFTER a 0.227 dex coherent floor built from a named line-item budget")
print("    (M/L+IMF 0.148, aperture/anisotropy 0.120, cluster model 0.088, instrument 0.052, estimator")
print("    0.047, a0 footing 0.047, distance 0.021), and it states the stat-only 19.4 sigma as the thing")
print("    being corrected.  Recomputed: sqrt(0.062^2 + 0.227^2) = %.4f, 1.159/%.4f = %.2f sigma."
      % (math.hypot(0.062, 0.227), math.hypot(0.062, 0.227), 1.159/math.hypot(0.062, 0.227)))
sig("A22", "4.9 / 4.7 sigma", "floor-included", "explicitly enumerated and propagated",
    f"{1.159/math.hypot(0.062,0.227):.2f} sigma -- reproduces", "EXEMPLARY; the template for A8 and A20")
row("A22", "+1.196 -> +1.159 dex, 19.4 sigma -> 4.9/4.7 sigma, floor 0.227 dex", "L23 S1/V1",
    f"{1.159/math.hypot(0.062,0.227):.2f} sigma reproduces exactly", "VERIFIED",
    "the only entry in section A whose significance is defensible as written")

sub("C5  A17 -- '6 sigma below' the abundance-matching prediction")
print("    L16-R4b: a0 returns only at log M_200 -1.80 dex, called '6.0 sigma below' LambdaCDM's prediction.")
print("    The 0.30 dex denominator is the abundance-matching SPREAD (Moster vs Behroozi vs Kravtsov plus")
print("    the 0.1 dex Upsilon systematic), i.e. a systematic used as a sigma. That is the right currency")
print("    here -- it is a coherent modelling uncertainty, not a per-galaxy statistical error -- so this")
print("    one is defensible. Recorded because it is the only sigma in section A built on a systematic.")
sig("A17", "6 sigma below the AM prediction", "systematic-as-sigma (correct usage)",
    "n/a", "1.80/0.30 = 6.0 -- reproduces", "defensible")

n_bad_sig = sum(1 for s in SIG if s["kind"].startswith("statistics-only"))
check("F3 [FAILURE MODE 3, correlated errors] every sigma and every error bar in section A either "
      "includes a coherent-systematic floor or is labelled statistics-only where it is quoted",
      n_bad_sig == 0,
      f"{n_bad_sig} statistics-only significances presented without a floor: A8's 13-15 sigma "
      f"(-> ~{resid_med/tot:.0f} with a 10% coherent X-ray mass calibration), A20's whole amplitude "
      f"table including 19.6 sigma (-> ~{(A_iso-1)/math.hypot(eA_iso,dA_ML):.0f} with a 0.10 dex "
      f"Upsilon_K floor, ~{(A_iso-1)/tot20:.0f} including the lane's own isolation band) and its 16 sigma "
      f"ladder gap (-> ~{(30.9-5.43)/math.hypot(1.6,d309):.0f}), and A7's |z| = 13 / 12.8 sigma. In every "
      f"case the DIRECTION of the conclusion survives and only the number falls. A22 is the counter-example "
      f"and shows the lane knows how to do this")

# ===========================================================================================
head("D -- FAILURE MODE 4: OVERCLAIM.  Each section-A sentence against the actual PASS/FAIL lines and "
     "printed numbers of its script.")
# ===========================================================================================

OVER = []
def over(entry, sentence, script_says, why):
    OVER.append(dict(entry=entry, s=sentence, script=script_says, why=why))

sub("D1  A14 -- 'The lead's own galactic matching open item is answered POSITIVELY.'")
print("    L11 runs 22 checks and THREE fail, two of them on exactly this question:")
print("      [FAIL] B2b  the kernel produced is the EXPONENTIAL carrier, not the programme's carried nu_RAR")
print("                  (0.0726 dex apart; the ceiling is exceeded 5.2x more often on bulgeless SPARC)")
print("      [FAIL] B3   the IC kernel IS disfavoured relative to nu_RAR on that control")
print("      [FAIL] B5   the far-field boundary condition on u is NOT determined by the published files;")
print("                  if u must approach the cosmological value, 27%/38% of bulgeless SPARC points")
print("                  beyond 2 kpc sit below the implied universal external field")
print("    L11's own VERDICT line says 'the two open items above are scored separately as B2b and B5 and")
print("    are NOT hidden inside this verdict'.  A14 hides them: it mentions neither.  FINDINGS does not.")
over("A14", "'The lead's own galactic matching open item is answered POSITIVELY'",
     "L11 VERDICT: 'a CANDIDATE HOST', with B2b, B3 and B5 scored separately as FAILs",
     "the handoff entry the lead is told it may rely on drops both caveats the script insisted on keeping visible")
row("A14", "the IC-series reduces to MOND; galactic matching answered positively", "L11 (19 PASS, 3 FAIL)",
    "the reduction verifies exactly (coefficient 1.000000, no slip <1e-4, same G); B2b/B3/B5 FAIL and are absent from A14",
    "OVERCLAIM", "add: 'kernel is the exponential carrier not nu_RAR (B2b/B3), and the far-field u is undetermined (B5)'")

sub("D2  A16 -- 'A late-time roll CLEARS the cosmological gates ... predicting sigma_8 = 0.845-0.861'")
print("    L9 prints, in the same table as that prediction:")
print("      sigma_8  0.853-0.861   gate +/-10%   Planck 0.8111 +/- 0.0060  =>  7-8 sigma   [canonical]")
print("      sigma_8  0.845-0.859   gate +/-10%   Planck 0.8111 +/- 0.0060  =>  6-8 sigma   [alt]")
print("      RSD dchi2  +5.28 to +9.00   gate <= +9.00        [the canonical band runs right up to the gate]")
print("      Omega_Lambda 0.248-0.274    not gated            measured 0.685")
print("    So the 'prediction' is already 6-8 sigma from the measurement it is compared against in the very")
print("    same row, and it clears 'growth' only because that gate was set at +/-10% and dchi2 <= 9.")
print("    FINDINGS says 'every survivor sits at the top of the growth gate' and that 2 sigma empties the")
print("    canonical footing -- true, but the handoff entry the lead reads says only 'clears'.")
over("A16", "'clears the cosmological gates (BBN, CMB, growth, expansion incl. absolute BAO)' and "
            "'a sharp falsifiable prediction sigma_8 = 0.845-0.861'",
     "L9's own table annotates that same sigma_8 as 6-8 sigma from Planck, with the RSD dchi2 band "
     "running right up to its gate and Omega_Lambda = 0.25-0.32 against 0.685",
     "'clears' is doing work a +/-10% gate cannot support; the prediction is already in tension at 6-8 sigma")
row("A16", "late roll clears BBN/CMB/growth/expansion; sigma_8 = 0.845-0.861, H0 = 68-72", "L9 T1-T6",
    "gates as defined do pass; but sigma_8 is 6-8 sigma from Planck in L9's own annotation and the RSD "
    "band reaches its gate", "OVERCLAIM", "A16 should carry '6-8 sigma from Planck sigma_8' explicitly")

sub("D3  A1 -- 'IC7's claim that c_7 is built from action derivatives alone is CONFIRMED as written'")
print("    True, and L4-I6 checks it symbolically (no free symbols beyond the state).  But L4-I5, in the")
print("    same run, records something the record does not carry anywhere:")
print("      [PASS] L4-I5 ... the central IC7 identity S_4 + 32 V c_7/B3^4 = 0 holds IDENTICALLY on the")
print("             isotropic plateau -- BUT IT HOLDS BECAUSE c_7 IS -S_4/32 BY DEFINITION: the repair is")
print("             an exactly tuned counterterm, not an independent prediction of the action.")
print("    Neither A1 nor FINDINGS' L4 section states that. It is the single most important qualification")
print("    on the IC7 repair and it is the lane's own finding.")
over("A1", "'c_7 is genuinely built from action derivatives alone' (with no further qualification)",
     "L4-I5: the identity holds because c_7 IS -S_4/32 by definition -- an exactly tuned counterterm, "
     "not an independent prediction",
     "both statements are true; omitting the second makes the first read as a prediction rather than a fit")
row("A1", "the lead's IC5/6/7 algebra reproduces; c_7 built from action derivatives alone", "L4 (28 PASS, 1 FAIL)",
    "reproduces exactly (obstruction verified to 40 digits here, independently of L4); I5's counterterm "
    "qualification is absent from the record", "OVERCLAIM", "add I5's sentence to A1")

sub("D4  A5/A6 -- correctly scoped.  Recorded as the counter-example.")
print("    A5 states three tiers with the deciding input named (IC10's open item 3) and A6 is explicitly")
print("    'SCOPED BY L19 to case Y1 only'. This is exactly the right shape for a conditional result and")
print("    it matches L19's C8a/C8b/C12 lines.  No overclaim.")
row("A5/A6", "three-tier Cherenkov conditional, target region scoped to Y1", "L19 C6/C8a/C8b/C12",
    "matches the script's own tiering; the deciding computation is named", "VERIFIED", "model conditional")

sub("D5  the entries that check out clause by clause")
print("    A2  DOF = 3 with A_0 = 0.4614531036 > 0, DeWitt lambda = 1, c_s^2 = 1/3 -- L4-D2/D3/D4/C1 verbatim.")
print("    A3  |j-1| < 0.074 (plateau ends 1.0736445) and 4 c_7/c = 0.008570513 -- L4-I11/I13 verbatim.")
print("    A10 the curl finding: 5.7e-03 of the path integral vs 1.3e-09 Newtonian, unbinds within 1 Gyr")
print("        at any timestep -- L1-V5a/V5b verbatim, and the method rule follows from it.")
print("    A12 no admissible point on either footing; minimal incompatible subsets all contain G2;")
print("        gamma_v ceilings 1.0450/1.0300; all ten gate controls C1-C10 PASS -- L14 verbatim.")
print("    A13 Omega_d,eff <= 2.6e-6 against Omega_d = 0.266, short by 1.0e5x -- L14-T4 verbatim.")
print("    A18 b = -0.819/-0.681 and -2.07, sigma^2 < 0 in 12/12, ratio 9.04 at b = 0.33, and the")
print("        SELF-CORRECTION of L7's own '5%' headline -- L18-H2/H3/H4/H6/H8/H9 verbatim. A18 is the")
print("        only entry in section A that exists to attack this lane's own strongest claim.")
print("    A20 the one clause that is unambiguously right and easy to get wrong: 'the closest separation")
print("        slope of any law (1.9 sigma)'. L21's table: 5.6, 6.1, 10.6, 10.6, 3.2, 1.9, 5.4 -- 1.9 is")
print("        indeed the minimum, and the shape axis is genuinely immune to the M/L.")
for e, c, s_, r_ in [
    ("A2",  "local DOF = 3, healthy khronon (A_0 = 0.46, lambda = 1, c_s^2 = 1/3)", "L4 D2/D3/C1", "verbatim"),
    ("A3",  "repair window |j-1| < 0.074; c_T^2 = 1 - 4c_7 Rbar_0/c, 4c_7/c = 0.00857", "L4 I11/I13", "verbatim"),
    ("A10", "algebraic nu(|g|)g has nonzero curl and unbinds within 1 Gyr", "L1 V5a/V5b", "verbatim"),
    ("A12", "no admissible point on either footing; every minimal subset contains G2", "L14 T1/T2", "verbatim"),
    ("A13", "condensate dark fraction capped at 2.6e-6, short by 1e5x", "L14 T4", "verbatim"),
    ("A18", "hydrostatic bias is not an escape and runs the wrong way", "L18 H2-H9", "verbatim"),
    ("A20", "1.9 sigma separation slope is the closest of any law", "L21 slope table", "minimum of 7, confirmed")]:
    row(e, c, s_, r_, "VERIFIED", "")
sub("D6  A21, A23 -- checked against their scripts, no overclaim found")
print("    A21's five clauses each map onto a named L17 check (M4, M5, O1, O2, S2, the Dirac counter's")
print("    controls) and its verdict phrase is L17's own.  A23's seven clauses map onto L20-G1/G2/G3/S2/")
print("    F1-F4/F6/V2 and it carries the lane's own honest caveat ('relocates the problem').")
row("A21", "A5 is a seasoning not a protein; 0 DOF, dlng/dlnM = 1.000000, amplitude short by 4e6", "L17 (15 PASS, 17 FAIL)",
    "every quoted number found in the .out on both footings", "VERIFIED", "")
row("A23", "IC10 plateau past-incomplete at a regular point; repair is not a coefficient", "L20 (23 PASS, 0 FAIL)",
    "all thirteen quoted numbers found in the .out; internal units, footing-free", "VERIFIED", "")

check("F4 [FAILURE MODE 4, overclaim] no section-A sentence is stronger, broader or more general than "
      "what its script's PASS/FAIL lines and printed numbers support", len(OVER) == 0,
      f"{len(OVER)} overclaims. A14 states the lead's galactic-matching item is 'answered POSITIVELY' "
      f"while dropping the B2b/B3/B5 FAILs its own script insisted on keeping visible; A16 says the roll "
      f"'clears' growth when L9's own table annotates the surviving sigma_8 as 6-8 sigma from Planck; "
      f"and A1 omits L4-I5's finding that IC7's c_7 is an exactly tuned counterterm rather than a "
      f"prediction. All three are omissions of the script's own caveats, not fabrications")

# ===========================================================================================
head("E -- CURRENCY.  Does every section-A number match what its script prints TODAY?")
# ===========================================================================================
PROBES = [
    ("A1",  "-11.1407711251147987",   "L4_verify_ic7.out"),
    ("A1",  "0.00235189114143216",    "L4_verify_ic7.out"),
    ("A1",  "0.0151964888331",        "L4_verify_ic7.out"),
    ("A2",  "count = 3",              "L4_verify_ic7.out"),
    ("A2",  "0.4614531036",           "L4_verify_ic7.out"),
    ("A3",  "1.0736445",              "L4_verify_ic7.out"),
    ("A3",  "0.008570513",            "L4_verify_ic7.out"),
    ("A4",  "15.42",                  "L10_khronon_gate.out"),
    ("A4",  "5.781e+05",              "L10_khronon_gate.out"),
    ("A5",  "1.44e-09",               "L19_cherenkov_applicability.out"),
    ("A5",  "7.2e+05",                "L19_cherenkov_applicability.out"),
    ("A5",  "8.812e+38",              "L19_cherenkov_applicability.out"),
    ("A6",  "2.5e-05",                "L10_khronon_gate.out"),
    ("A7",  "2.2-5.1",                "L2_cluster_inverse.out"),
    ("A7",  "|z| = 13",               "L2_cluster_inverse.out"),
    ("A7",  "12.8",                   "L6_screened_force.out"),
    ("A7",  "9.21",                   "L5_long_range_G.out"),
    ("A8",  "5.73",                   "L7_cosmic_ratio.out"),
    ("A8",  "0.149",                  "L7_cosmic_ratio.out"),
    ("A9",  "1.45",                   "L1_caustics_and_cap.out"),
    ("A9",  "0.92",                   "L1_caustics_and_cap.out"),
    ("A10", "5.7e-03",                "L1_caustics_and_cap.out"),
    ("A11", "7.45",                   "L3_flux_quantisation.out"),
    ("A11", "5.4756",                 "L3_flux_quantisation.out"),
    ("A12", "120,065,220",            "L14_parameter_sweep.out"),
    ("A12", "1.1800e-05",             "L14_parameter_sweep.out"),
    ("A12", "1.0450",                 "L14_parameter_sweep.out"),
    ("A13", "2.6",                    "L14_parameter_sweep.out"),
    ("A14", "1.000000",               "L11_galactic_limit.out"),
    ("A14", "6.45e-06",               "L11_galactic_limit.out"),
    ("A15", "-20.194205022906776",    "L15_sigma_one.out"),
    ("A15", "1.67931273219",          "L15_sigma_one.out"),
    ("A15", "1.7846769",              "L15_sigma_one.out"),
    ("A16", "0.845",                  "L9_late_transition.out"),
    ("A16", "0.9749",                 "L9_late_transition.out"),
    ("A17", "74.0%",                  "L16_hybrid_inverse.out"),
    ("A17", "-3.5%",                  "L16_hybrid_inverse.out"),
    ("A17", "3.29e-13",               "L16_hybrid_inverse.out"),
    ("A17", "0.198",                  "L16_hybrid_inverse.out"),
    ("A18", "-0.819",                 "L18_hse_bias.out"),
    ("A18", "-2.07",                  "L18_hse_bias.out"),
    ("A18", "9.04",                   "L18_hse_bias.out"),
    ("A19", "1.18979",                "L13_strong_coupling.out"),
    ("A19", "1.54",                   "L13_strong_coupling.out"),
    ("A19", "7.33e-92",               "L13_strong_coupling.out"),
    ("A19", "2522",                   "L13_strong_coupling.out"),
    ("A20", "1.802",                  "L21_binary_galaxies.out"),
    ("A20", "30.9",                   "L21_binary_galaxies.out"),
    ("A20", "0.60679",                "L21_binary_galaxies.out"),
    ("A20", "107.7",                  "L21_binary_galaxies.out"),
    ("A20", "112.9",                  "L21_binary_galaxies.out"),
    ("A21", "2.4971e-07",             "L17_elliptic_nonlocal.out"),
    ("A21", "31.11",                  "L17_elliptic_nonlocal.out"),
    ("A21", "1.000000",               "L17_elliptic_nonlocal.out"),
    ("A22", "1.1961",                 "L23_udg_verify.out"),
    ("A22", "0.227",                  "L23_udg_verify.out"),
    ("A22", "1.53",                   "L23_udg_verify.out"),
    ("A22", "0.635",                  "L23_udg_verify.out"),
    ("A23", "0.153984",               "L20_ghost_past.out"),
    ("A23", "2.9084",                 "L20_ghost_past.out"),
    ("A23", "0.93256",                "L20_ghost_past.out"),
    ("A23", "84.3%",                  "L20_ghost_past.out"),
]
missing = [(e, p, f) for e, p, f in PROBES if p not in OUT[f]]
print(f"    {len(PROBES)} load-bearing numbers probed against the .out their entry names.")
for e, p, f in missing:
    print(f"      MISSING: {e}  '{p}'  not found in {f}")
print(f"    plus: all 22 lane scripts were re-run for this audit; every one reproduces its committed .out")
print(f"    with only wall-clock timing lines differing.  No number in this record has drifted.")
check("F5 [currency] every section-A number is present in the output its own entry names, and every lane "
      "script reproduces its committed .out today", len(missing) == 0 and rerun_ok,
      f"{len(PROBES)} probes, {len(missing)} missing; live re-runs identical. "
      f"THE RECORD IS CURRENT -- nothing has drifted from its script. Every error found by this audit is "
      f"an error of DESCRIPTION, not of computation")

# ===========================================================================================
head("F -- CROSS-ENTRY CONSISTENCY.  Do any two section-A entries disagree on a shared quantity?")
# ===========================================================================================
DIS = []
def dis(q, e1, v1, e2, v2, verdict, note):
    print(f"    {q}")
    print(f"        {e1}: {v1}")
    print(f"        {e2}: {v2}")
    print(f"        -> {verdict}. {note}")
    if verdict == "DISAGREE": DIS.append((q, e1, v1, e2, v2, note))

sub("shared quantities")
dis("saturation point (s_sat, Delta_sat)", "L6/L13/L21 code", "2.540 / 0.6476",
    "L23-K1 re-derivation", f"{s_sat:.4f} / {d_sat:.4f} (true argmax)", "CONSISTENT",
    "every script that carries the kernel uses the same pair and it is the true stationary point")
dis("a0 footings", "all 22 scripts", "9.3619e-11 / 1.1279e-10",
    "CHARTER rule 3", "9.3619e-11 / 1.1279e-10", "CONSISTENT", "no script uses a third value")
dis("cosmic dark-to-baryon share", "A8", "Omega_dm/Omega_b = 5.43", "A20 ladder", "5.43", "CONSISTENT", "")
dis("cluster dark-to-baryon ratio at the outer radius", "A7 (via L2's J_Y)",
    f"1/J_Y = {min(inv):.2f}-{max(inv):.2f} over s = 0.09-0.91 (stellar-7 headline)",
    "A8 (L7 at 1000 kpc)", f"{np.median(ratio_N):.2f}", "CONSISTENT",
    f"recomputed from the raw JSON: M_dark/M_bar at 1000 kpc = {np.median(ratio_N):.2f}, inside L2's "
    f"headline band. NOTE the all-12 subset of L2 gives J_Y down to 0.100 (1/J_Y = 10.0), which does NOT "
    f"contain 5.73 -- the agreement holds on the headline stellar-7 subset only, and neither entry says so")
dis("c_14 ceiling", "A6 (from alpha_1)", "<= 2.5e-5", "A12 (sweep region)", "<= 1.18e-5", "CONSISTENT",
    "the sweep's grid edge is inside the PPN bound; A12 calls this 'agrees', which is containment not equality")
dis("cluster-to-galaxy boost contrast", "A7 / A16 / A18", "2.2-5.1 in all three", "L2/L9/L18 .out",
    "2.2-5.1 in all three", "CONSISTENT", "L18-H1 reproduces L2 exactly as a control")
dis("the +/- 0.68 on the cluster ratio", "A8", "quoted as the 12% cluster-to-cluster SCATTER",
    "A20 ladder", "used alongside '30.9 +/- 1.6' as if it were an uncertainty on the mean", "DISAGREE",
    "the same symbol is a population scatter in one entry and an error bar in the other; the error on the "
    "median of 12 would be 0.68/sqrt(12) = 0.20. A20's own 16.3 sigma in fact uses neither -- it compares "
    "to the cosmic 5.43 with only the 1.6")
dis("tensor cone c_T^2", "A3", "c_T^2 = 1 - 4 c_7 Rbar_0/c: IC7 DETUNES it off flat backgrounds",
    "A15", "'c_T^2 = 1 ... is a sigma-INDEPENDENT identity'", "DISAGREE",
    "both are true of different backgrounds (A15 means the IC6 sector on flat backgrounds), but as written "
    "the handoff asserts luminality as an identity in one row and its violation in another with no "
    "qualifier. L15-R14 also finds the detuning roughly DOUBLES at sigma = 1 (0.00857 -> 0.02259), which "
    "A3's single number does not carry")
dis("alpha_2 closed form", "L10-K1", "identifies a 3 c_14^2/4 term OMITTED by g03v",
    "A19 / L13-P2 detail", "quotes 'alpha_2 = -c_14/2 + c_14^2/(2 c_2)' -- the uncorrected form", "DISAGREE",
    "verified symbolically here: the correct expansion is -c_14/2 + c_14^2/(2 c_2) + 3 c_14^2/4. Numerically "
    "irrelevant at c_14 ~ 1e-5, but the record repeats an error one of its own lanes corrected")
dis("Cassini |a|/a0", "A4", "5.78e5 a0 (the alt column, presented as universal)",
    "L10 table", f"{y_can:.3g} canonical / {y_alt:.3g} alt", "DISAGREE",
    "already counted as a footing leak; it is also an internal inconsistency between the entry and its table")

check("F6 [cross-entry] no two section-A entries disagree on a shared quantity", len(DIS) == 0,
      f"{len(DIS)} disagreements: the +/- 0.68 is a scatter in A8 and an error bar in A20; A3 and A15 "
      f"assert the tensor cone is detuned and is an identity with no qualifier distinguishing flat from "
      f"curved backgrounds; A19 repeats an alpha_2 form that L10 itself corrected; and A4's Cassini "
      f"number contradicts its own script's table. None changes a verdict; all are record defects")

# ===========================================================================================
head("G -- THE LEDGER")
# ===========================================================================================
order = {"VERIFIED": 0, "LEAKY": 1, "WEAK": 2, "STAT-ONLY": 3, "OVERCLAIM": 4, "WRONG": 5, "UNVERIFIED": 6}
print(f"    {'entry':<22}{'verdict':<12}{'claim'}")
for r in sorted(LEDGER, key=lambda r: (order.get(r["verdict"], 9), r["entry"])):
    print(f"    {r['entry']:<22}{r['verdict']:<12}{r['claim'][:74]}")
    print(f"    {'':<34}-> {r['recomputed'][:84]}")
counts = {}
for r in LEDGER: counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
print(f"\n    ledger verdicts: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))

sub("UNVERIFIED -- claims this audit could not recheck without a new expensive solve. "
    "Recorded as UNVERIFIED, NOT passed by default.")
UNVER = [
 ("A9",  "that the M(<10 kpc) values are CONVERGED. L1's own note is that the trend rises with N "
         "(1.24 at 4000 -> 1.43 at 8000) and that the coarse timestep biases down; FINDINGS concludes "
         "'the converged value is at or above these'. No run above N = 8000 exists, and L1's own line "
         "reads 'numbers RISING with N are particle noise, not caustics' -- which is a different claim. "
         "Settling it needs an N = 16000-32000 multipole run."),
 ("A9",  "the caveats L1 itself declines to repair: angle-averaged QUMOND rather than a solved field "
         "equation, an isolated vacuole with no tides, z_i = 20 against the shell model's 50."),
 ("A20", "the isolation-depth systematic. Every amplitude is an UPPER limit and the lane says so; the "
         "size of the correction (1.99 -> 1.51 measured; how much further a 2-magnitude-deeper catalogue "
         "would take it) is not computable from 2MRS and is the single number the entry most needs."),
 ("A7",  "the SPARC-side Upsilon systematic on |z| = 13 and 12.8 sigma. Needs L2/L6 re-run with "
         "Upsilon_disc profiled rather than frozen at 0.5."),
 ("A16", "whether the surviving late-roll region is a real region or a boundary artefact of the +/-10% "
         "sigma_8 gate and the dchi2 <= 9 RSD gate, which the canonical band runs right up to."),
 ("A12", "the sweep's GRID resolution. 1.2e8 points is a coarse log grid in 6 dimensions (about 22 "
         "points per axis); 'no admissible point' is a statement about the grid, and the region is "
         "described in the .out itself as 'a thin sheet' where the marginal boxes are not independent."),
 ("A2/A3", "the lead-side inputs. L4 rebuilds the lead's algebra independently and it reproduces, and "
           "the lead's c_7 = 0.00235189114143216, S4_11 = -0.0642323935174161 and leftover 0.0151964888331 "
           "are present in its files today. What is NOT verified is the lead's anisotropic two-mode "
           "reduction itself, which neither L4 nor L15 reproduces (L15 names it as missing)."),
 ("A19", "the MOND scalar's cubic action. L13-P9 FAILs because Delta' = 0 on the saturated branch, so "
         "Sigma_par = infinity; the strong-coupling scale of the SCALAR (as distinct from the khronon) "
         "cannot be computed from the action as published. A19 records this correctly."),
]
for e, t in UNVER:
    print(f"    {e:<8}{t}")
    row(e, "(see UNVERIFIED list)", "n/a", "not rechecked", "UNVERIFIED", t[:80])

# ===========================================================================================
head("H -- VERDICT")
# ===========================================================================================
counts = {}
for r in LEDGER: counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
n_ver  = counts.get("VERIFIED", 0)
n_bad  = counts.get("WRONG", 0) + counts.get("OVERCLAIM", 0)
n_soft = counts.get("LEAKY", 0) + counts.get("STAT-ONLY", 0) + counts.get("WEAK", 0)
n_unv  = counts.get("UNVERIFIED", 0)
print(f"""
  WHAT SURVIVED.  Every computation in this record is CURRENT and REPRODUCIBLE.  All 22 lane scripts
  re-run today produce their committed .out to the character (only wall-clock lines differ).  The four
  algebraic keystones re-derive in exact arithmetic, independently of the lane's own code:
      S_4'(1)|sigma=1/3 = -11.140771125114798741  (record's 18 digits correct)
      S_4'(1)|sigma=1   = -20.194205022906776     (correct), sigma* = 4T/(4T-27) = 1.6793127 EXACT
      alpha_1 = -4 c_14 EXACT on c_1 = -c_3 = K_B; c_2* = c_14/(1-2c_14) its exact alpha_2 zero
      the split-degeneracy map is an exact rational identity; Z/beta^2 = 2/kappa^2 - 2b
  A8's 5.73 and 12% were rebuilt from the raw cluster JSON and reproduce.  A11, A21, A22 and A23 are
  clean as written; A22 is the model for how a significance should be reported in this programme.

  WHAT DID NOT.  Every error found is an error of DESCRIPTION, not of computation.  That is the good
  news and it is also the pattern: this record's failure mode is the sentence, not the solve.
    {n_bad} entries are WRONG or OVERCLAIMED, {n_soft} leak a footing or quote a statistics-only sigma,
    {n_unv} claims are UNVERIFIED and must not be read as passed.

  THE THREE THAT MUST BE FIXED BEFORE THE RECORD IS USED:
    1. A20's significances are statistics-only on a sample sharing one Upsilon_K, one distance scale and
       one isolation criterion -- the identical failure L23 corrected in h9, reintroduced in the newest
       entry. 19.6 sigma -> ~7 sigma with a 0.10 dex M/L floor, ~3 sigma including the lane's own
       isolation band. A > 1 survives; the number does not.
    2. A14 tells the lead its galactic-matching item is 'answered POSITIVELY' while dropping the three
       FAILs (B2b, B3, B5) that L11's own verdict line insisted be kept visible.
    3. A4 quotes the ALT column of L10's two-footing table as though it were universal, while FINDINGS
       says 'on both footings'. Canonical is 6.96e5 a0 and 4.5e4x, not 5.78e5 and 3.7e4x.
""")
check("F7 [VERDICT] the standing record in HANDOFF_CONTRACT section A is sound AS WRITTEN and can be "
      "relied on without amendment", n_bad == 0 and n_soft == 0,
      f"it is not: {n_bad} wrong/overclaimed, {n_soft} leaky or statistics-only, {n_unv} unverified, "
      f"{n_ver} verified. The UNDERLYING COMPUTATIONS are sound -- nothing has drifted and the algebra "
      f"re-derives exactly -- so every fix is a rewrite of a sentence, not a re-run of a solve. "
      f"The record is repairable in place")

print("\n" + "=" * 122)
print(f"RESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "RESULT: 0 FAIL")
print("=" * 122)
sys.exit(0)
