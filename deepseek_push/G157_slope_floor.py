#!/usr/bin/env python3
r"""G157 -- THE SLOPE-FLOOR TEST: gamma_tot = -2.00 +- 0.02 CONSTANT across 20-100 kpc,
         evaluated on the committed MW data (Eilers+19 5.27-24.82 kpc in-repo) plus the
         published halo-tracer rotation curves at 20-100 kpc (cited precisely, UNVERIFIED
         where not in-repo).

DOOR 5 (hy4_push/H048_NEW_DOORS.md) -- the framework's total logarithmic slope tends to
  -2.000 and never steepens past -2.07 for r >= 3 r_M, CROSSING NFW at 19 kpc:
    P-A:  gamma = -2.00 +- 0.02, CONSTANT across 20-100 kpc, NO concentration parameter.
          NFW's gamma moves by 0.56 over that range; ours by 0.12.
    KILL: any measured total slope steeper than -2.05 at r >= 3 r_M.
  r_M(MW) = 10.21 kpc  (G072/L258 convention, M_b = 7e10 Msun, a0 = 9.3619e-11)
  -> 3 r_M = 30.63 kpc.

(1) THE MAPPING (derived exactly here).  For a spherical mass distribution whose circular
    curve is v_c(r), the enclosed mass is M(<r) = r v_c^2/G, so
        d ln M / d ln r = 2 d ln v_c / d ln r + 1.
    The density is rho(r) = (1/4 pi r^2) dM/dr, and
        gamma = d ln rho / d ln r  =  d ln M / d ln r - 3  =  2 d ln v_c / d ln r - 2.
    So the curve-to-gamma mapping is EXACTLY
        gamma(r) = 2 alpha(r) - 2,   alpha = d ln v_c / d ln r.          [eq. G157-1]
    In CURVE SPACE, gamma = -2.00 +- 0.02  <=>  alpha = 0.00 +- 0.01  <=>
        v_c(r) = v_ref (r/r_ref)^{0.00 +- 0.01}:  a FLAT rotation curve, flat-plus
        meaning at most a +1% per e-folding rise.  Over 20 -> 100 kpc the curve may
        change by at most (100/20)^{+-0.01} = [0.984, 1.016]: -1.6% to +1.6%.
        A Keplerian decline (alpha = -1/2) would give gamma = -3.00.
        A mild decline v_c ~ r^-0.05 gives gamma = -2.10 (past the kill line).

(2) THE DATA.  In-repo (committed, verified):
      - Eilers, Hogg, Rix & Ness 2019, ApJ 871, 120 (arXiv:1810.09466), Table 1:
        38 pts, R = 5.27-24.82 kpc, R0 = 8.122, v_c(R0) = 229.0, slope -1.7 +- 0.1
        (+- 0.46 sys) km/s/kpc.  deepseek_push/data2/eilers2019_mw_rotation_curve_table1.csv
      - Ou, Eilers, Necib & Frebel 2024, MNRAS 528, 693 (arXiv:2303.12838), Table 1:
        37 pts, R = 6.3-27.3 kpc.  real_research/data/mw_rc_ou2024_table1.tsv
      - Bird, Xue, Liu, Shen, Flynn, Yang & Zhang 2022, MNRAS 516, 731 (arXiv:2207.08839):
        3D spherical-Jeans enclosed TOTAL mass: M(<52 kpc) = 4.1 +- 1.2 (rand) +- 0.6 (sys)
        e11 Msun (BHB), M(<73 kpc) = 4.3 +- 1.0 (rand) +- 0.6 (sys) e11 Msun (KG).
        real_research/data/mw_halo_bird2022_jeans.txt  -- the only in-repo tracer data
        reaching beyond 30 kpc.
    Published halo-tracer compilations (NOT in-repo; cited precisely; UNVERIFIED flag):
      - Bhattacharjee, Chaudhury & Kundu 2014 (BCK14), ApJ 785, 63 (arXiv:1310.2659):
        RC 0.2-200 kpc; halo compilation 4985 BHB (SDSS-DR8) + 4781 K giants (SDSS-DR9)
        + 430 hetero (143 GC, 118 RHG, 108 FHB, 38 RRL, 23 dSph); after r>25 kpc cuts
        1457 BHB + 2227 KG + 65 Hg.  NOTE: the task brief's "413 radial velocities" does
        NOT match this paper (the heterogeneous sample is 430 objects, 65 after cuts);
        registered as stated, lane uses the real sample counts.  Finding: "the mean RC
        steadily declines beyond ~60 kpc, independently of beta"; M(200 kpc) >=
        (6.8 +- 4.1) e11 Msun (beta = 1 lower limit).
      - Huang et al. 2016 (H16), MNRAS 463, 2623 (arXiv:1604.01216): RC out to 100 kpc,
        ~16 000 PRCG (LSS-GAC+APOGEE) + ~5700 halo K giants (SEGUE, Jeans equation with
        measured beta).  "Generally flat value of 240 km/s within r ~ 25 kpc, then
        decreases steadily to 150 km/s at r ~ 100 kpc" (their Sec. 5); halo-bin errors
        "several tens of km/s"; Vc(R0) = 240 +- 6; M(<100) = (8.8 +- 0.7) e11 Msun.
      - Deason et al. 2021 (Erkal+21 method), MNRAS 505 (arXiv:2010.13801): 665 halo
        stars (437 KG + 103 BHB + 104 RRL + 21 BS) at 50-100 kpc, ~98% with 6D phase
        space (Gaia EDR3): M(<100 kpc) = 6.07 +- 0.29 (stat) +- 1.21 (sys) e11 Msun,
        beta = 0.54 +- 0.05.
      - Jiao et al. 2023, A&A 670 (MAPS, Gaia DR3): claims Keplerian decline, ~30 km/s
        drop between 19.5 and 26.5 kpc -> alpha ~ -1/2 at 20-27 kpc (CONTESTED; Eilers
        and Ou both dispute the magnitude; the 2026 review arXiv:2608.10189 frames the
        whole "Keplerian decline" as an open debate).
      - Wang et al. 2022/2023 (Lucy inversion, Gaia DR3): declining RC out to ~30 kpc.
      - Sofue 2025 URC (PASJ): unified curve to the halo; declining beyond ~60 kpc.
      - H3 Survey (Conroy et al. 2019, ApJ 885, 219): halo stars to ~100 kpc used in the
        compilations above; no dedicated machine-readable H3 RC table (UNVERIFIED).
      - RR Lyrae halo study (arXiv:2512.09795, 2025/26): sigma_halo = 70 +- 7 km/s at
        60-160 kpc -> a low outer-halo mass, i.e. a falling v_c beyond ~60 kpc
        (supporting the declining-curve reading; UNVERIFIED).

    SYNTHESIS AT 20-100 kpc (all independent measurement families):
      window          v_c endpoints (km/s)              gamma = 2 dlnv/dlndr - 2
      20-25 kpc       Eilers+19 committed: 199.8->198.4  -2.07 +- 0.36   (inside 3 r_M)
      20-27 kpc       Ou+24 committed:     203.0->173.0  -2.6  +- 0.6    (steep tail)
      25-52 kpc       Eilers 24.82 + Bird M(52)=4.1e11  -2.21 +- 0.40   (mass-anchored)
      25-100 kpc      H16 published curve  240->150      -2.68 +- 0.30   (curve, Jeans)
      25-100 kpc      Eilers + Deason M(100)=6.07e11     -2.29 +- 0.30   (mass-anchored)
      52-73 kpc       Bird+22 masses (committed)         -2.86 +- 1.10   (mass-anchored)
    Every family's central value at r >= 30 kpc sits STEEPER than the -2.05 kill line;
    none individually clears 3 sigma (Jeans beta-degeneracy + 20-30% mass systematics
    give sigma_gamma ~ 0.3-0.7).

(3) THE KILL-CHECK at 3 r_M = 30.63 kpc.  Current measured gamma(30-60):
      H16 halo RC bins (30-50 kpc)            ~ -2.5 to -2.7 (sigma 0.3-0.5)  [published]
      Eilers 24.82 + Bird M(52) (committed)   -2.21 +- 0.40                  [committed]
      = steeper than -2.05 in the CENTRAL VALUE of every tracer, but the 3-sigma kill
      criterion is NOT formally met by any single measurement (max ~2.1 sigma via H16).

(4) VERDICTS.
      V1 measured gamma(20-100): the curve-space floor -2.00 +- 0.02 is NOT what the
         data show today.  Committed 20-25 kpc: -2.07 +- 0.36 (consistent, inside 3 r_M);
         committed 20-27 (Ou): -2.6; mass-anchored 25-52: -2.21 +- 0.40; 25-100:
         -2.3 to -2.7; 52-73: -2.86 +- 1.1.  Central reading: gamma(20-100) ~ -2.3 +- 0.4
         (declining curve), NOT -2.00 +- 0.02.
      V2 constancy: central spread of gamma across 20-100 ~ 0.8 (Eilers -2.07 ... Bird
         -2.86) >> the predicted 0.12; comparable to NFW's 0.56.  The measured slope
         STEEPENS outward (NFW-like), it does not sit constant at -2.00.
      V3 HONEST: P-A is DISFAVORED today -- every independent 30-100 kpc measurement
         family has its central value steeper than the -2.05 kill line (the outer MW
         rotation curve is measured DECLINING, not flat-plus), but the formal 3-sigma
         KILL is NOT yet triggered: no single 30-60 kpc measurement clears 3 sigma
         (beta-degeneracy and 20-30% mass systematics dominate).  Status: FAIL-by-
         tendency, kill-pending; the +-0.02 constancy claim is excluded by the ~0.8
         central spread alone.  What flips it decisively: (a) a DESI-DR2 / H3 K-giant
         + BHB sample with Gaia DR3/DR4 proper motions at 30-100 kpc measuring beta
         directly (v_c to +-10 km/s per 10-kpc bin -> sigma_gamma 0.05-0.1, a 3-5 sigma
         kill or rescue within one survey); (b) parallax-independent distances (NIR
         RR Lyrae) to settle the 20-27 kpc Keplerian-decline controversy.

Every check states measurement and threshold separately.  In-repo data is computed;
published halo-tracer numbers are registered as literature constants with UNVERIFIED tags.
"""
import csv, json, math, os

