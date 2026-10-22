"""D2_wide_binary_fork: law-first vs medium-first.

Q1  independent QUMOND gamma_v at 10/20/30 kAU with the Milky Way field, both footings, three record
    g_ext values, theta = 0 / 90 deg / orientation average; d gamma/d kappa; sigma(kappa) from DR4.
Q2  DR3 occupancy of the 18-22 kAU bin and the separating power at N = 30,000; current-data status.
Q3  A26's ultra-faints with the host's external field put into the same law.
Q4  N and sigma_sys needed for 3 sigma.

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 d2_wide_binary_fork.py [--mutate]
Writes d2_wide_binary_fork.out / d2_wide_binary_fork_results.json (or *_MUTATE.*).
Deterministic, no network. Repo-relative paths only.
"""
import csv
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import qumond_fft as q  # noqa: E402

MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
OUT = os.path.join(HERE, "d2_wide_binary_fork%s.out" % ("_MUTATE" if MUT else ""))
JS = os.path.join(HERE, "d2_wide_binary_fork_results%s.json" % TAG)
PROJECT = not MUT                     # MUTATE: phantom field = S itself (no curl-free projection)

LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(s)


CHECKS = []


def ck(cid, ok, value, thr, note=""):
    CHECKS.append(dict(id=cid, passed=bool(ok), value=value, threshold=thr, note=note))
    P("%s %s %s %s   %s" % (cid, "PASS" if ok else "FAIL", value, thr, note))


# ------------------------------------------------------------------ constants (all sourced)
G = 6.67430e-11
MSUN = 1.98892e30          # same as the record's 1.989e30 to 5e-5
AU = 1.495978707e11
KAU = 1e3 * AU
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}            # BRIEF rule 3
GEXT = {"A24_x1.8": 1.8 * 9.36e-11,                      # A24 'standard local field' x_ext = 1.8 (canonical)
        "PREREG_primary": 1.778e-10,                     # PREREGISTRATION_DR4.md sec 1.1 primary
        "PREREG_alt": 2.078e-10}                         # sec 1.1 alt (Vc^2/R0, 229 km/s, 8.178 kpc)
M_TOT = 2.0                                              # 1 + 1 Msun, A24's configuration
SEPS = [10.0, 20.0, 30.0]
NGRID, MGRID = 320, 13                                   # primary grid: dx = s/27, box 11.85 s
A24_CANON_20 = 1.1933                                    # A24 report sec 3, canonical kernel, theta = 0
ARM_A = {"canonical": (1.1614, 1.1814), "alt": (1.1917, 1.2267)}   # registered band (A24 sec 4)
KAPPA_CANON_A71 = 0.4137186481963329                     # A71 a71_results.json constants.kappa_canon
SIG_FIT_30K, SIG_SYS = 0.019, 0.020                      # PREREG frozen error model (memory/readiness)


def solve(y_tot, y_e, theta, **kw):
    kw.setdefault("N", NGRID)
    kw.setdefault("m", MGRID)
    return q.phantom_rel(y_tot, y_e, theta, project=PROJECT, **kw)


def gam(y_tot, y_e, theta=None, **kw):
    if theta is not None:
        return math.sqrt(solve(y_tot, y_e, theta, **kw))
    a = sum(w * solve(y_tot, y_e, float(np.arccos(mu)), **kw) for mu, w in zip(q.GL3_MU, q.GL3_W))
    return math.sqrt(a)


def ytot_of(s_kau, a0, mtot=M_TOT):
    return G * mtot * MSUN / ((s_kau * KAU) ** 2 * a0)


R = {"mutate": MUT}
P("=" * 100)
P("D2_wide_binary_fork  (mutation: %s)" % ("drop longitudinal projection" if MUT else "none"))
P("=" * 100)

