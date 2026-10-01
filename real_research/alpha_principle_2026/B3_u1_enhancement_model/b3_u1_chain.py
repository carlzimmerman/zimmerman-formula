#!/usr/bin/env python3
"""B3 -- link-by-link map of the Multiple Point Principle U(1) chain (1/alpha_Y at the Planck scale).  Pre-registered in B3_PREREGISTRATION.md (incl. Amendment 1).

Sources (all read in the primary text; see B3_SOURCE_LEDGER.md):
  [BN96] hep-ph/9607278 (U(1) paper: eqs (49),(122),(126)-(140), Tables 4-7)   [BT96] hep-ph/9607341 (thesis, same tables)   [BN93] hep-ph/9311321
  [CQ02] hep-lat/0210010 (modern compact-QED Wilson transition: beta_T and plaquette gap)

Run:    python3 b3_u1_chain.py          (exit 0 iff all declared internal checks pass; the link classification is REPORTED, not asserted)
MUTATE: python3 b3_u1_chain.py MUTATE   (the base enhancement factor 6 in the chain is replaced by the naive N_gen = 3; the declared reproduction check CK4 MUST
                                         flip to FAIL: exit 1 if the control fires, exit 3 if it does not)
"""
import sys
sys.dont_write_bytecode = True
import os
import math
import json
import itertools

HERE = os.path.dirname(os.path.abspath(__file__))
for sub in ("Y1_running_precision", "B_rg_asymptotic_safety", "N1_joint_couplings", "U3_invented_uv_boundary", "D_calibration_bar"):
    sys.path.insert(0, os.path.join(HERE, "..", sub))
import y1_lib as L

MUT = len(sys.argv) > 1 and sys.argv[1] == "MUTATE"
FAILED = []
MP = 1.22089e19
Y1_EXPECTED = 55.234
Y1_REL = 0.0023
SIG_MPP = 4.5          # stated absolute Planck-scale uncertainty, viewpoint a  [BN96 sec. 6]


def chk(tag, ok, detail=""):
    if not ok:
        FAILED.append(tag)
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


# =============================================================================================== transcribed primary-source data
BETA_C = {"Wilson": 1.0106, "Villain": 0.643}          # [BN96 (139),(140)] as used by the authors
LUCK = {"Wilson": (0.20, 0.24, 0.39), "Villain": (0.20, 0.33, 0.52)}   # alpha = a0 - a1 * x^p, x = dg/(beta_c + dg)   [BN96 (139),(140)]
A_W, DW0_PAPER, ETA_NORM, VOL = 0.252, 0.016, 0.377, 1.34            # [BN96 (131),(133),(137),(128)]
A_V, P_V = 0.16, 0.29                                               # Villain counterpart of (133)   [BN96 Table 6 caption]
# [BN96 Table 4]: (beta_crit, Delta<S>, xi) for Z2, Z3 and the printed Delta gamma_eff
T4 = {2: (0.44, 0.44, 0.04, 0.0473), 3: (0.67, 0.56, 0.04, 0.0393)}
# [BN96 Table 7]: (label, action, dg_corr, alpha_cont, 1/alpha_cont, enh(tau=.79), enh(tau=1), pred(.79), pred(1), starred7)
T7 = [
    ("Z2 only", "Wilson", 0.0600, 0.1220, 8.196, 6.677, 6.535, 54.7, 53.6, False),
    ("Z2+Z3", "Wilson", 0.1094, 0.1031, 9.697, 6.826, 6.653, 66.2, 64.5, False),
    ("(Z2+Z3)/2", "Wilson", 0.05615, 0.1239, 8.072, 6.662, 6.523, 53.8, 52.7, True),
    ("Z2/2+Z3", "Wilson", 0.08108, 0.1129, 8.854, 6.748, 6.591, 59.7, 58.4, True),
    ("Z2 only", "Villain", 0.04318, 0.1217, 8.219, 6.441, 6.348, 52.9, 52.2, False),
    ("Z2+Z3", "Villain", 0.08119, 0.09424, 10.61, 6.529, 6.418, 69.3, 68.1, False),
    ("(Z2+Z3)/2", "Villain", 0.04044, 0.1241, 8.055, 6.432, 6.341, 51.8, 51.1, True),
    ("Z2/2+Z3", "Villain", 0.05941, 0.1087, 9.204, 6.483, 6.382, 59.7, 58.7, True),
]
# [BN96 Table 6] (older, uncorrected Delta gamma): (label, action, dg, alpha, 1/alpha, enh79, enh1, pred79, pred1, starred6)
T6 = [
    ("Z2 only", "Wilson", 0.0473, 0.1286, 7.778, 6.625, 6.494, 51.5, 50.5, False),
    ("Z2+Z3", "Wilson", 0.0866, 0.1108, 9.021, 6.764, 6.604, 61.0, 59.6, False),
    ("(Z2+Z3)/2", "Wilson", 0.0433, 0.1309, 7.640, 6.607, 6.480, 50.5, 49.5, False),
    ("Z2/2+Z3", "Wilson", 0.0630, 0.1206, 8.292, 6.689, 6.543, 55.5, 54.3, True),
    ("Z2 only", "Villain", 0.0473, 0.118, 8.465, 6.452, 6.357, 54.6, 53.8, False),
    ("Z2+Z3", "Villain", 0.0866, 0.0911, 10.98, 6.539, 6.426, 71.8, 70.6, False),
    ("(Z2+Z3)/2", "Villain", 0.0433, 0.122, 8.226, 6.441, 6.348, 53.0, 52.2, True),
    ("Z2/2+Z3", "Villain", 0.0630, 0.106, 9.424, 6.491, 6.388, 61.2, 60.2, True),
]
MODERN = dict(beta_c=1.0111331, beta_c_sig=0.0000021, gap=0.026721, gap_sig=0.000059)   # [CQ02] eqs (3),(4)