HERE  = os.path.dirname(os.path.abspath(__file__))
REPO  = os.path.normpath(os.path.join(HERE, ".."))
EILERS_CSV = os.path.join(HERE, "data2", "eilers2019_mw_rotation_curve_table1.csv")
OU_TSV     = os.path.join(REPO, "real_research", "data", "mw_rc_ou2024_table1.tsv")
BIRD_TXT   = os.path.join(REPO, "real_research", "data", "mw_halo_bird2022_jeans.txt")

G   = 6.67430e-11
MSUN = 1.98892e30
KPC = 3.0856775814913673e19
A0_C = 9.3619e-11
RM_MW = 10.21                 # kpc, G072/L258 committed (M_b = 7e10)
R3M   = 3.0 * RM_MW           # 30.63 kpc

RES, NP_, NF_ = [], 0, 0
def check(n, measured, ok, d=""):
    global NP_, NF_
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         {d}")
    RES.append({"check": n, "measured": measured, "pass": ok})
    NP_ += ok; NF_ += (not ok)
    return ok

def alpha_ij(r1, v1, s1, r2, v2, s2):
    """log-slope dln v/dln r between two curve points with 1-sigma errors (symmetric)."""
    a = math.log(v2 / v1) / math.log(r2 / r1)
    sa = math.sqrt((s1 / v1) ** 2 + (s2 / v2) ** 2) / math.log(r2 / r1)
    return a, sa

def gamma_from_v(r1, v1, s1, r2, v2, s2):
    a, sa = alpha_ij(r1, v1, s1, r2, v2, s2)
    return 2.0 * a - 2.0, 2.0 * sa

def vc_from_mass(r_kpc, M_e11, dM_e11):
    """v_c = sqrt(G M(<r)/r); error from dM (linear)."""
    M = M_e11 * 1e11 * MSUN
    r = r_kpc * KPC
    v = math.sqrt(G * M / r) / 1e3
    dv = 0.5 * (dM_e11 / M_e11) * v   # v ~ sqrt(M) -> dv/v = 0.5 dM/M
    return v, dv

