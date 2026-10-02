#!/usr/bin/env python3
"""CFG268 -- conditioning ESTIMATES for z ~ 2.5-4 kinematic samples and single objects.

SCOPING ONLY. No a0 is computed here, no law is fitted, no kernel is inverted.
Every number printed is an ESTIMATE of the CFG240 design variable y = g/a0 at the
radius where the source paper quotes a velocity, from the paper's own published
numbers (transcribed below with their table/section). Two quantities per row:

  y_obs = V^2 / (R a0)          -- law-free, from the published V and R
  y_bar = g_bar(R) / a0         -- from the published stellar (and, where stated,
                                   gas) mass and size, thin exponential disc
                                   (Freeman 1970) unless a row says otherwise

Both footings of a0 are printed: canonical 9.3603e-11 and alternative 1.131e-10 m/s^2.
D_* = g_obs / g_bar(stars only). Stars-only baryons are a LOWER limit on the baryons,
so D_* is an UPPER limit on g_obs/g_bar.

Controls (exit 1 if any fails): C1 Freeman peak V^2 Rd/(G M) = 0.38705 at R = 2.15 Rd;
C2 far-field Newtonian limit (g_disc R^2/(G M) -> 1 at R = 60 Rd); C3 KDS isolated-field
sample has 32 rows, 13 rotation-dominated (Turner+17 Table 3 'RD'); C4 AMAZE/LSD has
11 rotating objects (Gnerucci+11 Table 3); C5 the KDS x AMAZE coordinate cross-match finds
at least one pair with |dz| < 0.01 (a repeat measurement of the same galaxy).
MUTATE=1 replaces the thin disc by a point mass (C1 must fail); its output is kept as
cfg268_y_estimates_MUTATE1.out (run commands in SCOPING.md).
"""
import math, os, sys
import numpy as np
from scipy.special import i0, i1, k0, k1

G = 6.674e-11
MSUN = 1.989e30
KPC = 3.0857e19
A0 = {"canonical": 9.3603e-11, "alt": 1.131e-10}
MUTATE = int(os.environ.get("MUTATE", "0"))


def g_disc(R_kpc, M_msun, Rd_kpc):
    """Midplane radial acceleration of a razor-thin exponential disc (m/s^2)."""
    if MUTATE == 1:
        return G * M_msun * MSUN / (R_kpc * KPC) ** 2
    yy = R_kpc / (2.0 * Rd_kpc)
    sig0 = M_msun * MSUN / (2.0 * math.pi * (Rd_kpc * KPC) ** 2)
    v2 = 4.0 * math.pi * G * sig0 * (Rd_kpc * KPC) * yy ** 2 * (i0(yy) * k0(yy) - i1(yy) * k1(yy))
    return v2 / (R_kpc * KPC)


def g_obs(V_kms, R_kpc):
    return (V_kms * 1e3) ** 2 / (R_kpc * KPC)


def g_sph(M_msun, R_kpc):
    return G * M_msun * MSUN / (R_kpc * KPC) ** 2


def ys(g):
    return g / A0["canonical"], g / A0["alt"]


def hms(ra, dec):
    h, m, s = [float(x) for x in ra.split(":")]
    sg = -1 if dec.strip().startswith("-") else 1
    d, dm, ds = [abs(float(x)) for x in dec.split(":")]
    return 15 * (h + m / 60 + s / 3600), sg * (d + dm / 60 + ds / 3600)


fails = []

# ---------------- controls on the disc formula ----------------
Rd = 1.0
M = 1e10
Rpk = 2.15 * Rd
pk = g_disc(Rpk, M, Rd) * (Rpk * KPC) * (Rd * KPC) / (G * M * MSUN)
c1 = abs(pk - 0.38705) < 2e-3
far = g_disc(60 * Rd, M, Rd) * (60 * Rd * KPC) ** 2 / (G * M * MSUN)
c2 = abs(far - 1.0) < 2e-3
print("CFG268 conditioning estimates (scoping; no a0 computed)%s" % ("  [MUTATE=%d]" % MUTATE if MUTATE else ""))
print("C1 Freeman peak V^2 Rd/(GM) at 2.15 Rd = %.5f (expect 0.38705): %s" % (pk, "PASS" if c1 else "FAIL"))
print("C2 far field g R^2/(GM) at 60 Rd = %.5f (expect 1): %s" % (far, "PASS" if c2 else "FAIL"))
if not c1: fails.append("C1")
if not c2: fails.append("C2")