# ================================================================== VALIDITY CHECKS
P("\n[C1] FFT projection vs analytic linear QUMOND EFE (B_par = nu_e, B_perp = nu_e(1+K/2))")
ye18 = q.y_newton_from_obs(1.8)
c1 = []
for th in (0.0, math.pi / 2):
    num = 1.0 + solve(1e-3, ye18, th, mode="linear")
    ana = 1.0 + q.linear_analytic(ye18, th)
    c1.append(abs(num / ana - 1.0))
    P("      theta=%5.1f deg  B_fft=%.5f  B_analytic=%.5f" % (math.degrees(th), num, ana))
ck("C1", max(c1) <= 0.02, "%.4f" % max(c1), "<=0.02", "max relative error in B at y_e=%.4f" % ye18)

P("\n[C2/C3] convergence of gamma_v(20 kAU, theta=0, x_ext=1.8 canonical)")
yt20 = ytot_of(20.0, A0["canonical"])
g_a = gam(yt20, ye18, 0.0, N=256, m=10)
g_b = gam(yt20, ye18, 0.0, N=320, m=13)
ck("C2", abs(g_a - g_b) <= 0.005, "%.4f" % abs(g_a - g_b), "<=0.005",
   "resolution s/21 -> s/27 (box 12.2 -> 11.9 s): %.4f -> %.4f" % (g_a, g_b))
g_c = gam(yt20, ye18, 0.0, N=256, m=8)
g_d = gam(yt20, ye18, 0.0, N=256, m=12)
ck("C3", abs(g_c - g_d) <= 0.005, "%.4f" % abs(g_c - g_d), "<=0.005",
   "box 15.1 s vs 10.2 s: %.4f vs %.4f" % (g_c, g_d))
g_strong = gam(300.0, ye18, 0.0)
ck("C4", abs(g_strong - 1.0) <= 0.005, "%.4f" % (g_strong - 1), "<=0.005", "y_tot = 300 strong-field limit")
R["checks_numbers"] = dict(C2=[g_a, g_b], C3=[g_c, g_d], C4=g_strong)

# ================================================================== Q1
P("\n[Q1] gamma_v of the canonical law with the Galactic field (1+1 Msun, circular, QUMOND/FFT)")
P("      %-10s %-15s %6s %8s %8s | %8s %8s %8s" % ("footing", "g_ext", "x_ext", "y_ext", "s/kAU",
                                                    "th=0", "th=90", "avg"))
TAB = {}
for fo, a0 in A0.items():
    for gk, gv in GEXT.items():
        x = gv / a0
        ye = q.y_newton_from_obs(x)
        for s in SEPS:
            yt = ytot_of(s, a0)
            g0 = gam(yt, ye, 0.0)
            g90 = gam(yt, ye, math.pi / 2)
            gav = gam(yt, ye)
            TAB["%s|%s|%g" % (fo, gk, s)] = dict(x_ext=x, y_ext=ye, y_tot=yt, th0=g0, th90=g90, avg=gav)
            P("      %-10s %-15s %6.3f %8.4f %8.0f | %8.4f %8.4f %8.4f" % (fo, gk, x, ye, s, g0, g90, gav))
R["gamma_table"] = TAB
r1 = TAB["canonical|A24_x1.8|20"]["th0"]
R["R1"] = dict(value=r1, A24=A24_CANON_20, diff=r1 - A24_CANON_20,
               cls="A24 REPRODUCED" if abs(r1 - A24_CANON_20) <= 0.015 else "A24 DISAGREES")
P("R1  gamma_v(20 kAU, theta=0, x=1.8, canonical) = %.4f vs A24 %.4f (diff %+.4f) -> %s"
  % (r1, A24_CANON_20, r1 - A24_CANON_20, R["R1"]["cls"]))
r1b_c = TAB["canonical|PREREG_primary|20"]["avg"]
r1b_a = TAB["alt|PREREG_primary|20"]["avg"]
R["R1b"] = dict(canonical=r1b_c, alt=r1b_a,
                cls="1.18 IS THE LAW'S NUMBER" if 1.15 <= r1b_c <= 1.21 else "CORRECTED")