# =============================================================================================== the chain, one link per function
def L1_beta_c(action, modern=False):
    """L1: lattice critical coupling of compact U(1).  Measured on the lattice (printed 1.0106; modern high-precision 1.0111331(21) [CQ02]; B2 measured 1.0113(10))."""
    if modern and action == "Wilson":
        return MODERN["beta_c"]
    return BETA_C[action]


def L2_alpha_cont(dg, action, beta_c=None):
    """L2: continuum (Coulomb-potential) coupling at beta_eff = beta_c + dg, by the Luck-Jersak fit alpha = a0 - a1 (dg/(beta_c + dg))^p  [BN96 (139),(140)].  A fit by others to Monte Carlo data."""
    a0, a1, p = LUCK[action]
    bc = L1_beta_c(action) if beta_c is None else beta_c
    return a0 - a1 * (dg / (bc + dg)) ** p


def L3_base_factor(ngen=3):
    """L3a: independent-monopole weakening factor = |diagonal|^2 / |nearest neighbour|^2 in the hexagonal (A_N) lattice = N + N(N-1)/2 = N(N+1)/2 [BN96 (126),(127)].  MUTATE: naive N_gen."""
    if MUT:
        return float(ngen)
    return ngen * (ngen + 1) / 2.0


def L3_delta_w(dg, action, modern=False):
    """L3b: jump of <cos theta> across the TP transition, from the cube-root law (Wilson, A = 0.252, plus the border-'1' correction (DW1/A)^3, [BN96 (131)-(133)]) or the Villain counterpart."""
    if action == "Wilson":
        dw1 = MODERN["gap"] if modern else DW0_PAPER
        return A_W * (dg + (dw1 / A_W) ** 3) ** (1.0 / 3.0)
    return A_V * dg ** P_V


def L3_enhancement(dg, action, tau=0.79, modern=False, base=None):
    """L3c: linear interpolation between the independent-monopole factor (6) and the 'volume approximation' (6 x 1.34) with weight eta/tau, eta = DW/0.377  [BN96 (134)-(138)]."""
    b = L3_base_factor() if base is None else base
    eta = L3_delta_w(dg, action, modern) / ETA_NORM
    return b + b * (VOL - 1.0) * eta / tau


def L5_dgamma_N(N, beta_crit, dS, xi, beta=None):
    """L5: contribution of Z_N to Delta gamma_eff [BN96 (122)]: (1/N^2) beta_crit dS [1 + xi (sinh 2b / beta_crit - 2 cosh 2b)], b = beta_crit."""
    b = beta_crit if beta is None else beta
    return beta_crit * dS / N ** 2 * (1.0 + xi * (math.sinh(2 * b) / beta_crit - 2 * math.cosh(2 * b)))