# ---------------- KDS (Turner+17, arXiv:1704.06263) ----------------
# Table 2 (id, RA, Dec, z, log M*, R_1/2 kpc) and Table 3 (V_C, sigma_int, class) of the
# isolated field sample. V_C is the beam-smearing-corrected model rotation at 2 R_1/2.
KDS = [
    ("b012141_012208", "03:32:23.290", "-27:51:57.348", 3.471, 9.8, 1.57, 93, 63, "RD"),
    ("b15573", "03:32:27.638", "-27:50:59.676", 3.583, 9.8, 0.52, 81, 84, "DD"),
    ("bs006516", "03:32:14.791", "-27:50:46.500", 3.215, 9.8, 1.91, 61, 45, "RD"),
    ("bs006541", "03:32:14.820", "-27:52:04.620", 3.475, 10.1, 1.83, 65, 83, "DD"),
    ("bs008543", "03:32:17.890", "-27:50:50.136", 3.474, 10.5, 1.59, 111, 71, "RD"),
    ("bs009818", "03:32:19.810", "-27:53:00.852", 3.706, 9.7, 1.24, 84, 79, "RD"),
    ("bs014828", "03:32:26.760", "-27:52:25.896", 3.562, 9.7, 1.61, 46, 88, "DD"),
    ("bs016759", "03:32:29.141", "-27:48:52.596", 3.602, 9.9, 0.87, 110, 57, "RD"),
    ("lbg_20", "03:32:41.244", "-27:52:20.676", 3.225, 9.5, 1.28, 56, 40, "RD"),
    ("lbg_24", "03:32:39.754", "-27:39:56.628", 3.279, 9.6, 1.27, 42, 51, "DD"),
    ("lbg_25", "03:32:29.189", "-27:40:22.476", 3.322, 9.4, 1.18, 33, 41, "DD"),
    ("lbg_30", "03:32:42.854", "-27:42:06.300", 3.419, 10.0, 0.95, 66, 77, "DD"),
    ("lbg_32", "03:32:34.399", "-27:41:24.324", 3.417, 9.9, 1.88, 121, 76, "RD"),
    ("lbg_38", "03:32:22.474", "-27:44:38.436", 3.488, 9.9, 0.92, 97, 53, "RD"),
    ("lbg_91", "03:32:27.202", "-27:41:51.756", 3.170, 9.8, 0.89, 91, 71, "RD"),
    ("lbg_94", "03:32:28.949", "-27:44:11.688", 3.367, 9.9, 1.16, 34, 55, "DD"),
    ("lbg_105", "03:32:24.005", "-27:52:16.140", 3.092, 9.3, 1.72, 32, 59, "DD"),
    ("lbg_109", "03:32:20.935", "-27:43:46.344", 3.600, 9.7, 1.98, 53, 91, "DD"),
    ("lbg_111", "03:32:42.497", "-27:45:51.696", 3.609, 9.7, 0.64, 58, 81, "DD"),
    ("lbg_112", "03:32:17.134", "-27:42:17.784", 3.617, 9.6, 0.46, 63, 78, "DD"),
    ("lbg_113", "03:32:35.957", "-27:41:49.956", 3.622, 9.6, 0.87, 41, 108, "DD"),
    ("lbg_124", "03:32:33.324", "-27:50:07.332", 3.794, 9.0, 0.78, 32, 46, "DD"),
    ("n3_006", "22:17:24.859", "00:11:17.620", 3.069, 10.5, 2.52, 81, 125, "DD"),
    ("n3_009", "22:17:28.330", "00:12:11.600", 3.069, 8.7, 1.06, 49, 48, "RD"),
    ("n_c3", "22:17:32.585", "00:10:57.180", 3.096, 9.8, 0.56, 51, 72, "DD"),
    ("lab18", "22:17:28.850", "00:07:51.800", 3.101, 8.2, 0.46, 41, 62, "DD"),
    ("lab25", "22:17:22.603", "00:15:51.330", 3.067, 8.4, 2.18, 48, 49, "DD"),
    ("ssa22a-d3", "22:17:32.453", "00:11:32.920", 3.069, 9.7, 1.78, 109, 93, "RD"),
    ("ssa22b-c20", "22:17:48.845", "00:10:13.840", 3.196, 9.5, 1.59, 139, 48, "RD"),
    ("ssa22b-d5", "22:17:35.808", "00:06:10.340", 3.175, 10.2, 3.30, 57, 23, "RD"),
    ("ssa22b-d9", "22:17:22.303", "00:08:04.130", 3.084, 10.1, 0.50, 46, 73, "DD"),
    ("ssa22b-md25", "22:17:41.690", "00:06:20.460", 3.304, 8.6, 1.39, 57, 75, "DD"),
]
n_rd = sum(1 for r in KDS if r[8] == "RD")
c3 = len(KDS) == 32 and n_rd == 13
print("C3 KDS rows = %d, RD = %d (expect 32, 13): %s" % (len(KDS), n_rd, "PASS" if c3 else "FAIL"))
if not c3: fails.append("C3")