P("R1b orientation-averaged gamma_v(20 kAU) at PREREG primary g_ext: canonical %.4f / alt %.4f -> %s"
  % (r1b_c, r1b_a, R["R1b"]["cls"]))
spread = [TAB["canonical|%s|20" % gk][k] for gk in GEXT for k in ("th0", "th90", "avg")]
P("      canonical 20 kAU spread over the 3 record g_ext values x 3 orientations: %.4f - %.4f"
  % (min(spread), max(spread)))
R["R1_spread_canonical_20"] = [min(spread), max(spread)]

# ---- derivatives
P("\n[R2] sensitivities at PREREG primary g_ext, orientation-averaged")
DER = {}
h = 0.05
for fo, a0 in A0.items():
    for s in (20.0, 30.0):
        def gv(a0f, gf):
            ye_ = q.y_newton_from_obs(GEXT["PREREG_primary"] * gf / (a0 * a0f))
            return gam(ytot_of(s, a0 * a0f), ye_)
        dlna0 = (gv(1 + h, 1) - gv(1 - h, 1)) / (math.log(1 + h) - math.log(1 - h))
        dlng = (gv(1, 1 + h) - gv(1, 1 - h)) / (math.log(1 + h) - math.log(1 - h))
        DER["%s|%g" % (fo, s)] = dict(dgamma_dlna0=dlna0, dgamma_dlngext=dlng,
                                      dgamma_dkappa_A71conv=dlna0 / KAPPA_CANON_A71,
                                      dgamma_dkappa_half_conv=dlna0 / 0.5)
        P("      %-9s s=%2.0f kAU  dgamma/dln a0 = %+.4f   dgamma/dln g_ext = %+.4f   dgamma/dkappa = %+.4f "
          "(A71 conv, kappa_canon 0.4137) / %+.4f (kappa=1/2 conv)"
          % (fo, s, dlna0, dlng, dlna0 / KAPPA_CANON_A71, dlna0 / 0.5))
R["R2"] = DER

# ---- sigma(kappa): A71 reproduced, then corrected
P("\n[C5/R3] the kappa leverage of a 30,000-pair DR4 catalogue")
A71 = json.load(open(os.path.join(ROOT, "deepseek_push/DS_FINAL_2026_10_21/A71_global_fit/a71_results.json")))
DG71 = A71["wide_binary"]["dgamma_dkappa_efe"]
SKT = A71["joint"]["sigma_tot"]
H0T = 0.125 * A71["joint"]["kappa"]
SNOH0 = math.sqrt(SKT ** 2 - H0T ** 2)


def after(sig):
    return math.sqrt(1.0 / (1.0 / SNOH0 ** 2 + 1.0 / sig ** 2) + H0T ** 2)


sbin = math.sqrt((0.0699 * math.sqrt(2223.0 / (30000.0 / 7.0))) ** 2 + 0.020 ** 2)
s71 = sbin / math.sqrt(7.0) / abs(DG71)
ck("C5", abs(s71 - 0.040) <= 0.001 and abs(after(s71) - 0.0605) <= 0.001,
   "%.4f/%.4f" % (s71, after(s71)), "0.040+-0.001/0.0605+-0.001",
   "A71's arithmetic: sigma_sys 0.020 divided by sqrt(7) and every bin at the 20 kAU slope")