def L5_improved(dg0_parts, action, w2, w3, conf_cos=0.623, tau_unused=None, p2=None, p3=None, tol=1e-12):
    """L5 (reconstruction of the 'improved' gamma_eff_corr of Table 7, underspecified in the source): dg = w2 dg2 c^-3/4 + w3 dg3 c^-8/9 (Wilson), c^+1/4, c^+1/9 (Villain),
    c = <cos theta> in the Coulomb phase = conf_cos + DeltaW(dg) iterated to a fixed point [BN96 (144)-(147), Table 7 caption]."""
    e2, e3 = (-0.75, -8.0 / 9.0) if action == "Wilson" else (0.25, 1.0 / 9.0)
    dg = w2 * dg0_parts[0] + w3 * dg0_parts[1]
    for _ in range(200):
        c = conf_cos + L3_delta_w(dg, action)
        new = w2 * dg0_parts[0] * c ** e2 + w3 * dg0_parts[1] * c ** e3
        if abs(new - dg) < tol:
            break
        dg = new
    return dg


def chain(dg, action, enh=None, tau=0.79, beta_c=None, modern=False):
    """L7: 1/alpha_Y(M_P) = enhancement x 1/alpha_cont.  enh = None -> the model's own interpolation (L3a-c); otherwise an external value."""
    ac = L2_alpha_cont(dg, action, beta_c if beta_c is not None else L1_beta_c(action, modern))
    e = L3_enhancement(dg, action, tau, modern) if enh is None else enh
    return e / ac, e, 1.0 / ac


# =============================================================================================== main
print(f"B3: U(1) chain of the Multiple Point Principle, link by link   (MUTATE={MUT})")
tr = L.run_central(mu_max=1e21)
tY = tr.A(MP)[0]
sY = tY * Y1_REL
print(f"  Y1 target 1/alpha_Y(M_P) = {tY:.3f} +- {sY:.3f} at M_P = {MP:.5e} GeV")
chk("C1 Y1 target equals the pre-registered 55.234 to 0.01", abs(tY - Y1_EXPECTED) < 0.01)
WIDE = 2 * math.hypot(SIG_MPP, sY)
SHARP = 2 * sY
print(f"  pass windows (2 sigma): wide (stated MPP uncertainty 4.5) = +-{WIDE:.2f}; sharp (Y1 error only) = +-{SHARP:.3f}")

# ---- CK1: L3 base factor from lattice geometry (independent derivation)
print("\nCK1  L3 base factor: hexagonal identification lattice, enumerate Gram-matrix sign classes (independent algebra)")
classes = []
for s in itertools.product((1, -1), repeat=3):
    g = [[1, s[0] / 2, s[1] / 2], [s[0] / 2, 1, s[2] / 2], [s[1] / 2, s[2] / 2, 1]]
    # positive definite? (Sylvester)
    d1, d2 = g[0][0], g[0][0] * g[1][1] - g[0][1] ** 2
    d3 = (g[0][0] * (g[1][1] * g[2][2] - g[1][2] ** 2) - g[0][1] * (g[1][0] * g[2][2] - g[1][2] * g[2][0]) + g[0][2] * (g[1][0] * g[2][1] - g[1][1] * g[2][0]))
    pd = d1 > 1e-9 and d2 > 1e-9 and d3 > 1e-9
    if not pd:
        classes.append((s, False, None, None, None))
        continue
    norms = {}
    for n in itertools.product(range(-3, 4), repeat=3):
        if n == (0, 0, 0):
            continue
        norms[n] = sum(n[i] * g[i][j] * n[j] for i in range(3) for j in range(3))
    mn = min(norms.values())
    nnn = sum(1 for v in norms.values() if abs(v - mn) < 1e-9)
    diag = sum(g[i][j] for i in range(3) for j in range(3))
    s3 = (s[0] == s[1] == s[2])
    classes.append((s, True, nnn, diag / mn, s3))
for s, pd, nnn, ratio, s3 in classes:
    print(f"    signs (g12,g13,g23) = {tuple('+' if x > 0 else '-' for x in s)}: positive definite={pd}" + (f", nearest neighbours={nnn}, |diag|^2/|nn|^2={ratio:.3f}, S3-symmetric={s3}" if pd else ""))
adm = [c for c in classes if c[1] and c[2] == 12 and c[4]]
chk("CK1 the S3-symmetric, positive-definite, 12-nearest-neighbour class is unique and gives diagonal ratio exactly 6", len(adm) == 1 and abs(adm[0][3] - 6.0) < 1e-9, f"({[(c[0], c[3]) for c in adm]})")
others = sorted({round(c[3], 3) for c in classes if c[1] and c[2] == 12 and not c[4]})
print(f"    non-S3-symmetric admissible classes give other diagonal ratios {others}: S3 symmetry is what selects 6 (premise: the three U(1) factors are permutation-equivalent)")
print("    general N: " + ", ".join(f"N={n}: {n + n * (n - 1) / 2:.0f}" for n in (2, 3, 4, 5)) + " = N(N+1)/2;  cubic (no interaction terms) lattice: ratio N = 3")
chk("CK1b the chain function L3_base_factor() agrees with the lattice algebra (real run: 6; MUTATE: 3)", abs(L3_base_factor() - 6.0) < 1e-9)

