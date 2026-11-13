#!/usr/bin/env python3
"""PRJ1: every number quoted by SEALED_PREDICTIONS.md, computed from the rules of the CANDIDATE sixth rule (the
crossing-speed joint, NOT ADOPTED) and of its two rivals (the split at FRZ1's constant v_stiff; the unsplit settled
family), with an SI check against the values JNT2, SRJ2, FLD1, LNJ1, DSC1 and DSC1R stored.
Footings canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), never pooled. One thread, light compute.
  python3 -I -B prj1_numbers.py > prj1_numbers.out
Sources (copied, cited; read-only):
  v*(z), v_L, M_b*(z): closure_2026_11_13/JNT2_crossing_speed_joint/jnt2_common.py (constants recomputed here in SI and
    compared with the module, which is imported read-only).
  The record's reference halo (FRZ1 / SRJ2 / SRJ3 / LNJ1 / DSC1R A1): halo_basics_z, conc, dta_of, Omz copied from
    closure_2026_11_13/LNJ1_joint_switch_on_euclid_lenses/lnj1.py lines 104-121 (= FRZ1's frz1_hm.py); the share X from
    closure_2026_11_09/PD1_phantom_is_dust/pd1.json as LNJ1 line 147 (median share_over_Mb, z < 1 -> z0.0, else z1.0).
  v_stiff boundary: SRJ2's vgal (closure_2026_11_12/SRJ2_regime_split_joint/srj2_rc.py lines 38-48) rebuilt.
  R_fold, R_ta: FLD1's run files (fable52_push/FLD1_fold_reach/runs/hubble_<foot>_M<logMb>_zi10_N2400.json), read as
    FZS1's rfold_kpc (closure_2026_11_10/FZS1_forest_settled_radius/fzs1_hm.py lines 33-45).
Cold dark energy is a gravitating field component, not a particle. kappa = 1/2 and 5.41 are FITTED.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
sys.dont_write_bytecode = True
import importlib.util
import numpy as np
from scipy.optimize import brentq
from scipy.special import i0, i1, k0, k1

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = []; CHK = []
def P(s=""): print(s, flush=True); OUT.append(s)
def check(name, got, want, tol, rel=True):
    d = abs(got / want - 1) if rel else abs(got - want); ok = d <= tol
    CHK.append(ok); P(f"  CHECK {name}: {got:.6g} vs stored {want:.6g} ({'rel' if rel else 'abs'} dev {d:.2e}, tol {tol:g}) -> {'PASS' if ok else 'FAIL'}")

# ---------------------------------------------------------------- SI constants (JNT2's choices, recomputed)
G = 6.67430e-11; MSUN = 1.98892e30; MPC = 3.0856775814913673e22; KPC = MPC / 1e3
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOTS = ("canonical", "alt")
XS = 5.41; H0 = 67.4e3 / MPC; OL = 0.6847; OM = 1 - OL
VSTIFF = {"canonical": 265.8, "alt": 288.1}
def E(z): return math.sqrt(OM * (1 + z) ** 3 + OL)
def vstar(ft, z): return A0[ft] / (10 * (1 + XS) * H0 * E(z))                      # m/s
def logMbstar(ft, z): return math.log10(vstar(ft, z) ** 4 / (G * A0[ft]) / MSUN)  # law's flat speed = v*
def logMbstar_virial(ft, z):                                                       # v_L = v*  (same number)
    return math.log10(vstar(ft, z) ** 3 / (10 * G * (1 + XS) * H0 * E(z)) / MSUN)
def M200c_switch(ft, z): return vstar(ft, z) ** 3 / (10 * G * H0 * E(z)) / MSUN   # total mass whose v200c = v*
def vL(Mb, z): return (10 * G * (1 + XS) * Mb * MSUN * H0 * E(z)) ** (1 / 3)
def glaw(gN, a0): return 0.5 * (gN + np.sqrt(gN * gN + 4 * gN * a0))

# ---------------------------------------------------------------- the record's reference halo (copied from LNJ1 / FRZ1)
hh = 0.6736; om_b, om_c = 0.02237, 0.1200
Om_h = (om_b + om_c) / hh ** 2; FB = om_b / (om_b + om_c); RHO_M = Om_h * 2.77536627e11; GH = 4.30091e-9
m_nfw = lambda x: np.log1p(x) - x / (1 + x)
def Omz(z): return Om_h * (1 + z) ** 3 / (Om_h * (1 + z) ** 3 + 1 - Om_h)
def dta_of(z): return 5.55 + (11.81 - 5.55) * (1 - Omz(z)) / (1 - Om_h)
def conc_fn(z): return lambda M: 10.14 * (M / 2e12) ** -0.081 * (1 + z) ** -1.01
def halo_basics_z(M, conc, dta, omz):
    c = conc(M); r2 = (3 * M / (4 * math.pi * 200 * RHO_M)) ** (1 / 3); mc = m_nfw(c)
    xta = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - dta / 200.0, 1.0, 80.0, xtol=1e-12)
    xc = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - 1.0 / omz, 0.05, 1.0, xtol=1e-12)
    return dict(M=M, c=c, r200=r2, rs=r2 / c, mc=mc, rta=xta * r2, Mta=M * m_nfw(c * xta) / mc, r200c=xc * r2, M200c=M * m_nfw(c * xc) / mc)
PD1 = json.load(open(os.path.join(REPO, "closure_2026_11_09", "PD1_phantom_is_dust", "pd1.json")))
XTAB = {f: {k: float(np.median([r["share_over_Mb"] for r in PD1[f]["share_tables"][k]])) for k in ("z0.0", "z1.0")} for f in FOOTS}
def Xof(ft, z): return XTAB[ft]["z0.0"] if z < 1 else XTAB[ft]["z1.0"]
def ref_halo(ft, Mb, z):
    """record's reference halo for baryon mass Mb (Msun) at z: cold mass X M_b as NFW to r_ta. Physical kpc."""
    conc = conc_fn(z); dta = dta_of(z); omz = Omz(z); Mta = Xof(ft, z) * Mb * hh / (1 - FB)
    lM = brentq(lambda l: halo_basics_z(10 ** l, conc, dta, omz)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-12)
    hb = halo_basics_z(10 ** lM, conc, dta, omz); a = 1e3 / hh / (1 + z)                          # comoving Mpc/h -> physical kpc
    v = math.sqrt(GH * hb["M200c"] * (1 + z) / hb["r200c"])                                       # FRZ1's v_vir (km/s)
    return dict(X=Xof(ft, z), rs=hb["rs"] * a, rta=hb["rta"] * a, r200c=hb["r200c"] * a, c=hb["c"], v_vir=v, M200c_h=hb["M200c"])