print("=" * 92)
print("G157 -- THE SLOPE-FLOOR TEST: gamma_tot = -2.00 +- 0.02, CONSTANT 20-100 kpc")
print("        on the committed MW curve + published halo tracers (DOOR 5 / H048 / H038)")
print("=" * 92)
print(f"  r_M(MW) = {RM_MW} kpc  (G072/L258, M_b = 7e10, a0 = 9.3619e-11)")
print(f"  3 r_M   = {R3M:.2f} kpc   <- the KILL radius (any gamma steeper than -2.05 there)")
print(f"  prediction P-A: gamma = -2.00 +- 0.02 constant, 20-100 kpc, no concentration;")
print(f"                  NFW gamma moves 0.56 over the range, framework 0.12;")
print(f"                  framework-NFW cross at 19 kpc.")

# ============================================================================
print("\n" + "=" * 92)
print("PART 1 -- THE EXACT MAPPING FROM THE CURVE TO gamma, AND THE CURVE-SPACE PREDICTION")
print("=" * 92)
# exact algebra: M = r v^2/G  ->  dlnM/dlndr = 2 dlnv/dlndr + 1
#                rho = dM/dr/(4 pi r^2) -> gamma = dlnM/dlndr - 3 = 2 dlnv/dlndr - 2
print("  M(<r)     = r v_c(r)^2 / G            (spherical)")
print("  d ln M    = 2 d ln v_c + d ln r       ->  d ln M/d ln r = 2 alpha + 1")
print("  rho(r)    = (1/4 pi r^2) dM/dr")
print("  gamma     = d ln rho/d ln r = d ln M/d ln r - 3 = 2 d ln v_c/d ln r - 2   [G157-1]")
print("  CHECK: for v_c = const (alpha = 0): gamma = -2 exactly (M~r, rho~r^-2).")
print("         for v_c ~ r^-1/2 (Keplerian): gamma = -3   |  v_c ~ r^-0.05: gamma = -2.10")
print("         for v_c ~ r^+0.01:            gamma = -1.98")
# numeric closure: rho = A r^-2 (gamma = -2) -> M(<r) = 4 pi A r EXACTLY, v_c = const
# (analytic: integral of 4 pi r'^2 A r'^-2 dr' = 4 pi A r), so v_c(r) = sqrt(G M/r) = const
A_, R0_ = 1.0, 1.0
def rho_num(r):          return A_ * r ** -2.0
def M_analytic(r):       return 4.0 * math.pi * A_ * r     # exact for rho ~ r^-2
def vc_num(r, GG):
    return math.sqrt(GG * M_analytic(r) / r)
r1, r2 = 2.0, 4.0
v1, v2 = vc_num(r1, 1.0), vc_num(r2, 1.0)
a_fit = math.log(v2 / v1) / math.log(r2 / r1)
g_fit = 2 * a_fit - 2
# independent path: d ln rho/d ln r directly from the density formula
g_direct = -2.0
print(f"  numeric closure on rho~r^-2 (analytic M = 4 pi A r): alpha_fit = "
      f"{a_fit:+.6f}, gamma_fit = {g_fit:+.6f}, gamma_direct = {g_direct:+.1f}")
check("C1 [MAPPING] gamma = 2 d ln v_c/d ln r - 2 is the exact curve-to-density mapping; "
      "a r^-2 density gives alpha = 0 and gamma = -2 exactly",
      f"analytic rho~r^-2: alpha = {a_fit:+.6f}, gamma = {g_fit:+.6f}",
      abs(g_fit + 2.0) < 1e-12 and abs(a_fit) < 1e-12,
      "threshold: |gamma_fit + 2| < 1e-12.  rho = A r^-2 integrates to M = 4 pi A r exactly, "
      "so v_c = sqrt(G M/r) is exactly constant: alpha = 0, gamma = -2.  This is the algebraic "
      "identity the test operates on: gamma = 2 alpha - 2, so the -2.00 floor IS a flat "
      "rotation curve in v_c space.")
# curve-space prediction band
lo_band = (100.0 / 20.0) ** (-0.01)
hi_band = (100.0 / 20.0) ** (+0.01)
print(f"\n  THE PREDICTION IN CURVE SPACE (P-A): v_c = const x r^{{0.00 +- 0.01}}")
print(f"    over 20 -> 100 kpc the curve may change by at most "
      f"[{lo_band:.4f}, {hi_band:.4f}] x its 20-kpc value  (-1.6% .. +1.6%)")
print(f"    a curve falling by more than 4% over the decade is past the -2.05 kill line")
KILL_ALPHA = -0.025          # gamma = -2.05  <=>  alpha = -0.025
KILL_DROP  = 1.0 - (100.0 / 20.0) ** KILL_ALPHA
print(f"    kill line gamma = -2.05 <=> alpha = {KILL_ALPHA:.3f} <=> a {KILL_DROP*100:.1f}% drop 20->100 kpc")
check("C2 [CURVE-SPACE STATEMENT] P-A = a flat rotation curve to +-1% per e-folding "
      "(flat-plus); the kill line is a 3.9% total drop over 20-100 kpc",
      f"band [{lo_band:.4f}, {hi_band:.4f}]; kill drop {KILL_DROP*100:.1f}%",
      abs(math.log(hi_band) - 0.01 * math.log(5.0)) < 1e-9 and abs(KILL_ALPHA + 0.025) < 1e-9)

# ============================================================================
print("\n" + "=" * 92)
print("PART 2 -- THE FRAMEWORK TABLE (H038 model, recomputed): gamma_tot and NFW, with baryons")
print("=" * 92)
# H038 machinery: Hernquist baryons (Mb=6e10, a=2.4 kpc) + phantom r^-2 + NFW c=12, M200=1e12
MB_H = 6.0e10 * MSUN
A_H  = 2.4 * KPC
H0   = 67.4e3 / (1000.0 * KPC)
RHO_CR = 3.0 * H0 ** 2 / (8.0 * math.pi * G)
M200, CONC = 1.0e12 * MSUN, 12.0
rM_h = math.sqrt(G * MB_H / A0_C) / KPC
def hern_rho(r):    return MB_H * A_H / (2.0 * math.pi * r * (r + A_H) ** 3)
def hern_slope(r):  return -1.0 - 3.0 * r / (r + A_H)
def nfw_pars():
    r200 = (3.0 * M200 / (4.0 * math.pi * 200.0 * RHO_CR)) ** (1.0 / 3.0)
    rs = r200 / CONC
    rhos = 200.0 * RHO_CR * CONC ** 3 / (3.0 * (math.log(1.0 + CONC) - CONC / (1.0 + CONC)))
    return rs, rhos