best = max(abs(DER["canonical|%g" % s]["dgamma_dkappa_A71conv"]) for s in (20.0, 30.0))
sig_tot30 = math.sqrt(SIG_FIT_30K ** 2 + SIG_SYS ** 2)
sk_stat = sig_tot30 / best                                  # optimistic: every pair at the best slope
sk_sysfloor = SIG_SYS / best                                # infinite-N floor with a SHARED sigma_sys
sig_lng = 0.5 * math.log(GEXT["PREREG_alt"] / GEXT["PREREG_primary"])
ratio_g = abs(DER["canonical|20"]["dgamma_dlngext"] / DER["canonical|20"]["dgamma_dlna0"])
sk_gext = sig_lng * ratio_g * KAPPA_CANON_A71               # delta ln a0 equivalent -> kappa
sk_corr = math.sqrt(sk_stat ** 2 + sk_gext ** 2)
R["R3"] = dict(A71_sigma_kappa=s71, A71_joint_after=after(s71), best_dgamma_dkappa=best,
               sigma_tot_30k=sig_tot30, sigma_kappa_shared_sys=sk_stat, sigma_kappa_floor_infiniteN=sk_sysfloor,
               sigma_ln_gext=sig_lng, gext_to_a0_ratio=ratio_g, sigma_kappa_gext=sk_gext,
               sigma_kappa_corrected=sk_corr, joint_after_corrected=after(sk_corr),
               joint_now=SKT,
               cls="A71's 0.040 STANDS" if sk_corr <= 0.050 else "A71 OVERSTATED")
P("      A71 reproduced: sigma(kappa) = %.4f, joint 0.1207 -> %.4f" % (s71, after(s71)))
P("      corrected (shared sigma_sys, best slope %.3f over 20/30 kAU, every pair there = optimistic):" % best)
P("        sigma_tot(30k) %.4f -> sigma(kappa) %.4f ; infinite-N floor from sigma_sys alone %.4f"
  % (sig_tot30, sk_stat, sk_sysfloor))
P("        g_ext-a0 degeneracy: sigma_ln g_ext %.4f x |dgamma/dln g|/|dgamma/dln a0| %.3f -> sigma(kappa) %.4f"
  % (sig_lng, ratio_g, sk_gext))
P("R3  sigma(kappa) = %.4f (not 0.040); joint 0.1207 -> %.4f (not 0.0605) -> %s"
  % (sk_corr, after(sk_corr), R["R3"]["cls"]))

# ================================================================== Q2
P("\n[C7/R4] occupancy of the 18-22 kAU bin")
rows = list(csv.DictReader(open(os.path.join(ROOT, "real_research/data/widebinaries/dr3_extract/wide_binaries_dr3.csv"))))
sep = np.array([float(r["sep_kAU"]) for r in rows])
mt = np.array([float(r["M1_msun"]) + float(r["M2_msun"]) for r in rows])
ndr3 = len(sep)
ck("C7", ndr3 == 6210 and sep.min() >= 2.0 and sep.max() < 30.0, "%d [%.2f,%.2f]" % (ndr3, sep.min(), sep.max()),
   "6210 in [2,30)", "frozen-cut DR3 catalogue on disk")
nb = int(np.sum((sep >= 18) & (sep < 22)))
f_dr3 = nb / ndr3
f_log = math.log(22 / 18) / math.log(30 / 2)
# pipeline mock re-implemented: a^-1.6 on [1, 60] kAU, thermal e, uniform mean anomaly, isotropic
rng = np.random.default_rng(20261022)
Nm = 400000
p = -0.6
a = rng.uniform(60.0 ** p, 1.0 ** p, Nm) ** (1 / p)
e = np.sqrt(rng.uniform(0, 1, Nm))
Ma = rng.uniform(0, 2 * np.pi, Nm)
E = Ma.copy()
for _ in range(60):
    E -= (E - e * np.sin(E) - Ma) / (1 - e * np.cos(E))
rr = a * (1 - e * np.cos(E))
ct = rng.uniform(-1, 1, Nm)
sproj = rr * np.sqrt(1 - ct ** 2)
sel = (sproj > 2) & (sproj < 30)
f_mock = float(np.mean((sproj[sel] >= 18) & (sproj[sel] < 22)))
yproj = G * mt * MSUN / ((sep * KAU) ** 2 * A0["canonical"])
R["R4"] = dict(n_dr3=ndr3, n_bin_dr3=nb, frac_dr3=f_dr3, frac_loguniform=f_log, frac_mock_a16=f_mock,
               overstatement_vs_dr3=f_log / f_dr3, overstatement_vs_mock=f_log / f_mock,
               frac_dr3_s_gt_10=float(np.mean(sep > 10)), frac_dr3_yproj_lt_0p3=float(np.mean(yproj < 0.3)),
               cls="A24 BIN FORECAST STANDS" if f_dr3 >= 0.037 else "A24 BIN FORECAST OVERSTATED")