# ---- CK2: Z2, Z3 critical couplings from exact self-duality
print("\nCK2  L5 inputs: Z2 and Z3 critical couplings by exact 4D self-duality, e^J = 1 + sqrt(N), J = beta (1 - cos(2 pi/N))")
dual = {}
for N in (2, 3):
    J = math.log(1 + math.sqrt(N))
    dual[N] = J / (1 - math.cos(2 * math.pi / N))
    print(f"    Z{N}: beta_c(duality) = {dual[N]:.4f}   printed {T4[N][0]}")
chk("CK2 duality reproduces the printed Z2 and Z3 critical couplings within 0.005", all(abs(dual[N] - T4[N][0]) < 0.005 for N in (2, 3)))

# ---- CK3: Delta gamma_eff
print("\nCK3  L5 Delta gamma_eff: eq (122) from the printed inputs, and the reconstructed 'improved' values")
parts = {}
for N in (2, 3):
    bcz, dS, xi, printed = T4[N]
    parts[N] = L5_dgamma_N(N, bcz, dS, xi)
    print(f"    Z{N}: computed {parts[N]:.5f}  printed {printed}   (without the xi term: {bcz * dS / N ** 2:.5f})")
chk("CK3a eq (122) reproduces Table 4 (0.0473, 0.0393) within 0.0003", all(abs(parts[N] - T4[N][3]) < 3e-4 for N in (2, 3)))
nxi = {N: T4[N][0] * T4[N][1] / N ** 2 for N in (2, 3)}
print(f"    xi = 0 changes the sum {parts[2] + parts[3]:.4f} -> {nxi[2] + nxi[3]:.4f} ({100 * (nxi[2] + nxi[3]) / (parts[2] + parts[3]) - 100:+.1f}%): the graphically estimated xi is a minor input")
combos = [("Z2 only", 1.0, 0.0), ("Z2+Z3", 1.0, 1.0), ("(Z2+Z3)/2", 0.5, 0.5), ("Z2/2+Z3", 0.5, 1.0)]
print("    reconstructed improved Delta gamma (iterated cos-power factor) vs printed Table 7; the Villain conf. <cos> is not given in the source (0.623 used):")
rec_ok = 0
rec_tot = 0
recon = {}
for lab, act, dgp, *_ in T7:
    w2, w3 = [(c[1], c[2]) for c in combos if c[0] == lab][0]
    val = L5_improved((parts[2], parts[3]), act, w2, w3)
    rel = val / dgp - 1
    recon[(lab, act)] = val
    rec_tot += 1
    rec_ok += abs(rel) < 0.03
    print(f"      {act:8s} {lab:10s} reconstructed {val:.5f}  printed {dgp:.5f}  ({100 * rel:+.1f}%)")
print(f"    {rec_ok} of {rec_tot} reconstructed within 3% (REPORTED; the procedure is underspecified in the source; not a hard check)")

# ---- CK7: plaquette jumps from the small Z_N Monte Carlo (src/zn.c, output b3_ck7_zn_jumps.out)
print("\nCK7  L5 inputs: plaquette jumps DeltaS_ZN from the small Z2/Z3 Monte Carlo (8^4, cold/hot metastable branches at the self-dual coupling)")
ck7_ok = None
mcjump = {}
p7 = os.path.join(HERE, "b3_ck7_zn_jumps.out")
if os.path.exists(p7):
    vals = {}
    for ln in open(p7):
        if ln.startswith("N="):
            f = dict(tok.split("=") for tok in ln.replace("<cos>", "cos").split() if "=" in tok)
            vals[(int(f["N"]), ln.split("start=")[1].split()[0])] = float(f["cos"])
    for N in (2, 3):
        mcjump[N] = vals[(N, "cold")] - vals[(N, "hot")]
        print(f"    Z{N}: cold {vals[(N, 'cold')]:.4f}  hot {vals[(N, 'hot')]:.4f}  jump {mcjump[N]:.4f}   printed {T4[N][1]}   ({100 * (mcjump[N] / T4[N][1] - 1):+.1f}%)")
    ck7_ok = all(abs(mcjump[N] / T4[N][1] - 1) <= 0.10 for N in (2, 3))
    chk("CK7 Monte Carlo plaquette jumps agree with the printed DeltaS (Z2 0.44, Z3 0.56) within 10%", ck7_ok)
    pz = {N: L5_dgamma_N(N, T4[N][0], mcjump[N], T4[N][2]) for N in (2, 3)}
    print(f"    Dgamma pieces with the Monte Carlo jumps: Z2 {pz[2]:.4f} (printed 0.0473), Z3 {pz[3]:.4f} (printed 0.0393); weights (1/2, 1/2), (1/2, 1):")
    for w2, w3 in ((0.5, 0.5), (0.5, 1.0)):
        dgx = w2 * pz[2] + w3 * pz[3]
        dgp = w2 * parts[2] + w3 * parts[3]
        print(f"      w=({w2},{w3}): Dgamma {dgx:.4f} vs {dgp:.4f};  1/alpha_Y {chain(dgx, 'Wilson')[0]:.2f} vs {chain(dgp, 'Wilson')[0]:.2f}")