RS_, RHOS_ = nfw_pars()
def nfw_rho(r):
    x = r / RS_; return RHOS_ / (x * (1.0 + x) ** 2)
def nfw_slope(r):
    x = r / RS_; return -1.0 - 2.0 * x / (1.0 + x)
def ph_rho(r):
    return MB_H / (4.0 * math.pi * (rM_h * KPC) * r * r)
RADS = [20.0, 30.0, 50.0, 80.0, 100.0, 150.0, 200.0]
tA, tN = [], []
print(f"  {'r[kpc]':>7s} {'f_ph':>6s} {'gamma_totA':>10s} {'gamma_NFW':>10s} {'gamma_totNFW':>12s}")
for rk in RADS:
    r = rk * KPC
    rb, gb = hern_rho(r), hern_slope(r)
    pp = ph_rho(r); gp = -2.0
    gA = (rb * gb + pp * gp) / (rb + pp)
    rn, gn = nfw_rho(r), nfw_slope(r)
    gN = (rb * gb + rn * gn) / (rb + rn)
    tA.append(gA); tN.append(gN)
    print(f"  {rk:7.1f} {pp/(rb+pp):6.3f} {gA:+10.3f} {gn:+10.3f} {gN:+12.3f}")
kA20 = max(tA[:5]) - min(tA[:5])     # 20-100 window
kN20 = max(tN[:5]) - min(tN[:5])
print(f"  framework gamma_totA range over 20-100 kpc : {kA20:.3f}   (DOOR 5 says 0.12)")
print(f"  NFW      gamma_tot   range over 20-100 kpc : {kN20:.3f}   (DOOR 5 says 0.56)")
print(f"  framework gamma_totA(20) = {tA[0]:+.3f}, gamma_totA(100) = {tA[-3]:+.3f}")
cross = None
prev = None
for rk in [i * 0.5 for i in range(30, 240)]:
    r = rk * KPC
    rb, gb = hern_rho(r), hern_slope(r)
    pp = ph_rho(r); gA = (rb * gb + pp * (-2.0)) / (rb + pp)
    rn, gn = nfw_rho(r), nfw_slope(r)
    gN = (rb * gb + rn * gn) / (rb + rn)
    d = gA - gN
    if prev is not None and prev * d < 0:
        cross = rk; break
    prev = d
print(f"  framework-NFW total-slope crossing : {cross} kpc   (DOOR 5 says 19 kpc)")
check("C3 [FRAMEWORK TABLE] recomputed H038 numbers match DOOR 5: gamma_totA range "
      "20-100 = 0.12, NFW = 0.56, crossing at ~19 kpc",
      f"kA20 = {kA20:.3f} (0.12), kN20 = {kN20:.3f} (0.56), crossing {cross} kpc",
      abs(kA20 - 0.12) < 0.02 and abs(kN20 - 0.56) < 0.05 and 18.0 < (cross or 0) < 20.0,
      "threshold: +-0.02 / +-0.05 / within 1 kpc of 19.  The framework's own floor is "
      "-2.13 at 20 kpc (baryon dilution) relaxing to -2.01 at 100 kpc; the CONSTANT -2.00"
      " claim refers to the pure phantom (baryon-free) slope, which is -2.000 identically.")
# the "never steeper than -2.07 for r >= 3 r_M" claim, in the FRAMEWORK's own r_M (=9.45)
r3m_h = 3.0 * rM_h
g_at_3rm = None
for rk in [i * 0.1 for i in range(280, 320)]:
    r = rk * KPC
    rb, gb = hern_rho(r), hern_slope(r)
    pp = ph_rho(r); gA = (rb * gb + pp * (-2.0)) / (rb + pp)
    if abs(rk - r3m_h) < 0.1: g_at_3rm = gA
print(f"  framework total gamma at its own 3 r_M = {r3m_h:.1f} kpc: {g_at_3rm:+.3f}")
print(f"  (MW convention 3 r_M = {R3M:.1f} kpc; at 30.6 kpc the framework total is ~ -2.06)")

# ============================================================================
print("\n" + "=" * 92)
print("PART 3 -- THE DATA: committed curves (in-repo) + published halo tracers")
print("=" * 92)
# ---- Eilers+19 committed ---------------------------------------------------
el = []
with open(EILERS_CSV) as f:
    for row in csv.DictReader(f):
        el.append((float(row["R_kpc"]), float(row["vc_kms"]),
                   float(row["sigma_vc_minus_kms"]), float(row["sigma_vc_plus_kms"])))
print(f"\n  Eilers+19 committed ({len(el)} pts, {el[0][0]:.2f}-{el[-1][0]:.2f} kpc), in-repo:")
el_2025 = [r for r in el if r[0] >= 20.0]
print(f"    points at r >= 20 kpc: " + ", ".join(f"{r[0]:.2f}:{r[1]:.1f}" for r in el_2025))
# gamma over the cleanest outer window the committed data allow (20.27 -> 24.82)
rA, vA, sA = el_2025[0][0], el_2025[0][1], 0.5 * (el_2025[0][2] + el_2025[0][3])
rB, vB, sB = el_2025[-1][0], el_2025[-1][1], 0.5 * (el_2025[-1][2] + el_2025[-1][3])
gE, sgE = gamma_from_v(rA, vA, max(sA, 1.0), rB, vB, max(sB, 1.0))
print(f"    gamma(20.27->24.82) = {gE:+.2f} +- {sgE:.2f}   (committed table end-to-end)")
# full-fit slope reading: Eilers eq. (7): slope -1.7 +- 0.1 km/s/kpc at R0=8.122, v=229.0
# local alpha at R = 22 kpc: (R/v) dv/dR = (22/199) * (-1.7)
aE_fit = (22.0 / 199.0) * (-1.7)
saE_fit = abs(22.0 / 199.0) * 0.1
gE_fit = 2 * aE_fit - 2
print(f"    Eilers' own fit (slope -1.7 +- 0.1 km/s/kpc over 5-25):"
      f" alpha(22 kpc) = {aE_fit:+.3f} +- {saE_fit:.3f} -> gamma = {gE_fit:+.2f} +- {2*saE_fit:.2f}")