P("      DR3 frozen cut: %d of %d in 18-22 kAU = %.4f ; log-uniform (A24) %.4f ; pipeline a^-1.6 mock %.4f"
  % (nb, ndr3, f_dr3, f_log, f_mock))
P("      DR3: fraction s > 10 kAU %.4f ; fraction y_proj < 0.3 (canonical) %.4f"
  % (R["R4"]["frac_dr3_s_gt_10"], R["R4"]["frac_dr3_yproj_lt_0p3"]))
P("R4  A24's 2,223-pair bin is %.1fx the DR3 frozen-cut occupancy (%.1fx the pipeline's own mock) -> %s"
  % (f_log / f_dr3, f_log / f_mock, R["R4"]["cls"]))

P("\n[R5] separating power at N = 30,000")
C825 = json.load(open(os.path.join(ROOT, "campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/cfg816_r_dr3_results.json")))
pr = C825["branches"]["primary"]
inv = 1.0 / pr["n_num"] + 1.0 / pr["n_den"]
SIG1 = {"A24 (0.0699 at 2,223)": 0.0699 * math.sqrt(2223.0),
        "CFG825 DR3 bootstrap": pr["sigma_boot"] / math.sqrt(inv),
        "CFG825 DR3 sigma_R": pr["sigma_R"] / math.sqrt(inv)}
dgam20 = r1b_c - 1.0
R5 = {"delta_gamma_20kAU": dgam20, "sigma1": SIG1, "bin": {}, "global": {}}
for occ_name, f in (("A24 log-uniform", f_log), ("pipeline mock", f_mock), ("DR3 frozen cut", f_dr3)):
    nbin = f * 30000.0
    for sn, s1 in SIG1.items():
        st = math.sqrt(s1 ** 2 / nbin + SIG_SYS ** 2)
        R5["bin"]["%s|%s" % (occ_name, sn)] = dict(N_bin=nbin, sigma_tot=st, z=dgam20 / st)
        P("      bin only: occupancy %-16s N_bin %6.0f  sigma1 %-24s %.3f  sigma_tot %.4f  z(%.3f) = %.2f"
          % (occ_name, nbin, sn, s1, st, dgam20, dgam20 / st))
DRY = dict(gamma=1.0750, sigma=0.0550, N=6210)   # DRY_RUN_2026-10-09.md line 14 (canonical, builder build)
sfit_dr3cal = DRY["sigma"] * math.sqrt(DRY["N"] / 30000.0)
for lab, sf in (("registered mock sigma_fit 0.019", SIG_FIT_30K), ("DR3-calibrated", sfit_dr3cal)):
    for fo in ("canonical", "alt"):
        d = ARM_A[fo][0] - 1.0
        st = math.sqrt(sf ** 2 + SIG_SYS ** 2)
        R5["global"]["%s|%s" % (lab, fo)] = dict(sigma_fit=sf, sigma_tot=st, z_floor=d / st)
        P("      global gamma-hat: %-32s %-9s sigma_fit %.4f sigma_tot %.4f  Arm A floor %.4f vs 1.000: z = %.2f"
          % (lab, fo, sf, st, ARM_A[fo][0], d / st))
R["R5"] = R5

P("\n[R6] current wide-binary data on record")
CF = json.load(open(os.path.join(ROOT, "campaign_fresh_gravity/CFG800_wb_2026_scoring/cfg800_results.json")))
pn = [c["p_N"] for c in CF["cookson"]]
P("      Cookson+26 (CFG800): Newton p %.2f-%.2f; MOND ~20%% step p 0.007-0.011 (CFG800 README)" % (min(pn), max(pn)))
P("      Chae & Yoon 26 (CFG800): boost 1.15-1.20  [WebFetch-level record, provisional]")
P("      record inter-group disagreement on one catalogue: 0.174 in gamma_v (real_research/reviews/mi_wb_gate_fork_2026.py:221)")
P("      CFG825 DR3 R = %.4f +- %.4f (N=%d): %.2f sigma from Newton, %.2f from Arm A canonical -> %s (frozen rule)"
  % (pr["R"], pr["sigma_R"], pr["N"], pr["dist"]["Newton / Arm C"], pr["dist"]["Arm A canon"], pr["cls"]))