else:
    print("    b3_ck7_zn_jumps.out missing: CK7 not run (sub-link stays UNDETERMINED)")

# ---- CK4: rows
print("\nCK4  L2/L3/L7 re-derivation: all eight Table 7 rows and eight Table 6 rows from the chain functions")
bad = []
maxd = [0, 0, 0]
for tab, rows in (("T7", T7), ("T6", T6)):
    for lab, act, dgp, alp, ialp, e79, e1, p79, p1, st in rows:
        ia = 1.0 / L2_alpha_cont(dgp, act)
        ee79 = L3_enhancement(dgp, act, 0.79)
        ee1 = L3_enhancement(dgp, act, 1.0)
        pp79, pp1 = ee79 * ia, ee1 * ia
        d = (abs(ia - ialp), max(abs(ee79 - e79), abs(ee1 - e1)), max(abs(pp79 - p79), abs(pp1 - p1)))
        maxd = [max(a, b) for a, b in zip(maxd, d)]
        if d[0] > 0.02 or d[1] > 0.006 or d[2] > 0.25:
            bad.append((tab, act, lab, tuple(round(x, 3) for x in d)))
chk("CK4 every printed row reproduced: 1/alpha_cont within 0.02, enhancement within 0.006, prediction within 0.25", not bad, f"(max deviations {maxd[0]:.3f}, {maxd[1]:.4f}, {maxd[2]:.3f}; bad rows: {bad})")
mean7 = sum(r[7] for r in T7 if r[9]) / 4
mean6 = sum(r[7] for r in T6 if r[9]) / 3
chk("CK4b mean of the four Table 7 starred rows = 56.25 (the abstract's 56)", abs(mean7 - 56.25) < 1e-9, f"({mean7:.3f})")
print(f"    viewpoint-a centre under the Table 6 star set (Wilson 1/2 Z2+Z3 and both Villain 1/2 rows): {mean6:.2f}; under the Table 7 star set: {mean7:.2f}; Y1 {tY:.2f}  -> selection of star set moves the centre by {mean7 - mean6:+.2f}")
print("    star sets differ between Table 6 and Table 7 for the Wilson (Z2+Z3)/2 row; the printed text does not say when each star was assigned")

# ---- the pieces of the chain at the starred row, for the record
dg0 = [r for r in T7 if r[0] == "(Z2+Z3)/2" and r[1] == "Wilson"][0][2]
ia0, e0 = 1 / L2_alpha_cont(dg0, "Wilson"), L3_enhancement(dg0, "Wilson", 0.79)
print(f"\nChain at the Table 7 Wilson (Z2+Z3)/2 row: Dgamma = {dg0}, 1/alpha_cont = {ia0:.3f}, enhancement = {e0:.3f}, 1/alpha_Y = {ia0 * e0:.2f}  (Y1 {tY:.3f})")
print(f"  without any discrete-subgroup correction (Dgamma = 0): 1/alpha_cont = {1 / L2_alpha_cont(0.0, 'Wilson'):.3f} = 1/{LUCK['Wilson'][0]};  x6 = {6 / L2_alpha_cont(0.0, 'Wilson'):.1f} (the table's 'independent monopole approx. 30')")
chk("CK4c Dgamma = 0 with enhancement 6 gives the printed 'independent monopole approx.' 30 (Table 8) within 0.5", abs(6 / L2_alpha_cont(0.0, "Wilson") - 30.0) < 0.5 or MUT)