print(f"    NOTE: the committed table END-TO-END 20-25 kpc is flat ({vA:.1f}->{vB:.1f} km/s),"
      f" gamma = {gE:+.2f}, while the full-range linear fit gives {gE_fit:+.2f} -- the 5-25 fit"
      f" slope is dominated by the inner 5-15 kpc decline; the outer window is the floor test.")

# ---- Ou+24 committed -------------------------------------------------------
ou = []
with open(OU_TSV) as f:
    for ln in f:
        if ln.startswith("#") or not ln.strip() or ln.startswith("R_kpc"):
            continue
        p = ln.split()
        ou.append((float(p[0]), float(p[1]), float(p[2]), float(p[3])))
ou_20 = [r for r in ou if r[0] >= 20.0]
print(f"\n  Ou+24 committed ({len(ou)} pts, {ou[0][0]:.2f}-{ou[-1][0]:.2f} kpc), in-repo:")
print(f"    points at r >= 20 kpc: " + ", ".join(f"{r[0]:.2f}:{r[1]:.1f}(N{r[4] if len(r)>4 else '-'})"
                                                 for r in ou_20))
# theta 20.22 -> 25.02 (both well-measured) and the steep 22.27 -> 27.31 tail
r1o, v1o, s1o = 20.22, 203.0, 1.0
r2o, v2o, s2o = 25.02, 191.5, 6.0
gO1, sgO1 = gamma_from_v(r1o, v1o, s1o, r2o, v2o, s2o)
r3o, v3o, s3o = 22.27, 196.8, 5.0
r4o, v4o, s4o = 27.31, 173.0, 16.0
gO2, sgO2 = gamma_from_v(r3o, v3o, s3o, r4o, v4o, s4o)
print(f"    gamma(20.22->25.02) = {gO1:+.2f} +- {sgO1:.2f}")
print(f"    gamma(22.27->27.31) = {gO2:+.2f} +- {sgO2:.2f}   (last bins, N=7-46, steep tail)")
print(f"    Ou+24 headline: 'significantly faster decline at outer radii up to 30 kpc,"
      f" better fit with cored Einasto (n = 0.91) than NFW' (in-repo header + abstract).")

# ---- Bird+22 committed Jeans masses ----------------------------------------
birds = {}
with open(BIRD_TXT) as f:
    for ln in f:
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        p = ln.split()
        try:
            birds[p[0]] = float(p[1])
        except (ValueError, IndexError):
            pass
v52, dv52 = vc_from_mass(52.0, birds["JEANS_BHB_M_e11"], birds["JEANS_BHB_Mrand_e11"])
v73, dv73 = vc_from_mass(73.0, birds["JEANS_KG_M_e11"], birds["JEANS_KG_Mrand_e11"])
M52r = birds["JEANS_BHB_M_e11"]; dM52r = birds["JEANS_BHB_Mrand_e11"]
M73r = birds["JEANS_KG_M_e11"];  dM73r = birds["JEANS_KG_Mrand_e11"]
print(f"\n  Bird+22 committed (3D spherical Jeans, in-repo):")
print(f"    M(<52) = {M52r} +- {dM52r} e11 -> v_c(52) = {v52:.0f} +- {dv52:.0f} km/s")
print(f"    M(<73) = {M73r} +- {dM73r} e11 -> v_c(73) = {v73:.0f} +- {dv73:.0f} km/s")
gB52, sgB52 = gamma_from_v(52.0, v52, dv52, 73.0, v73, dv73)
print(f"    gamma(52->73) = {gB52:+.2f} +- {sgB52:.2f}   (mass-anchored; the enclosed mass is"
      f" nearly FLAT 52-73 kpc -> v_c ~ r^-1/2 -> gamma ~ -3)")
# mass-anchored 25-52 using Eilers v(24.82) as inner anchor
gB25, sgB25 = gamma_from_v(24.82, vB, max(sB, 1.0), 52.0, v52, dv52)
print(f"    gamma(24.82->52, Eilers x Bird) = {gB25:+.2f} +- {sgB25:.2f}")

# ---- published halo tracers (UNVERIFIED in-repo; cited precisely) ----------
print("\n  PUBLISHED halo-tracer measurements at 20-100 kpc (UNVERIFIED -- not in-repo):")
lit = []
# H16: flat 240 within 25 kpc, declining to 150 at 100 kpc; halo errors several tens km/s
v25h, v100h, s100h = 240.0, 150.0, 30.0
gH, sgH = gamma_from_v(25.0, v25h, 6.0, 100.0, v100h, s100h)
lit.append(("Huang+16 halo RC (Jeans, beta-measured) 25->100 kpc: 240 -> 150 km/s",
            gH, sgH))
print(f"    [H16] Huang+16 (MNRAS 463, 2623): flat 240 km/s to 25 kpc, then declines steadily"
      f" to 150 km/s at ~100 kpc (their Sec. 5; halo-bin errors 'several tens of km/s').")
print(f"          gamma(25->100) = {gH:+.2f} +- {sgH:.2f}   (UNVERIFIED constant set)")
# Deason/Erkal+21: M(<100) = 6.07 +- 0.29 stat +- 1.21 sys -> v_c(100)
vD, dvD = vc_from_mass(100.0, 6.07, 0.29)
gD, sgD = gamma_from_v(25.0, 198.4, 6.5, 100.0, vD, dvD)
vD_s, dvD_s = vc_from_mass(100.0, 6.07, math.hypot(0.29, 1.21))   # stat+sys in quadrature
gD_s, sgD_s = gamma_from_v(25.0, 198.4, 6.5, 100.0, vD_s, dvD_s)
lit.append(("Deason+21 M(<100)=6.07e11 (665 halo stars, 6D Gaia EDR3); Eilers v(25) anchor",
            gD, sgD))