print("\n== KDS isolated field sample (Turner+17): ESTIMATES at R = 2 R_1/2 (where V_C is quoted) ==")
print("   R_d = R_1/2 / 1.678; stars only (no gas in the paper). y columns: canonical / alt footing.")
print("   %-15s %5s %5s %5s %5s %4s %4s | %12s %12s %16s %7s" % ("id", "z", "logM*", "R12", "R", "VC", "sig", "y_bar*", "y_obs(rot)", "y_obs(V2+3.35s2)", "D*(rot)"))
kds_rows = []
for (nm, ra, de, z, lm, r12, vc, sg, cl) in KDS:
    R = 2 * r12
    gb = g_disc(R, 10 ** lm, r12 / 1.678)
    go = g_obs(vc, R)
    gp = ((vc * 1e3) ** 2 + 3.35 * (sg * 1e3) ** 2) / (R * KPC)
    yb = ys(gb); yo = ys(go); yp = ys(gp)
    kds_rows.append((nm, z, yb[0], yo[0], yp[0], go / gb, cl))
    print("   %-15s %5.3f %5.1f %5.2f %5.2f %4d %4d | %5.2f / %4.2f %5.2f / %4.2f %6.2f / %5.2f %7.2f %s" %
          (nm, z, lm, r12, R, vc, sg, yb[0], yb[1], yo[0], yo[1], yp[0], yp[1], go / gb, cl))
yb_all = np.array([r[2] for r in kds_rows]); yo_all = np.array([r[3] for r in kds_rows]); yp_all = np.array([r[4] for r in kds_rows])
D_all = np.array([r[5] for r in kds_rows])
rd = np.array([r[6] == "RD" for r in kds_rows])
print("   SUMMARY (canonical footing): y_bar* range %.2f-%.2f (median %.2f); y_obs(rot) %.2f-%.2f (median %.2f);"
      " y_obs with pressure term %.2f-%.2f (median %.2f)" % (yb_all.min(), yb_all.max(), np.median(yb_all), yo_all.min(), yo_all.max(),
                                                            np.median(yo_all), yp_all.min(), yp_all.max(), np.median(yp_all)))
print("   rows with y_bar* < 0.3: %d of 32 (RD only: %d of 13); rows with y_bar* < 0.1: %d" %
      ((yb_all < 0.3).sum(), (yb_all[rd] < 0.3).sum(), (yb_all < 0.1).sum()))