def g_ref_halo(H, Mb, r_kpc):
    r = np.minimum(np.asarray(r_kpc, float), H["rta"])
    Cr = H["X"] * Mb * MSUN * m_nfw(r / H["rs"]) / m_nfw(H["rta"] / H["rs"])
    return G * Cr / (np.asarray(r_kpc, float) * KPC) ** 2
def lMb_vstiff(ft, z): return brentq(lambda l: ref_halo(ft, 10 ** l, z)["v_vir"] - VSTIFF[ft], 8.5, 13.5, xtol=1e-7)

# ---------------------------------------------------------------- FLD1's fold radius (FZS1's reader)
MASSES = [6.5, 7, 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, 12]
FT = {f: {M: np.array(json.load(open(os.path.join(REPO, "fable52_push", "FLD1_fold_reach", "runs", f"hubble_{f}_M{M:g}_zi10_N2400.json")))["series"]) for M in MASSES} for f in FOOTS}
def at_z(S, z, col=2):
    o = np.argsort(S[:, 1]); return float(np.interp(z, S[o, 1], S[o, col]))
def rfold_kpc(ft, z, lM, col=2):
    R = np.array([at_z(FT[ft][M], z, col) for M in MASSES])
    if lM < MASSES[0]: return float(R[0] * 10 ** ((lM - MASSES[0]) / 3))
    if lM > MASSES[-1]: return float(R[-1] * 10 ** ((lM - MASSES[-1]) / 3))
    if np.any(R <= 0): return float(np.interp(lM, MASSES, R))
    return float(10 ** np.interp(lM, MASSES, np.log10(R)))

# ---------------------------------------------------------------- an exponential disc (Freeman 1970, thin, in the plane)
def gN_disc(Mb, Rhalf_kpc, r_kpc):
    Rd = Rhalf_kpc / 1.67835 * KPC; r = np.asarray(r_kpc, float) * KPC; y = r / (2 * Rd)
    S0 = Mb * MSUN / (2 * math.pi * Rd ** 2)
    v2 = 4 * math.pi * G * S0 * Rd * y ** 2 * (i0(y) * k0(y) - i1(y) * k1(y))
    return v2 / r