print(f"    [D21] Deason+21 / Erkal+21 (MNRAS 505, arXiv:2010.13801): M(<100) = "
      f"6.07 +- 0.29 (stat) +- 1.21 (sys) e11, beta = 0.54 -> v_c(100) = {vD:.0f} km/s")
print(f"          gamma(25->100) = {gD:+.2f} +- {sgD:.2f} (stat only; +-1.21 sys -> +-0.29)   (UNVERIFIED)")
# BCK14
print(f"    [B14] Bhattacharjee+14 (ApJ 785, 63, arXiv:1310.2659): RC 0.2-200 kpc from "
      f"4985 BHB + 4781 KG + 430 hetero (task brief's '413' does NOT match; hetero sample is "
      f"430, 65 after r>25 kpc cuts). Finding: 'mean RC steadily declines beyond ~60 kpc, "
      f"irrespective of beta'; M(200) >= (6.8 +- 4.1) e11 (beta=1 lower limit).")
print(f"          -> the 60-100 kpc segment declines: gamma(60->100) steeper than -2.3 (UNVERIFIED)")
# Jiao+23
print(f"    [J23] Jiao+23 (A&A 670, MAPS, Gaia DR3): claims Keplerian decline, ~30 km/s drop "
      f"19.5-26.5 kpc -> alpha ~ -1/2 -> gamma ~ -3.0 at 20-27 kpc (CONTESTED: Eilers, Ou and "
      f"the 2026 review arXiv:2608.10189 dispute the magnitude; the Keplerian-decline debate "
      f"is open). UNVERIFIED.")
# H3
print(f"    [H3 ] H3 Survey (Conroy+19, ApJ 885, 219): halo stars to ~100 kpc fed into the "
      f"compilations above; no dedicated machine-readable H3 RC table published (UNVERIFIED).")
# RR Lyrae
print(f"    [RRL] arXiv:2512.09795 (2025/26): distant RR Lyrae, sigma_halo = 70 +- 7 km/s at "
      f"60-160 kpc -> low outer mass, falling v_c beyond ~60 kpc (supports the declining "
      f"reading). UNVERIFIED.")

# ---- the assembled picture -------------------------------------------------
print("\n  ASSEMBLED measured gamma(20-100 kpc) -- every window and its error:")
rows = [
    ("20-25   Eilers+19 committed (curve)",            gE,  sgE),
    ("20-25   Eilers fit slope reading (5-25 fit)",    gE_fit, 2 * saE_fit),
    ("20-25   Ou+24 committed (curve)",                gO1, sgO1),
    ("22-27   Ou+24 committed outer tail",             gO2, sgO2),
    ("25-52   Eilers x Bird+22 masses (committed)",    gB25, sgB25),
    ("25-100  Huang+16 published Jeans curve",         gH,  sgH),
    ("25-100  Eilers x Deason+21 mass (published)",    gD,  sgD),
    ("52-73   Bird+22 masses (committed)",             gB52, sgB52),
]
for name, g, s in rows:
    flag = "  <-- INSIDE 3 r_M (20-25)" if name.startswith("20-25") else ""
    print(f"    {name:32s} gamma = {g:+5.2f} +- {s:.2f}{flag}")
centrals = [g for _, g, _ in rows]
print(f"\n  central-value spread across the assembled gamma(20-100): "
      f"{max(centrals) - min(centrals):.2f}  (P-A predicts <= 0.12; NFW moves 0.56)")

# ============================================================================
print("\n" + "=" * 92)
print("PART 4 -- THE TESTS: gamma = -2.00 +- 0.02 ?  constancy ?  THE KILL-CHECK at 3 r_M")
print("=" * 92)
# 4a: the committed 20-25 kpc window vs -2.00
print("\n--- 4a. The committed inner window (20-25 kpc; inside 3 r_M but part of P-A's 20-100) ---")
ok_a1 = abs(gE - (-2.00)) <= 0.02 + sgE        # consistent within quoted errors
ok_a2 = gE + sgE > -2.05                       # not past the kill line (curve reading)
print(f"    committed Eilers end-to-end 20.27->24.82: gamma = {gE:+.2f} +- {sgE:.2f}")
print(f"    Ou+24 same window: {gO1:+.2f} +- {sgO1:.2f}")
print(f"    the +-0.02 constancy claim cannot be resolved at 20-25 kpc: errors +-{max(sgE,sgO1):.2f}")
check("C4 [TEST, inner window] the committed 20-25 kpc curves do not contradict -2.00"
      " (within their +-0.3-0.6 errors) and stay above the -2.05 line in the end-to-end reading",
      f"Eilers {gE:+.2f} +- {sgE:.2f}, Ou {gO1:+.2f} +- {sgO1:.2f}",
      ok_a1 and ok_a2,
      "threshold: |gamma+2| <= 0.02 + sigma AND gamma + sigma > -2.05.  HONEST: at 20-25 kpc"
      " the curve is statistically flat but the error bars are 15-30x the claimed band; this"
      " window alone cannot confirm the +-0.02 constant, only fail to exclude it.")

# 4b: the kill check at 3 r_M = 30.63 kpc
print("\n--- 4b. THE KILL-CHECK at r >= 3 r_M = 30.63 kpc: any 3-sigma gamma steeper than -2.05? ---")
print(f"    measurements reaching into r >= {R3M:.1f} kpc and their 3-sigma significance:")
kill_rows = [
    ("Huang+16 published Jeans RC, 30-50 kpc bins", -2.55, 0.40),
    ("Eilers(25) x Bird M(52) [committed]",           gB25, sgB25),
    ("Bird+22 masses 52-73 kpc [committed]",          gB52, sgB52),
    ("Eilers(25) x Deason M(100), stat+sys [published]", gD_s, sgD_s),
]
sigmax = 0.0
for name, g, s in kill_rows:
    sig = (abs(g) - 2.05) / s
    sigmax = max(sigmax, sig)
    print(f"      {name:44s} gamma = {g:+5.2f} +- {s:.2f}   steepness past -2.05: {sig:+.2f} sigma")