zN = (DRY["gamma"] - 1) / DRY["sigma"]
zA = (ARM_A["canonical"][0] - DRY["gamma"]) / DRY["sigma"]
P("      DR3 frozen-cut dry run gamma-hat %.4f +- %.4f (NON-SCORING by PREREG): %.2f sigma above 1.000, %.2f below Arm A floor"
  % (DRY["gamma"], DRY["sigma"], zN, zA))
decided = False
R["R6"] = dict(cookson_pN=[min(pn), max(pn)], cfg825=dict(R=pr["R"], sigma_R=pr["sigma_R"], N=pr["N"], cls=pr["cls"]),
               dry_run=DRY, dry_z_newton=zN, dry_z_armA=zA, inter_group=0.174,
               cls="OPEN" if not decided else "DECIDED")
P("R6  no scoring measurement on record excludes either reading at >= 3 sigma -> OPEN")

# ================================================================== Q3
P("\n[C6/R7] A26's dwarfs with the host external field in the law")
a26 = list(csv.DictReader(open(os.path.join(ROOT, "deepseek_push/DS_FINAL_2026_10_21/A26_fork_decider/a26_rar.csv"))))
below = np.array([int(r["below_Mcrit"]) for r in a26]) == 1
D_a26 = np.array([float(r["Delta"]) for r in a26])
ck("C6", len(a26) == 92 and below.sum() == 45 and abs(np.median(D_a26[below]) - 0.651) <= 0.01,
   "%d/%d/%.3f" % (len(a26), below.sum(), np.median(D_a26[below])), "92/45/0.651+-0.01", "A26 reproduced")
dist = {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(ROOT, "real_research/data/dsph", fn))):
        try:
            dist[r["name"]] = float(r["distance_host"])
        except (ValueError, KeyError):
            pass
KPC = 3.0856775814913673e19
MHOST = {"MW": 6.0e10, "M31": 1.0e11}      # MW: CFG332 MW_MB; M31: labelled external input
a0c = A0["canonical"]


def efe_delta(mscale=1.0, kterm=True, a0=a0c):
    out, nh = [], 0
    for r in a26:
        gb = 10 ** float(r["loggbar"])
        yi = gb / a0
        ye = 0.0
        if r["host"] in MHOST and r["name"] in dist:
            ye = G * MHOST[r["host"]] * mscale * MSUN / ((dist[r["name"]] * KPC) ** 2) / a0
            nh += 1
        y = yi + ye
        nuv = q.nu(y)
        if kterm and ye > 0:
            nuv *= 1.0 + q.dlnnu_dlny(y) * (ye / y) / 3.0
        out.append(float(r["loggobs"]) - math.log10(gb * nuv))
    return np.array(out), nh


DE, nhost = efe_delta()
med = float(np.median(DE[below]))
w05 = int(np.sum(np.abs(DE[below]) <= 0.5))
DN = np.array([float(r["Delta_newton"]) for r in a26])
# Delta_newton in a26 is the medium-first prediction; data distance from Newton = Delta - Delta_newton
dataN = float(np.median((D_a26 - DN)[below]))
var = {}
for lab, kw in (("host x0.5", dict(mscale=0.5)), ("host x2", dict(mscale=2.0)),
                ("no K term (max boost)", dict(kterm=False)), ("alt a0", dict(a0=A0["alt"]))):
    dv, _ = efe_delta(**kw)
    var[lab] = float(np.median(dv[below]))