print("   D*(rot) < 1 (stars alone exceed the rotation-only acceleration): %d of 32; with the pressure term the median ratio"
      " g_obs/g_bar* rises from %.2f to %.2f" % ((D_all < 1).sum(), np.median(D_all), np.median(yp_all / yb_all)))
print("   pressure term 3.35 sigma^2 exceeds V_C^2 in %d of 32 rows" % sum(1 for r in KDS if 3.35 * r[7] ** 2 > r[6] ** 2))

# ---------------- AMAZE/LSD (Gnerucci+11, arXiv:1007.4180) ----------------
# Table 1 (RA, Dec, z), Table 3 (log Mdyn, r_e = exponential scale radius, Vmax), Table 4 (log M*).
# flags: 'lim' = limit in Table 3; 'unc' = parameter unconstrained (Table 3 note 5).
AMZ = [
    ("SSA22a-M38", "22:17:17.7", "00:19:00.7", 3.294, 11.34, 2.574, 346, 11.01, ""),
    ("SSA22a-C16", "22:17:32.0", "00:13:16.1", 3.068, 10.31, 1.730, 129, 10.83, ""),
    ("CDFS-2528", "03:32:45.5", "-27:53:33.3", 3.688, 10.71, 1.644, 197, 9.76, "lim"),
    ("SSA22a-D17", "22:17:18.9", "00:18:16.8", 3.087, 10.70, 1.214, 260, 9.40, ""),
    ("CDFA-C9", "00:53:13.7", "12:32:11.1", 3.212, 9.93, 0.821, 129, 10.18, ""),
    ("CDFS-9313", "03:32:17.2", "-27:47:54.4", 3.654, 9.29, 0.713, 67, 9.52, "unc"),
    ("CDFS-9340", "03:32:17.2", "-27:47:53.4", 3.658, 10.3, 1.420, 151, 9.09, "unc"),
    ("3C324-C3", "15:49:47.1", "21:27:05.0", 3.289, 10.12, 2.5, 86, 9.95, ""),
    ("CDFS-14411", "03:32:20.9", "-27:43:46.3", 3.599, 9.59, 1.240, 69, 9.51, ""),
    ("CDFS-16767", "03:32:35.9", "-27:41:49.9", 3.624, 10.93, 0.362, 623, 10.06, "unc"),
    ("Q0302-C131", "03:04:35.0", "-00:11:18.3", 3.240, 9.99, 0.466, 117, 10.09, "lim"),
]
c4 = len(AMZ) == 11
print("\nC4 AMAZE/LSD rotating objects = %d (expect 11): %s" % (len(AMZ), "PASS" if c4 else "FAIL"))
if not c4: fails.append("C4")
print("\n== AMAZE/LSD rotating objects (Gnerucci+11): ESTIMATES at R = 2.2 r_e (peak of an exponential disc curve) ==")
print("   %-12s %5s %6s %5s %5s %5s | %12s %12s %7s %s" % ("name", "z", "logM*", "r_e", "R", "Vmax", "y_bar*", "y_obs", "D*", "flag"))
amz_y = []
for (nm, ra, de, z, lmd, re, vm, lms, fl) in AMZ:
    R = 2.2 * re
    gb = g_disc(R, 10 ** lms, re)
    go = g_obs(vm, R)
    yb = ys(gb); yo = ys(go)
    amz_y.append((yb[0], yo[0]))
    print("   %-12s %5.3f %6.2f %5.2f %5.2f %5d | %5.2f / %4.2f %5.2f / %5.2f %7.2f %s" % (nm, z, lms, re, R, vm, yb[0], yb[1], yo[0], yo[1], go / gb, fl))
a = np.array(amz_y)
print("   SUMMARY (canonical): y_bar* %.2f-%.2f (median %.2f); y_obs %.2f-%.2f (median %.2f)" % (a[:, 0].min(), a[:, 0].max(), np.median(a[:, 0]), a[:, 1].min(), a[:, 1].max(), np.median(a[:, 1])))