# ---- CK5: stale inputs
print("\nCK5  stale inputs replaced by modern lattice values [CQ02]: beta_c 1.0106 -> 1.0111331, plaquette gap at gamma=0 0.016 -> 0.026721 (reported shifts, no pass/fail)")
for lab, act, dgp, *_r in T7:
    if act != "Wilson":
        continue
    a = chain(dgp, "Wilson")[0]
    b = chain(dgp, "Wilson", modern=True, beta_c=MODERN["beta_c"])[0]
    c = chain(dgp, "Wilson", modern=True)[0]
    print(f"    Wilson {lab:10s}: paper inputs {chain(dgp, 'Wilson', tau=0.79)[0]:.3f};  modern beta_c only {chain(dgp, 'Wilson', beta_c=MODERN['beta_c'])[0]:.3f};  modern gap only {chain(dgp, 'Wilson', modern=True, beta_c=1.0106)[0]:.3f};  both {b:.3f}")
print("    effect of the stale inputs is below 0.1 in 1/alpha_Y: not a driver.")

# ---- CK6: normalisation alternatives
print("\nCK6  L4 normalisation alternatives (the lattice unit charge identified with a different particle's charge), applied to the starred centre 56.25")
norms = [("positron unit y/2=1 (used; Q_our = Q_max/6, q=1)", 1.0), ("q=2 (Q_our = Q_max/12: 'wasting' fewer monopoles)", 4.0), ("q=3", 9.0),
         ("left-handed quark doublet as the unit (y/2=1/6)", 36.0), ("coupling to Y instead of Y/2 (g'/2)", 4.0), ("coupling to Y/4", 16.0), ("unit = 1/Z6 smaller charge, i.e. no Z6 quotient", 1.0 / 36.0)]
for name, f in norms:
    v = 56.25 * f
    z = (v - tY) / math.hypot(SIG_MPP, sY)
    print(f"    {name:55s} 1/alpha_Y = {v:9.2f}   z = {z:+8.2f}   {'within wide window' if abs(z) <= 2 else 'excluded'}")
print("    (the SU(5)-normalised coupling 5/3 g'^2 is the same physics with a 3/5 factor on both sides; not an alternative)")

# ---- Sensitivity scan
print("\nSENSITIVITY SCAN (pre-registered grid)")
ENH = [3.0, 4.0, 6.0, 6.5, 6.662, 8.04]
print("  (a) 1/alpha_Y at each printed Delta gamma (Table 7 values) for external enhancement factors; W = inside wide window, S = inside sharp window")
print("      action   variant       Dgamma | own interpolation | " + " ".join(f"{e:>9.3f}" for e in ENH))
spread_rows = []
for lab, act, dgp, *_r in T7:
    own = chain(dgp, act, tau=0.79)[0]
    cells = []
    for e in ENH:
        v = chain(dgp, act, enh=e)[0]
        spread_rows.append(v)
        flag = "S" if abs(v - tY) <= SHARP else ("W" if abs(v - tY) <= WIDE else "-")
        cells.append(f"{v:8.2f}{flag}")
    ownflag = "S" if abs(own - tY) <= SHARP else ("W" if abs(own - tY) <= WIDE else "-")
    print(f"      {act:8s} {lab:10s} {dgp:7.4f} | {own:9.2f}{ownflag}        | " + " ".join(cells))

print("  (b) Wilson, beta_c = 1.0106: required Delta gamma_eff to hit Y1 for each external enhancement (sharp = exact; wide = edge of +-9.0 window)")


def solve_dg(enh, target, action="Wilson", bc=None):
    lo, hi = 1e-9, 0.9
    f = lambda d: enh / L2_alpha_cont(d, action, bc) - target
    if f(lo) > 0 or f(hi) < 0:
        return float("nan")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


for e in ENH:
    print(f"      enhancement {e:6.3f}: Dgamma_eff(sharp) = {solve_dg(e, tY):.4f};  wide window Dgamma in [{solve_dg(e, tY - WIDE):.4f}, {solve_dg(e, tY + WIDE):.4f}]")
req_own = None
lo, hi = 1e-6, 0.5
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if chain(mid, "Wilson", tau=0.79)[0] < tY:
        lo = mid
    else:
        hi = mid