P("PRJ1 numbers for the sealed predictions of the CANDIDATE sixth rule (crossing-speed joint). NOT ADOPTED.")
P("Footings canonical / alt never pooled. kappa = 1/2 and 5.41 FITTED. Adopts nothing.")
P()
# ================================================================ 1. the switch
P("== 1. The switch: v*(z) = a0 / (10 (1 + X) H(z)); log M_b*(z) = log[v*^4 / (G a0)]; M200c at v200c = v*")
ZL = [0.0, 0.3, 0.5, 0.66, 1.0, 1.2, 1.5, 2.0, 2.2, 2.3, 2.5, 3.0, 3.5, 4.0, 4.4, 4.5, 5.0, 6.0]
for ft in FOOTS:
    P(f"[{ft}]  z | E(z) | v*(z) km/s | log M_b* (law speed) | log M_b* (lemma virial; must equal) | log M200c switch (Msun) | (Msun/h)")
    for z in ZL:
        a, b = logMbstar(ft, z), logMbstar_virial(ft, z); assert abs(a - b) < 1e-9
        Ms = M200c_switch(ft, z)
        P(f"  {z:4.2f} | {E(z):6.4f} | {vstar(ft, z) / 1e3:7.2f} | {a:6.3f} | {b:6.3f} | {math.log10(Ms):6.3f} | {math.log10(Ms * hh):6.3f}")