# ---------------- KDS x AMAZE cross-match (repeat measurements) ----------------
print("\n== KDS x AMAZE/LSD coordinate cross-match: every Gnerucci+11 Table 1 row in the two KDS fields (CDFS = GOODS-S, SSA22)"
      " against the 32 KDS isolated-field rows, tolerance 1.5 arcsec (AMAZE RA is given to 0.1 s = 1.5 arcsec) ==")
AMZ_ALL_CDFS = [  # Table 1 rows in CDFS and SSA22 that are NOT among the 11 rotators
    ("CDFS-11991", "03:32:42.4", "-27:45:51.6", 3.661), ("CDFS-5161", "03:32:22.6", "-27:51:18.0", 3.660),
    ("CDFS-6664", "03:32:33.3", "-27:50:07.4", 3.797), ("CDFS-4414", "03:32:23.2", "-27:51:57.9", 3.471),
    ("CDFS-4417", "03:32:23.3", "-27:51:56.8", 3.473), ("CDFS-12631", "03:32:18.1", "-27:45:19.0", 3.709),
    ("CDFS-13497", "03:32:36.3", "-27:44:34.6", 3.413), ("CDFS-16272", "03:32:17.1", "-27:42:17.8", 3.619),
    ("SSA22a-aug96M16", "22:17:30.9", "00:13:10.7", 3.292), ("SSA22a-C36", "22:17:46.1", "00:16:43.0", 3.063),
    ("SSA22b-C5", "22:17:47.1", "00:04:25.7", 3.117), ("SSA22a-C6", "22:17:40.9", "00:11:26.0", 3.097),
    ("SSA22a-M4", "22:17:40.9", "00:11:27.9", 3.098), ("SSA22a-C30", "22:17:19.3", "00:15:44.7", 3.104),
]
pairs = []
for (an, ara, ade, az, *_rest) in [r[:4] for r in AMZ] + AMZ_ALL_CDFS:
    a_ra, a_de = hms(ara, ade)
    for r in KDS:
        k_ra, k_de = hms(r[1], r[2])
        sep = 3600 * math.hypot((a_ra - k_ra) * math.cos(math.radians(k_de)), a_de - k_de)
        if sep < 1.5:
            pairs.append((an, r[0], sep, az, r[3]))
kd = {r[0]: r for r in KDS}
am = {r[0]: r for r in AMZ}
for p in pairs:
    extra = ""
    if p[0] in am and p[1] in kd:
        extra = "  V: AMAZE Vmax %d%s vs KDS V_C %d (sigma_int %d, %s)" % (am[p[0]][6], " [" + am[p[0]][8] + "]" if am[p[0]][8] else "",
                                                                         kd[p[1]][6], kd[p[1]][7], kd[p[1]][8])
    elif p[1] in kd:
        extra = "  (AMAZE: not classified rotating; KDS V_C %d, sigma_int %d, %s)" % (kd[p[1]][6], kd[p[1]][7], kd[p[1]][8])
    print("   %-15s <-> %-15s sep %.2f\"  z %.3f vs %.3f  |dz| %.3f%s" % (p[0], p[1], p[2], p[3], p[4], abs(p[3] - p[4]), extra))
good = [p for p in pairs if abs(p[3] - p[4]) < 0.01]
c5 = len(good) >= 1
print("C5 repeat-measurement pairs with |dz| < 0.01: %d: %s" % (len(good), "PASS" if c5 else "FAIL"))
if not c5: fails.append("C5")

# ---------------- single objects ----------------
print("\n== Single objects: ESTIMATES (published V, R and masses; see SCOPING.md for every source) ==")
print("   y_obs = V^2/(R a0) or G M_dyn/(R^2 a0) as stated; y_bar from the stated baryons and geometry.")