req_own = 0.5 * (lo + hi)
print(f"      with the model's own interpolation (tau=0.79): Dgamma_eff(sharp) = {req_own:.4f}; the starred printed values are 0.05615 and 0.08108, the mid value (0.0686) of the two is {chain(0.5 * (0.05615 + 0.08108), 'Wilson')[0]:.2f}")
print(f"      sensitivity d(1/alpha_Y)/d(Dgamma) at the own-interpolation solution: {(chain(req_own + 0.005, 'Wilson')[0] - chain(req_own - 0.005, 'Wilson')[0]) / 0.01:.0f} per unit; per 0.01: {(chain(req_own + 0.005, 'Wilson')[0] - chain(req_own - 0.005, 'Wilson')[0]):.2f}")

print("  (c) pass volume on the declared grids (Wilson, beta_c = 1.0106, external enhancement)")
dgs_a = [0.04 + 0.005 * i for i in range(15)]           # 0.04 .. 0.11
enh_a = [6.0, 6.5, 6.662, 8.04]
cells = [(d, e) for d in dgs_a for e in enh_a]
nw = sum(abs(chain(d, "Wilson", enh=e)[0] - tY) <= WIDE for d, e in cells)
ns = sum(abs(chain(d, "Wilson", enh=e)[0] - tY) <= SHARP for d, e in cells)
print(f"      grid A (Dgamma 0.04-0.11, enhancement 6/6.5/6.662/8.04; the range the papers print): {nw} of {len(cells)} cells in the wide window ({100 * nw / len(cells):.0f}%), {ns} in the sharp window ({100 * ns / len(cells):.0f}%)")
dgs_b = [0.005 * i for i in range(25)]                   # 0 .. 0.12
cells_b = [(d, e) for d in dgs_b for e in ENH]
nwb = sum(abs(chain(d, "Wilson", enh=e)[0] - tY) <= WIDE for d, e in cells_b)
print(f"      grid B (Dgamma 0-0.12, enhancement 3/4/6/6.5/6.662/8.04): {nwb} of {len(cells_b)} cells in the wide window ({100 * nwb / len(cells_b):.0f}%)")
vals_b = [chain(d, 'Wilson', enh=e)[0] for d, e in cells_b]
print(f"      grid B 1/alpha_Y range: {min(vals_b):.1f} to {max(vals_b):.1f} (spread factor {max(vals_b) / min(vals_b):.1f}); wide window width {2 * WIDE:.1f}")
vals_a = [chain(d, 'Wilson', enh=e)[0] for d, e in cells]
print(f"      grid A 1/alpha_Y range: {min(vals_a):.1f} to {max(vals_a):.1f}")
# own interpolation over all 8 rows and over a continuous Dgamma
own_all = [chain(r[2], r[1], tau=t)[0] for r in T7 for t in (0.79, 1.0)]
inw = sum(abs(v - tY) <= WIDE for v in own_all)
print(f"      the model's own interpolation, all 8 rows x tau in (0.79, 1): {inw} of {len(own_all)} in the wide window; range {min(own_all):.1f} to {max(own_all):.1f}")
print("  (d) Dgamma_eff composition (weights on the Table 4 pieces; uncorrected pieces, Wilson, enhancement from own interpolation):")
for w2, w3 in itertools.product((0.0, 0.5, 1.0), repeat=2):
    dgx = w2 * parts[2] + w3 * parts[3]
    v = chain(dgx, "Wilson", tau=0.79)[0]
    print(f"      w(Z2)={w2:3.1f} w(Z3)={w3:3.1f}: Dgamma = {dgx:.4f}  1/alpha_Y = {v:6.2f}  {'in wide window' if abs(v - tY) <= WIDE else 'outside'}  ({'principled: Z2 weight 1/2 by direction count; Z3 weight 1 or 1/2 undecided in the source' if (w2 == 0.5 and w3 in (0.5, 1.0)) else 'not a weighting the source supports' })")
print("  (e) action and beta_c: Wilson beta_c 1.0106 / 1.01113 at the starred rows (own interpolation):")
for lab, act, dgp, *_r in T7:
    if act == "Wilson" and _r[-1]:
        print(f"      {lab:10s}: {chain(dgp, 'Wilson')[0]:.3f} / {chain(dgp, 'Wilson', beta_c=MODERN['beta_c'])[0]:.3f}")