P()
P("SI check against stored values")
spec = importlib.util.spec_from_file_location("jnt2_common_ro", os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint", "jnt2_common.py"))
J = importlib.util.module_from_spec(spec); spec.loader.exec_module(J)
for ft, v0 in (("canonical", 668.53), ("alt", 807.93)):
    check(f"v*(0) {ft} vs JNT2 / DSC1 KA-B / LNJ1 KA-3 (668.53 / 807.93)", vstar(ft, 0) / 1e3, v0, 0.005, rel=False)
    check(f"v*(0) {ft} vs jnt2_common.vstar0_kms (module, read-only)", vstar(ft, 0) / 1e3, J.vstar0_kms(ft), 1e-12)
    for z in (0.0, 1.0, 2.0, 2.3, 4.4):
        check(f"log M_b*({z}) {ft} vs jnt2_common.logMstar", logMbstar(ft, z), J.logMstar(ft, z), 1e-9, rel=False)
for ft, vals in (("canonical", (13.21, 12.19, 11.28)), ("alt", (13.45, 12.44, 11.53))):
    for z, v in zip((0, 1, 2), vals): check(f"log M_b*({z}) {ft} vs COMPLETED_FORM rule 6 (2 decimals)", logMbstar(ft, z), v, 0.005, rel=False)
check("log M_b*(2) canonical vs DSC1R KA1 (11.279)", logMbstar("canonical", 2.0), 11.279, 0.0005, rel=False)
check("log M_b*(2) alt vs DSC1R KA1 (11.526)", logMbstar("alt", 2.0), 11.526, 0.0005, rel=False)
for ft, z, vs in (("canonical", 1, 373.3), ("canonical", 2, 220.4), ("canonical", 2.5, 177.4), ("alt", 1, 451.1), ("alt", 2, 266.4), ("alt", 2.5, 214.4)):
    check(f"v*({z}) {ft} vs COMPLETED_FORM table", vstar(ft, z) / 1e3, vs, 0.06, rel=False)
# JNT2's forest grid: lightest grid M200c above v*(z) (Msun/h). The grid is discrete, so the stored value must lie at or
# just above the analytic switch mass (within one grid step of FRZ1's mass grid: 0.05 dex? reported, tolerance 0.1 dex).
hm = json.load(open(os.path.join(REPO, "closure_2026_11_13", "JNT2_crossing_speed_joint", "jnt2_hm.json")))
for ft in FOOTS:
    for z in ("2.2", "3.0", "4.4"):
        st = hm["membership"][ft][z]["lightest_above_M200c"]; an = M200c_switch(ft, float(z)) * hh
        d = math.log10(st) - math.log10(an); ok = -0.005 <= d <= 0.1; CHK.append(ok)
        P(f"  CHECK forest switch M200c z {z} {ft}: analytic {an:.3e} Msun/h, JNT2 lightest grid halo above {st:.3e} (log diff {d:+.3f}; 0 to +0.1) -> {'PASS' if ok else 'FAIL'}")
P()
# ================================================================ 2. the record's reference halo and the v_stiff rival
P("== 2. The record's reference halo (X from PD1) and the rival boundary at FRZ1's v_stiff")
for ft in FOOTS: P(f"  X {ft}: z < 1 {XTAB[ft]['z0.0']:.4f}, z >= 1 {XTAB[ft]['z1.0']:.4f}")
check("X canonical z>=1 vs DSC1R A1 (55.72)", XTAB["canonical"]["z1.0"], 55.72, 0.005, rel=False)
check("X alt z<1 vs DSC1R A1 (59.50)", XTAB["alt"]["z0.0"], 59.50, 0.005, rel=False)
H = ref_halo("canonical", 10 ** 10.95, 2.24); Rm = 4.31
gmod = float(G * (10 ** 10.95 / 2 * MSUN) / (Rm * KPC) ** 2 + g_ref_halo(H, 10 ** 10.95, Rm))
check("LNJ1 KA-4 / SRJ3 K5 zC 400569 r_200c (121.62 kpc)", H["r200c"], 121.62, 1e-3)
check("LNJ1 KA-4 / SRJ3 K5 zC 400569 r_s (39.53 kpc)", H["rs"], 39.53, 1e-3)
check("LNJ1 KA-4 / SRJ3 K5 zC 400569 g_mod (4.4290e-10)", gmod, 4.4290e-10, 1e-3)
H2 = ref_halo("canonical", 2e11, 2.3)
check("DSC1R A1 KA1 halo M_b 2e11 z 2.3: c (2.92)", H2["c"], 2.92, 0.006, rel=False)
check("DSC1R A1 KA1 halo M_b 2e11 z 2.3: r_s (54 kpc)", H2["rs"], 54.0, 0.6, rel=False)
check("DSC1R A1 KA1 halo M_b 2e11 z 2.3: r_ta (715 kpc)", H2["rta"], 715.0, 0.6, rel=False)
VB = {}
for ft, stored in (("canonical", (11.324, 11.108, 10.933)), ("alt", (11.432, 11.216, 11.042))):
    for z, s in zip((0.0, 1.0, 2.0), stored):
        check(f"v_stiff boundary log M_b z {z:g} {ft} vs SRJ2 srj2_rc.out", lMb_vstiff(ft, z), s, 0.0015, rel=False)
P(f"[both]  z | log M_b at v_stiff (rival split) can / alt | log M_b* (candidate) can / alt | candidate minus rival can / alt")
for z in (0.0, 0.5, 1.0, 1.2, 1.5, 2.0, 2.3, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0):
    a = [lMb_vstiff(ft, z) for ft in FOOTS]; b = [logMbstar(ft, z) for ft in FOOTS]; VB[z] = a
    P(f"  {z:3.1f} | {a[0]:6.3f} / {a[1]:6.3f} | {b[0]:6.3f} / {b[1]:6.3f} | {b[0] - a[0]:+6.3f} / {b[1] - a[1]:+6.3f}")
P("  (the candidate's switch mass falls by -4 log E(z); the rival's falls by much less; they cross near the z where the two columns are equal)")
for ft in FOOTS:
    zc = brentq(lambda z: logMbstar(ft, z) - lMb_vstiff(ft, z), 0.5, 6.0, xtol=1e-6)
    P(f"  [{ft}] the two boundaries cross at z = {zc:.3f}, log M_b = {logMbstar(ft, zc):.3f}")
P()
# ================================================================ 3. the three disc cells (frozen definitions in SEALED_PREDICTIONS.md)
P("== 3. Disc cells: membership margins 0.15 dex; cell A z 1.8-2.6 above M_b*; cell B z 0.5-1.7 between v_stiff and M_b*; cell C z 3.5-6 between M_b* and v_stiff")
for ft in FOOTS:
    P(f"[{ft}]")
    for z in (1.8, 2.0, 2.3, 2.6):
        P(f"  cell A z {z}: log M_b >= {logMbstar(ft, z) + 0.15:.3f}  (rival v_stiff boundary {lMb_vstiff(ft, z):.3f}: rival also gives the reference here)")
    for z in (0.5, 0.8, 1.0, 1.2, 1.5, 1.7):
        lo, hi = lMb_vstiff(ft, z) + 0.15, logMbstar(ft, z) - 0.15
        P(f"  cell B z {z}: log M_b in [{lo:.3f}, {hi:.3f}] (width {hi - lo:.2f} dex)")
    for z in (3.5, 4.0, 4.5, 5.0, 5.5, 6.0):
        lo, hi = logMbstar(ft, z) + 0.15, lMb_vstiff(ft, z) - 0.15
        P(f"  cell C z {z}: log M_b in [{lo:.3f}, {hi:.3f}] (width {hi - lo:.2f} dex){'  EMPTY' if hi <= lo else ''}")
P()
P("== 4. Fold radius and settled radius at the cells (FLD1; physical kpc); f window [1.25, 2]")
check("FLD1 R_fold canonical log 10.7 z 0 (169)", rfold_kpc("canonical", 0.0, 10.7), 169, 0.6, rel=False)
check("FLD1 R_fold canonical log 10.7 z 2 (58)", rfold_kpc("canonical", 2.0, 10.7), 58, 0.6, rel=False)
check("FLD1 R_fold canonical log 10.45 z 4 (17.2)", rfold_kpc("canonical", 4.0, 10.45), 17.2, 0.06, rel=False)
for ft in FOOTS:
    for (z, lM) in ((0.0, 10.7), (1.2, 11.5), (2.3, 11.45), (2.3, 11.3), (4.5, 10.25), (5.0, 10.25), (5.5, 10.25), (0.0, 13.0), (0.0, 13.3)):
        R = rfold_kpc(ft, z, lM); Rta = rfold_kpc(ft, z, lM, col=3)
        P(f"  [{ft}] z {z} log M_b {lM}: R_fold {R:7.1f}, R_ta {Rta:7.1f}, R_set at f 1.25 / 2: {1.25 * R:7.1f} / {2 * R:7.1f}")
P()
P("== 5. Representative discs (named, not real): V_c^2 / V_bar^2 at 2, 3, 4, 5 R_1/2 under the law, the record's reference halo at A = 1, and baryons alone")
P("   Gamma = g / g_N in the disc plane (thin exponential disc). A_eq = the reference multiple that gives the law's g at that radius.")
P("   d = log10 V_c(law) - log10 V_c(reference, A = 1) (dex). Memberships under the candidate (v*), the rival split (v_stiff, SRJ2 rule) and the unsplit family.")
REP = [("A", 2.3, 11.45, 5.0), ("A", 2.3, 11.70, 5.0), ("B", 1.2, 11.50, 6.0), ("B", 0.9, 11.40, 6.0), ("C", 4.5, 10.25, 1.5), ("C", 5.0, 10.30, 1.2)]
for ft in FOOTS:
    P(f"[{ft}]")
    for cell, z, lM, Rh in REP:
        Mb = 10 ** lM; Hh = ref_halo(ft, Mb, z); a0 = A0[ft]
        cand = "REFERENCE" if lM > logMbstar(ft, z) else "LAW"
        riv = "REFERENCE" if Hh["v_vir"] > VSTIFF[ft] else "LAW (inside f R_fold)"
        Rf = rfold_kpc(ft, z, lM)
        P(f"  cell {cell} z {z} log M_b {lM} R_1/2 {Rh} kpc: v_L {vL(Mb, z) / 1e3:.0f} km/s vs v* {vstar(ft, z) / 1e3:.0f}; FRZ1 v_vir {Hh['v_vir']:.0f} vs v_stiff {VSTIFF[ft]}; "
          f"margin to M_b* {lM - logMbstar(ft, z):+.2f} dex, to v_stiff boundary {lM - lMb_vstiff(ft, z):+.2f} dex")
        P(f"     candidate: {cand}; rival split: {riv}; unsplit: LAW inside R_set = {1.25 * Rf:.1f} to {2 * Rf:.1f} kpc (5 R_1/2 = {5 * Rh:.1f} kpc); "
          f"halo c {Hh['c']:.2f}, r_s {Hh['rs']:.1f} kpc, r_ta {Hh['rta']:.0f} kpc, X {Hh['X']:.2f}")
        for m in (2, 3, 4, 5):
            r = m * Rh; gN = float(gN_disc(Mb, Rh, r)); gl = float(glaw(gN, a0)); gh = float(g_ref_halo(Hh, Mb, r))
            P(f"     {m} R_1/2 ({r:5.1f} kpc): g_N/a0 {gN / a0:6.3f}; Gamma law {gl / gN:6.3f}, reference A=1 {(gN + gh) / gN:6.3f}, baryons 1; "
              f"A_eq {(gl - gN) / gh:6.3f}; d {0.5 * math.log10(gl / (gN + gh)):+.4f} dex")
P()
P("== 6. Strong lenses and the forest (pointers; numbers for the kill-only conditions)")
for ft in FOOTS:
    P(f"  [{ft}] log M_b* at z_l 0.66 (EUC1's median lens z): {logMbstar(ft, 0.66):.3f}; at z_l 1.09 / 1.72 (LNJ1's 26 above, canonical): {logMbstar(ft, 1.09):.3f} / {logMbstar(ft, 1.72):.3f}")
    P(f"  [{ft}] forest switch M200c (Msun/h) at z 2.2 / 2.6 / 3.0 / 3.4 / 3.8 / 4.4: " + " / ".join(f"{M200c_switch(ft, z) * hh:.2e}" for z in (2.2, 2.6, 3.0, 3.4, 3.8, 4.4)))
P()
n = len(CHK); P(f"checks: {sum(CHK)} of {n} pass")
P("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
sys.exit(0 if all(CHK) else 1)