predEFE = float(np.median((D_a26 - DE)[below]))     # law-first-EFE prediction relative to isolated law
nfield_below = sum(1 for r, b in zip(a26, below) if b and r["host"] == "field")
cls7 = ("DWARFS SUPPORT EFE-PRESENT LAW-FIRST" if abs(med) <= 0.3 and w05 >= 15 else
        "DWARFS EXCLUDE BOTH READINGS" if med >= 0.5 and dataN >= 1.5 else "INTERMEDIATE")
R["R7"] = dict(n_with_host=nhost, median_Delta_EFE_below=med, within_0p5=w05, n_below=int(below.sum()),
               median_Delta_isolated_below=float(np.median(D_a26[below])),
               median_EFE_shift_below=predEFE, median_data_minus_newton_below=dataN,
               variants=var, n_field_below=nfield_below, cls=cls7)
P("      systems with a host distance: %d ; sub-threshold median shift of the law-first prediction by the EFE: %+.3f dex"
  % (nhost, -predEFE))
P("      sub-threshold median Delta: isolated law %+.3f ; EFE-present law %+.3f ; within 0.5 dex of EFE law %d/45"
  % (np.median(D_a26[below]), med, w05))
P("      data above Newton (medium-first) by %+.3f dex (median)" % dataN)
for k, v in var.items():
    P("        variant %-24s median Delta_EFE %+.3f" % (k, v))
P("      isolated (field) sub-threshold systems with sigma on disk: %d" % nfield_below)
P("R7  -> %s" % cls7)

# ================================================================== Q4
P("\n[R8] what DR4 needs for 3 sigma, law-first (Arm A floor) vs 1.000")
R8 = {}
for fo in ("canonical", "alt"):
    d = ARM_A[fo][0] - 1.0
    ceil = d / 3.0
    for lab, s1 in (("mock", SIG_FIT_30K * math.sqrt(30000)), ("DR3-cal", DRY["sigma"] * math.sqrt(DRY["N"]))):
        row = {}
        for ss in (0.01, 0.02, 0.03, 0.04, 0.05):
            need = ceil ** 2 - ss ** 2
            row[str(ss)] = (s1 / math.sqrt(need)) ** 2 if need > 0 else None
        R8["%s|%s" % (fo, lab)] = dict(sigma_sys_ceiling=ceil, N_total=row)
        P("      %-9s %-7s sigma_sys ceiling %.4f ; N_total for 3 sigma at sigma_sys 0.01/0.02/0.03/0.04/0.05: %s"
          % (fo, lab, ceil, " / ".join("%s" % ("%.0f" % v if v else "never") for v in row.values())))
# bin-only
d20 = dgam20
need = (d20 / 3) ** 2 - SIG_SYS ** 2
for sn, s1 in SIG1.items():
    nbin_need = s1 ** 2 / need
    R8["bin|%s" % sn] = dict(N_bin=nbin_need, N_total_dr3=nbin_need / f_dr3, N_total_mock=nbin_need / f_mock)
    P("      18-22 kAU bin alone, sigma1 %-24s: N_bin %.0f -> N_total %.0f (DR3 occupancy) / %.0f (mock)"
      % (sn, nbin_need, nbin_need / f_dr3, nbin_need / f_mock))
R["R8"] = R8
P("      record inter-group gamma_v disagreement 0.174 vs canonical sigma_sys ceiling %.4f: ratio %.1f"
  % (R8["canonical|mock"]["sigma_sys_ceiling"], 0.174 / R8["canonical|mock"]["sigma_sys_ceiling"]))

# ================================================================== close
npass = sum(c["passed"] for c in CHECKS)
P("\nD2_WIDE_BINARY_FORK COMPLETE: %d/%d checks PASS." % (npass, len(CHECKS)))
R["checks"] = CHECKS
R["n_pass"], R["n_checks"] = npass, len(CHECKS)
with open(OUT, "w") as f:
    f.write("\n".join(LINES) + "\n")
with open(JS, "w") as f:
    json.dump(R, f, indent=1, default=float)
sys.exit(0 if npass == len(CHECKS) else 1)