def row(name, note, go, gbs):
    yo = ys(go)
    s = "   %-26s y_obs %6.2f / %5.2f" % (name, yo[0], yo[1])
    for lab, gb in gbs:
        yb = ys(gb)
        s += " | y_bar[%s] %5.2f / %5.2f (D %.2f)" % (lab, yb[0], yb[1], go / gb)
    print(s)
    if note:
        print("      " + note)


# ADF22.1 (= ALPAKA 23): V_rot 530 at 2 r_e = 14 kpc (Umehata+25); outermost ring ~14 kpc (Rizzo+26).
# M*,SED = 10^11.4 (Umehata+25), r_e(F444W) = 7.0 kpc (Umehata+25; Rizzo+26 global 6.2);
# M_gas = 2.0e11 (alpha_CO/2.5) from JVLA CO(1-0) (Umehata+25). Gas assumed to share the stellar scale (assumption).
Ms = 10 ** 11.4; Rd = 7.0 / 1.678
gs = g_disc(14.0, Ms, Rd)
row("ADF22.1 z3.09 R=14", "stars r_e 7.0 kpc; gas CO(1-0) with alpha_CO 0.8 / 2.5 / 4.6 at the same scale (assumption)",
    g_obs(530, 14.0), [("*", gs)] + [("*+g a%.1f" % al, gs + g_disc(14.0, 2.0e11 * al / 2.5, Rd)) for al in (0.8, 2.5, 4.6)])
gs2 = g_disc(14.0, Ms, 6.2 / 1.678)
row("ADF22.1 z3.09 R=14 (re6.2)", "Rizzo+26 global r_e 6.2 kpc, stars only", g_obs(530, 14.0), [("*", gs2)])
row("ADF22.1 z3.09 R=4", "inner ring for the y span (V taken as 500 km/s, read from the flat curve; ESTIMATE)", g_obs(500, 4.0),
    [("*", g_disc(4.0, Ms, Rd)), ("*+g a2.5", g_disc(4.0, Ms, Rd) + g_disc(4.0, 2.0e11, Rd))])

# Big Wheel: V_rot ~314 at the outermost radius, R_obs ~ 10 kpc (Quadri+26, arXiv:2605.04144);
# M* = 10^11.37 (SED, W25) or 10^11.00 (their dynamical posterior); r_half-mass 6.3 kpc; gas 10^10.76, R_d,gas 3.81.
g_gas = g_disc(10.0, 10 ** 10.76, 3.81)
row("Big Wheel z3.25 R=10", "i = 38 (+8/-10) deg: from sin i alone V moves +31%/-14% and y_obs +72%/-27%",
    g_obs(314, 10.0), [("*SED", g_disc(10.0, 10 ** 11.37, 6.3 / 1.678)), ("*SED+g", g_disc(10.0, 10 ** 11.37, 6.3 / 1.678) + g_gas),
                        ("*dyn+g", g_disc(10.0, 10 ** 11.00, 3.96) + g_gas)])

# PKS 0529-549: flat V ~280 (outer rings; 310 in Lelli+18) out to 3.3 kpc (Lin+25, arXiv:2411.08958).
# Gas 7.3e10 (CO(4-3), Huang+24 as quoted in Lin+25), gas R_e 2.57 kpc (Sersic n 0.52 -> exponential approx);
# stars: SED 3e11 (De Breuck+10), dynamical stars-only upper limit 1.1e11, CIGALE preliminary 0.4-1.2e11;
# stellar R_e 3.0 kpc with n ~5.6: modelled here as a Hernquist sphere (a = R_e/1.815), an assumption.
def g_hern(M, Re, R):
    aa = Re / 1.815
    return G * M * MSUN * (R / (R + aa)) ** 2 / (R * KPC) ** 2
ggas = g_disc(3.3, 7.3e10, 2.57 / 1.678)
row("PKS0529-549 z2.57 R=3.3", "V 280 (310 gives y_obs x1.23); stars Hernquist R_e 3.0 kpc",
    g_obs(280, 3.3), [("gas", ggas), ("g+*0.4e11", ggas + g_hern(0.4e11, 3.0, 3.3)), ("g+*1.1e11", ggas + g_hern(1.1e11, 3.0, 3.3)),
                      ("g+*3e11", ggas + g_hern(3e11, 3.0, 3.3))])