# ---- link table (REPORTED)
print("\nLINK TABLE (reported; classification by the criteria of the pre-registration)")
LINKS = [
    ("L1 lattice beta_c", "DERIVED-INDEP", "measured on the lattice; B2 re-measured Wilson 1.0113(10); modern 1.0111331(21) [CQ02]; moves 1/alpha_Y by 0.01"),
    ("L2 beta_c -> alpha_cont (Luck-Jersak fit, 0.20/0.24/0.39; 0.33/0.52)", "DERIVED-ARITH", "form is a fit to Coulomb-potential Monte Carlo data of other authors; arithmetic reproduced (CK4); not re-measured; steep: 1/alpha_cont = 5.0 at Dgamma=0, 8.1 at 0.056"),
    ("L3a base factor 6 = N(N+1)/2", "DERIVED-INDEP", "CK1: lattice algebra, unique under S3 symmetry; premises: SMG^3, hexagonal (tightest-packing) lattice, independent-monopole approximation. Order of events: 'phenomenologically desirable' (1993) and 'roughly 6 ... needed' precede the derivation"),
    ("L3b volume factor 1.34 (B4, B6 terms)", "UNDETERMINED", "extra 4th/6th order action terms introduced to reach the multiple point; not reproducible from the text here"),
    ("L3c linear interpolation 6 -> 8.04 with eta/tau, DW=0.252 dg^(1/3), tau 0.79/1", "CHOSEN", "the text says 'we estimate ... linearly interpolating'; arithmetic reproduced (CK4); modest effect (6 -> 6.5)"),
    ("L4 normalisation: lattice unit = positron charge (U(1)/Z6), q = 1", "CHOSEN", "stated principle (Z_Nmax factor-group rule) plus a self-described speculative 'no wasted monopoles' argument for q = 1; alternatives are excluded by 1 to 3 orders of magnitude (CK6)"),
    ("L5a Z2, Z3 critical couplings 0.44, 0.67", "DERIVED-INDEP", "CK2: exact self-duality"),
    ("L5b plaquette jumps DeltaS_Z2 0.44, Z3 0.56; xi = 0.04", "DERIVED-INDEP" if ck7_ok else "UNDETERMINED", "jumps re-measured by a small 8^4 Monte Carlo of metastable branches (CK7, 6% and 4% below the printed values, inside the 10% criterion); xi = 0.04 is a graphical estimate and a 4% effect"),
    ("L5c eq (122) assembly of Dgamma_eff", "DERIVED-ARITH", "CK3a: Table 4 reproduced from the inputs"),
    ("L5d 'improved' Dgamma (iterated cos power), Table 7", "DERIVED-ARITH" if rec_ok == rec_tot else "UNDETERMINED", f"my reconstruction from the printed exponents reproduces {rec_ok} of {rec_tot} Table 7 values within 3% (all within 1%); the underlying <cos^p> averaging (replacing the average by the power of the mean) is an approximation"),
    ("L5e weights: Z2 x 1/2 (3 of 6 directions), Z3 x 1 or 1/2", "CHOSEN", "Z2 weight by a counting argument; Z3 left open in the text; the starred set differs between Tables 6 and 7"),
    ("L6 action Wilson vs Villain", "CHOSEN", "both printed and both starred; 51.8 to 59.7 in the starred set"),
    ("L8 Planck scale identification and matching", "UNDETERMINED", "inherited from B1: M_P not stated; factor 3 in scale = 1.2 in 1/alpha_Y"),
]
for n, s, why in LINKS:
    print(f"  {s:14s} {n}\n                  {why}")

out = dict(links=[dict(link=n, status=s, evidence=w) for n, s, w in LINKS], y1=float(tY), wide=float(WIDE), sharp=float(SHARP),
           pass_volume_gridA=dict(wide=int(nw), sharp=int(ns), cells=len(cells)), pass_volume_gridB=dict(wide=int(nwb), cells=len(cells_b)),
           req_dg_own=float(req_own), req_dg_enh={str(e): float(solve_dg(e, tY)) for e in ENH}, star7_mean=float(mean7), star6_mean=float(mean6))
if not MUT:
    json.dump(out, open(os.path.join(HERE, "b3_results.json"), "w"), indent=1)

print("\nVERDICT SCAFFOLD (the classification itself is in B3_RESULT.md): internal checks " + ("ALL PASS" if not FAILED else f"FAILED: {FAILED}"))
if MUT:
    fired = any(t.startswith("CK4 ") for t in FAILED)
    print(f"\nMUTATE CONTROL: base factor 6 -> 3.  CK4 row reproduction {'FAILED (as it must)' if fired else 'STILL PASSED'}; all failed checks: {FAILED}  ->",
          "the control fires (exit 1)" if fired else "CONTROL BROKEN (exit 3)")
    sys.exit(1 if fired else 3)
sys.exit(0 if not FAILED else 1)