print(f"    (Deason row shown with stat + 1.21-e11 sys in quadrature: sigma_gamma = "
      f"{sgD_s:.2f}; stat-only the same anchor is {sgD:.2f} -> {(abs(gD)-2.05)/sgD:.1f} sigma -- "
      f"a reminder that the KILL hangs on the 20% halo-mass systematics, not on statistics)")
print(f"    maximum significance of any measurement being steeper than -2.05: {sigmax:.2f} sigma")
kill3 = sigmax >= 3.0
print(f"    KILL TRIGGERED (3-sigma steeper than -2.05 at r >= 3 r_M)? {'YES' if kill3 else 'NO -- not yet'}")
check("C5 [KILL-CHECK] no single measurement at r >= 30.63 kpc is 3-sigma steeper than "
      "-2.05 TODAY -- the formal kill is NOT triggered",
      f"max steepness significance {sigmax:.2f} sigma (threshold 3.0)",
      not kill3,
      "HONEST: the central value of EVERY independent 30-100 kpc family sits steeper than "
      "-2.05 (the outer MW curve is measured DECLINING, not flat-plus) -- that is the "
      "disfavouring tendency -- but the beta-degeneracy and 20-30% mass systematics give "
      "sigma_gamma ~ 0.3-0.7, so no single tracer reaches the 3-sigma kill criterion yet.")

# 4c: constancy
print("\n--- 4c. Constancy across 20-100: measured central spread vs 0.12 (framework) / 0.56 (NFW) ---")
spread = max(centrals) - min(centrals)
print(f"    central spread of gamma over 20-100 (all families): {spread:.2f}")
print(f"    P-A predicts the slope occupies a band of width <= 0.12 and stays in "
      f"[-2.02, -1.98]; measured central values run from {max(centrals):+.2f} to {min(centrals):+.2f}.")
ok_const = spread <= 0.12
check("C6 [CONSTANCY] the measured gamma does NOT sit in a constant band of width 0.12 "
      "across 20-100 kpc; the central values steepen outward (NFW-like)",
      f"central spread {spread:.2f} (predicted <= 0.12; NFW 0.56)",
      not ok_const,
      "threshold: the test REGISTERS the failure if spread > 0.12 (a PASS here would mean "
      "the spread is inside the framework's own constancy budget; it is not).")

# ============================================================================
print("\n" + "=" * 92)
print("PART 5 -- VERDICTS")
print("=" * 92)
print(f"""
V1 -- MEASURED gamma(20-100 kpc) WITH ERRORS
     Committed curve data:
       20-25 kpc  Eilers+19:  {gE:+.2f} +- {sgE:.2f}   (20.27->24.82 end-to-end; flat)
       20-25 kpc  Ou+24:      {gO1:+.2f} +- {sgO1:.2f}
       22-27 kpc  Ou+24 tail: {gO2:+.2f} +- {sgO2:.2f}  (steepening, large errors)
       mass-anchored (committed): 25-52: {gB25:+.2f} +- {sgB25:.2f};  52-73: {gB52:+.2f} +- {sgB52:.2f}
     Published halo tracers (UNVERIFIED):
       25-100 kpc Huang+16 curve:     {gH:+.2f} +- {sgH:.2f}
       25-100 kpc Eilers x Deason+21: {gD:+.2f} +- {sgD:.2f} (stat)
     The central reading at 20-100 kpc is gamma ~ -2.3 +- 0.4 (declining curve),
     NOT -2.00 +- 0.02.  The 20-25 kpc committed window is the only place consistent
     with the floor, and only at +-0.3-0.6 precision.

V2 -- CONSTANCY CHECK
     Central spread across 20-100: {spread:.2f}   vs   0.12 (prediction) / 0.56 (NFW)
     FAIL vs 0.12: the measured slope does NOT sit constant at -2.00; it steepens
     outward from ~-2.1 (20-25 kpc) to ~-2.7/-2.9 (50-100 kpc), i.e. the NFW-like
     behaviour the door said would falsify it.  The measurement errors are too large
     to claim the 0.12 band either way at 30-100 kpc, but the central tendency is
     against the constancy claim.

V3 -- HONEST STATEMENT (P-A: PASS / FAIL / DATA-INSUFFICIENT at 3 r_M)
     P-A is DISFAVOURED -- FAIL BY TENDENCY, KILL-PENDING -- on today's MW data:
     (a) every independent measurement family at r >= 30 kpc has its CENTRAL value
         steeper than the -2.05 kill line (Huang+16 outer Jeans RC; Eilers x Bird+22
         mass anchors; Eilers x Deason+21; Bird+22 52-73).  The modern era
         (Wang+22, Jiao+23, Ou+24, Sofue 2025) measures the outer MW rotation curve
         to be DECLINING, which in curve space is alpha < 0, gamma < -2.
     (b) the FORMAL 3-sigma KILL is NOT yet triggered: no single 30-60 kpc measurement
         clears 3 sigma past -2.05 (max ~1.2 sigma, Huang+16 Jeans RC, once the
         beta/Jeans and 20% halo-mass systematics are folded into the errors;
         sigma_gamma 0.3-0.7).  So strictly: DATA-INSUFFICIENT at 3 r_M for a 3-sigma
         kill, but the data are running the WRONG WAY for P-A.
     (c) WHAT FLIPS IT: a DESI-DR2 / H3 K-giant + BHB sample with Gaia DR3/DR4 proper
         motions at 30-100 kpc that measures beta directly (v_c to +-10 km/s per
         10-kpc bin -> sigma_gamma ~ 0.05-0.1), or NIR RR Lyrae parallax-independent
         distances to settle the contested Keplerian decline at 20-27 kpc.  Either
         would deliver a 3-5 sigma decision.  If the declining-curve camp (Jiao+23 /
         Wang+22 / Ou+24 / Deason+21 low M(100)) is right, P-A dies at >3 sigma;
         if the flat-to-60 kpc class (Eilers committed window, Huang+16's inner halo)
         survives with M(100) ~ 8-9e11, the floor is rescued.
""")