# SDP.81: V_rot 320 +- 20 (i = 40 +- 5) within 1.5 kpc, M_dyn 3.5e10 (Swinbank+15); R_CO ~6 kpc, M_dyn ~8e10 (Rybak+15b).
row("SDP.81 z3.04 R=1.5", "gas 2.7-3.9e10 (CO(1-0) and dust) and M* 6.6e10 offset by 1.5 kpc: baryons ~ dynamics", g_obs(320, 1.5), [])
row("SDP.81 z3.04 R=6", "Rybak+15b: M_dyn ~8e10 within R_CO ~6 kpc", g_sph(8e10, 6.0), [])

# MQN01-QC (Pensabene+25): M_dyn 2.5e11 within 4.1 kpc; M* 9.1e10 within 2.3 kpc; M_H2 6e10 (alpha_CO/1.7).
row("MQN01-QC z3.25 R=4.1", "rings oversampled 1.6x (not independent)", g_sph(2.5e11, 4.1), [])

# GN20 (z 4.055, just outside the band): v_c(R_e = 3.6) = 496, v_c,max = 574 at 6.8 kpc (Ubler+24, i fitted);
# M* 1.1-2.3e11 (Tan+14 etc., as quoted), disc R_e 3.6 kpc (Colina+23); M_H2 1.3e11 (alpha 0.8, Hodge+12).
row("GN20 z4.06 R=6.8", "inclination 30-45 deg in the literature: V ranges 442-646", g_obs(574, 6.8),
    [("*1.1e11+g", g_disc(6.8, 1.1e11, 3.6 / 1.678) + g_disc(6.8, 1.3e11, 3.6 / 1.678))])

# GA-NIFS GS_4891 (z 3.70): v_rot ~90 km/s at 2.2 kpc, M_dyn ~1.7e10; M* within the kinematic region 5.5e9 (Rodriguez del Pino+24).
row("GS_4891 z3.70 R=2.2", "one radius; no gas; M* inside the region put inside 2.2 kpc (upper bound on g_bar)", g_obs(90, 2.2),
    [("* sph", g_sph(5.5e9, 2.2))])

# Cosmic Eye (z 3.074): v sin i = 55 +- 7 to +-2 kpc, sigma 54 (Stark+08 via Coppin+07); M_dyn (8+-2)e9 csc^2 i within 2 kpc;
# M* ~(6+-2)e9; M_gas (2.4+-0.4)e9 (CO(3-2), Coppin+07).
row("Cosmic Eye z3.07 R=2", "g_obs here uses M_dyn sin^2 i = 8e9 (i = 90 deg; a LOWER bound); baryons all inside 2 kpc (UPPER bound)",
    g_sph(8e9, 2.0), [("*+g sph", g_sph(6e9 + 2.4e9, 2.0))])

# arc&core (z 3.2, Nesvadba+06): M_dyn 10^9.3 within 1 kpc.
row("arc&core z3.2 R=1", "inner kpc only; no gas or stellar mass in the abstract", g_sph(10 ** 9.3, 1.0), [])

# References just below the band
row("Cosmic Eyelash z2.33 R=2.5", "reference (below band): V 320, M_dyn 6.0e10 within 2.5 kpc", g_obs(320, 2.5), [])
row("J0901 z2.26 R=4.25", "reference (below band): v_circ ~260 at r_1/2 ~4.25 kpc (Sharon+19)", g_obs(260, 4.25), [])
print("   (CFG229 record, for comparison: ALESS 122.1 at y = 4.8, the only class-M root; the ALPAKA discs at y = 26-157.)")

print("\nRESULT: %s" % ("ALL CONTROLS PASS" if not fails else "FAILED: " + ", ".join(fails)))
sys.exit(1 if fails else 0)