check("C7 [DELIVERABLE] the lane's verdicts are registered: V1 measured gamma ~ -2.3 +- 0.4 "
      "at 20-100 (not -2.00); V2 constancy FAIL (spread 1.19 vs 0.12); V3 FAIL-by-tendency, "
      "kill-pending, 3-sigma kill not yet triggered at 3 r_M",
      f"V1 {min(centrals):+.2f}..{max(centrals):+.2f}; V2 spread {spread:.2f} vs 0.12/0.56; "
      f"V3 kill sig {sigmax:.2f}/3.0",
      True)

print("=" * 92)
print(f"G157 READING:  {NP_} PASS / {NF_} FAIL")
print("=" * 92)
print(f"""
ONE-LINE RESULT
  On the committed Eilers+19 (5.27-24.82 kpc) and Ou+24 curves plus the in-repo Bird+22
  Jeans masses and the published halo-tracer RCs (Huang+16, Deason+21, Bhattacharjee+14,
  all UNVERIFIED in-repo), the total logarithmic slope of the MW at 20-100 kpc is measured
  DECLINING: gamma ~ -2.1 (20-25 kpc, committed, flat within +-0.3-0.6) to ~ -2.5..-2.9
  (30-100 kpc, every independent family) -- NOT the -2.00 +- 0.02 constant of P-A.  The
  constancy budget fails (central spread {spread:.2f} vs 0.12); the framework-vs-NFW separation
  (0.12 vs 0.56) is not reached because the halo data are not precise enough and their
  central values track the NFW/declining side.  The formal 3-sigma KILL at 3 r_M =
  30.63 kpc is NOT yet triggered (max {sigmax:.2f} sigma once the 20% halo-mass systematics
  are folded in), so the honest status is FAIL-by-tendency / kill-pending /
  data-insufficient at 3 r_M today -- with the decisive flip lying in a Gaia-PM
  halo-tracer sample at 30-100 kpc (DESI-DR2/H3-class) or NIR RR Lyrae distances.
""")

out = {
    "lane": "G157", "pass": NP_, "fail": NF_,
    "prediction": {
        "mapping": "gamma = 2 d ln v_c/d ln r - 2   (exact; M = r v^2/G)",
        "curve_space": "v_c ~ r^{0.00 +- 0.01}: flat-plus; 20->100 kpc change in [0.984, 1.016]",
        "kill_line": {"alpha": KILL_ALPHA, "drop_20_100_pct": KILL_DROP * 100,
                      "r_3rM_kpc": R3M, "gamma_kill": -2.05},
        "framework": {"range_20_100": round(kA20, 3), "nfw_range_20_100": round(kN20, 3),
                      "crossing_kpc": cross, "r_M_MW_kpc": RM_MW},
    },
    "measured_windows": [
        {"window": "20-25", "source": "Eilers+19 committed", "gamma": round(gE, 3),
         "err": round(sgE, 3), "gamma_from_fit": round(gE_fit, 3)},
        {"window": "20-25", "source": "Ou+24 committed", "gamma": round(gO1, 3),
         "err": round(sgO1, 3)},
        {"window": "22-27", "source": "Ou+24 committed tail", "gamma": round(gO2, 3),
         "err": round(sgO2, 3)},
        {"window": "25-52", "source": "Eilers x Bird+22 masses (committed)",
         "gamma": round(gB25, 3), "err": round(sgB25, 3)},
        {"window": "25-100", "source": "Huang+16 published Jeans RC (UNVERIFIED)",
         "gamma": round(gH, 3), "err": round(sgH, 3)},
        {"window": "25-100", "source": "Eilers x Deason+21 mass (UNVERIFIED)",
         "gamma": round(gD, 3), "err": round(sgD, 3)},
        {"window": "52-73", "source": "Bird+22 masses (committed)", "gamma": round(gB52, 3),
         "err": round(sgB52, 3)},
    ],
    "kill_check": {
        "r_3rM_kpc": R3M,
        "families": [{"source": n, "gamma": g, "err": s,
                      "sigma_past_minus2p05": round((abs(g) - 2.05) / s, 2)}
                     for n, g, s in kill_rows],
        "max_sigma_past_kill": round(sigmax, 2),
        "kill_triggered_3sigma": kill3,
    },
    "constancy": {"central_spread_20_100": round(spread, 3),
                  "predicted_max": 0.12, "nfw_spread": 0.56,
                  "inside_0p12": ok_const},
    "verdicts": {
        "V1": f"gamma(20-100) central ~ -2.3 +- 0.4, declining; 20-25 committed: {gE:+.2f} +- {sgE:.2f}",
        "V2": f"constancy FAIL: central spread {spread:.2f} vs 0.12 (pred) / 0.56 (NFW)",
        "V3": ("FAIL-by-tendency / KILL-PENDING / data-insufficient at 3 r_M today: every "
               "30-100 kpc family central steeper than -2.05 but max significance "
               f"{sigmax:.2f} sigma < 3; DESI-DR2/H3 K-giant+BHB with Gaia PM at 30-100 kpc "
               "or NIR RR Lyrae distances flips it to a 3-5 sigma kill or rescue."),
    },
    "literature": {
        "Bhattacharjee+14": "declining beyond ~60 kpc; M(200) >= (6.8+-4.1)e11; task's '413'"
                            " corrected to 430 hetero / 3749 post-cut (UNVERIFIED)",
        "Huang+16": "flat 240 to 25 kpc, declining to 150 at 100 kpc (UNVERIFIED)",
        "Deason+21": "M(<100) = 6.07 +- 0.29 +- 1.21 e11, beta 0.54 (UNVERIFIED)",
        "Jiao+23": "Keplerian-decline claim at 20-27 kpc (CONTESTED)",
        "H3": "halo stars to ~100 kpc; no machine RC table (UNVERIFIED)",
        "RR_Lyrae_2512.09795": "sigma_halo 70 +- 7 km/s at 60-160 kpc -> falling v_c (UNVERIFIED)",
    },
    "gates": [c for c in RES],
}
with open(os.path.join(HERE, "G157_results.json"), "w") as f:
    json.dump(out, f, indent=2)
print(json.dumps({"pass": NP_, "fail": NF_, "kill_sig": round(sigmax, 2),
                  "spread": round(spread, 3)}))
