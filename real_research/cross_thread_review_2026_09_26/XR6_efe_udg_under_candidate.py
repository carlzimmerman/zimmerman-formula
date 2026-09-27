#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR6_efe_udg_under_candidate.py -- the construction the parallel threads converged on (2026-09-26, evening) scored
against the galaxy-environment liabilities that no thread owns: the two 09-03 external-field (EFE) samples and the
Coma ultra-diffuse galaxies.  (The Local Group zero-velocity radius is XR6_lg_zero_velocity_mond_sector.py.)
Independent cross-thread review.  Read-only on every committed file: the loaders of hunt_2026/k_contrarian_clusterbtfr.py
and k_contrarian_dwarfefe.py are IMPORTED (their main() is never called); L23's Coma pipeline, L340's nu_mono and the
switch are REIMPLEMENTED here, each with a control that reproduces the committed numbers.

THE CANDIDATE (C-H/K branch; every definition read from the code):
  kernel   nu_mono (L340_filtered_khronon_completion.py:103-117) = nu_RAR for y <= 2.3374 (XC4), region-local per
           L361_bound_region_kernel.py:16-32: (lap - M^2) w = 4 pi G f rho_b, M^2 = m^2 (1 - f), 1/m <= 0.5 Mpc (L361 R4):
           a region's kernel reads ITS OWN baryons; fields from outside are screened across the inactive web; in-region
           baryons feel their region's phantom; the carrier is Newtonian only (L353).  Inside a region the EFE is
           ordinary QUMOND sourced by the in-region BARYONS: e_N = G M_b(<r)/r^2 (XR4's reading, XR4:9-24).
  switch   the MOND-sector reading as the particle-mesh track implements it (L395_two_switch_branches.py:22-25 and its
           phantom_sw, cell 'msc'): x = 1.5 Omega_m(z) (rho_b + max(rho_ph,all, 0))/rho_bar_m (absolute; the
           untruncated phantom of ALL baryons), ON where x >= x_c,eff(z) max(1, v_loc^2/v_cap^2),
           x_c,eff = x_c0 [Omega_L0/Omega_L(z)]^p = x_c0 E(z)^(2p), p = 1, x_c0 = 2.5; v_loc^2 = |g_ms|^2/(-div g_ms) of
           the MOND-sector field g_ms = g_N,b + g_ph (0 where -div g_ms <= 0, as L395 does); v_cap = 325 km/s (MS3 K1).
           Equivalent form (derived in the README, checked here as K0): ON <=> 4 pi G rho_ms >= max(x_c,eff H^2,
           sqrt(x_c,eff) H |g_ms|/v_cap).  So the cap binds only where the MOND-sector field is strong and the density
           is near the web's: the outskirts of hosts with v_loc > v_cap.  In deep MOND v_loc^2 = v_f(r)^2/(1 + s/2),
           s = dlnM_b/dlnr, and the capped edge is r_cap = (1 + s/2) v_cap/(H sqrt(x_c,eff)) -- the SAME for every host
           above v_cap (MS3's 1.75 Mpc at z = 0.5; ~3.6 Mpc at z = 0.02-0.06).
  carrier  kernel-invisible, cleared by a density trigger (kick 575-650 km/s); retention by host mass from L388.
THE MECHANISM, computed per galaxy (not assumed):
  (a) inside the host's MOND region -> the in-region EFE from the host's baryons;
  (b) beyond it, in its own region -> no EFE except what the screened gap transmits (L361 R1's Yukawa law);
  (c) no region at its disc, or a region smaller than the radius its kinematics sample -> Newtonian with the carrier
      cleared: a NEW failure if it happens (reported as plainly as a rescue).
  The galaxy's own region is found with the same switch: the host's local MOND-sector density and field plus the
  galaxy's own phantom in the host's external field (scalar-sum form, XR4's committed form); its edge is where the
  capped threshold wins.  The 1-D form drops the positive lobes of the true 3-D EFE phantom, so it UNDER-estimates the
  galaxy's region: conservative for the case-(c) check.

SCENARIOS (one switch reading and one cell each, never pooled):
  S0  XR4's switch (the on-branch closed-form edge), no cap, nu_RAR   -- the control; must equal XR4's committed numbers
  S1  the MOND-sector switch, no cap                                  -- the candidate with the cap removed (= MUTATE)
  S2-S4  the MOND-sector switch WITH the cap, operator A (L361's action): gap Dirichlet / 1/m = 0.2 / 0.5 Mpc
  S5  the MOND-sector switch with the cap, operator B (the PM track's L377/L395 phantom, which reads ALL baryons in
      nu's argument, XR5 table row B): the cap removes phantom but screens no external field -> the EFE is S1's
  Systematics carried per scenario: f_b(R500) in {0.10, 0.13, 0.157} (XR4's template), the scalar-sum and 1-D QUMOND
  subtract forms (XR4), the committed 3-D radius r = R_proj and the deprojected r = 1.3 R_proj (the committed cb-7 row),
  the cluster's baryons extended (XR4) or truncated at r200 (MS3's halo-model 'door'), both a0 footings.

CHECKS (controls first; load-bearing unless marked 'reported')
  K0  the kernel: nu_mono = nu_RAR to 1e-6 for y <= 2.337 and max |dlog| = 0.0104 dex (XC4: 0.01037); the switch's
      equivalent form holds on random draws.
  K5  the local cap reproduces MS3's design target: a deep-MOND host above v_cap at z = 0.5 is capped at 1.75 Mpc (MS3 K1)
      within the kernel's non-deep correction (<= 3%), and every KiDS lens (M_b <= 3e11, v_f <= 247 km/s) keeps its
      uncapped edge (MS3 K1's statement).
  C1  CONTROL: S0 reproduces XR4's committed cluster numbers (every f_b, form and footing; 1e-9).
  C2  CONTROL: XR4's committed dwarf numbers (statistic C; six variants x two footings; 1e-9).
  C3  CONTROL: L23's committed Coma numbers (+1.159 / +1.112 dex, systematic floor 0.227, 4.9 / 4.7 sigma, DF44 alone
      +0.938 +- 0.139, first infall at 9 Mpc +0.635).
  K1  THE CAP MOVES CLUSTER MEMBERS OUT OF THEIR CLUSTER'S REGION: >= 10% of the 314 members lie beyond the capped
      edge (committed geometry, every f_b, both footings).  MUTATE=1 (no cap) must FAIL this.
  N1  (reported, pre-declared) NO NEW FAILURE: every member beyond the cap keeps its disc switched on and its own region
      out to at least R_HI (the radius W50 samples).
  V1  (reported, pre-declared) the cap RESCUES the cluster slope: every operator-A variant < 3 sigma.
  V2  (reported, pre-declared) the cap makes the slope WORSE: every operator-A variant is further from the data than the
      same variant uncapped (S1).
  V3  (reported) the zero point (members - field) under the cap.
  D1  the dwarfs: the cap binds nowhere in the MW/M31 regions (v_loc < v_cap in every host's deep-MOND zone) and every
      dwarf's position is switched ON, inside its host's MOND-sector region (except those beyond it, screened).
  D2  (reported, pre-declared) the dwarf liability STANDS: every candidate variant >= 3 sigma.
  U1  all eleven Coma UDGs (projected and Einasto 3-D positions; three Coma mass models; every f_b; both footings) lie
      inside Coma's capped MOND region, so the EFE acts on them under the candidate.
  U2  (reported, pre-declared) the UDG liability FLIPS under the candidate: central arm < 3 sigma on both footings, with
      the systematic floor recomputed on the candidate's arm.
  U3  THE CAP REMOVES COMA'S FIELD AT THE FIRST-INFALL RADIUS (9 Mpc lies beyond the capped edge).  MUTATE=1 must FAIL.
  U4  (reported) Coma's retained carrier inside a UDG's r_1/2 moves the offset by < 0.01 dex (it cannot rescue it).
MUTATE=1 removes the cap (v_cap -> infinity) on the MOND-sector reading: every cluster member is back inside its
cluster's region, the cluster numbers must equal XR4's, and K1 and U3 must FAIL (rc = 1).
Runtime ~1 min, single-threaded.  Run from the repository root:
    python3 real_research/cross_thread_review_2026_09_26/XR6_efe_udg_under_candidate.py      (MUTATE=1 for the control)
"""
import os, sys, json, math, time
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR6_efe_udg_under_candidate"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
OUT = {"lane": SLUG, "mutate": MUTATE, "cell": "p = 1, x_c0 = 2.5", "switch": "MOND-sector reading (L395 'msc')",
       "checks": {}, "numbers": {}}
CH = []


def check(name, measured, ok, load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}\n         measured: {measured}")


def banner(t):
    P("\n" + "=" * 118); P(t); P("=" * 118)


P(__doc__.split("SCENARIOS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the cap is removed (v_cap -> infinity); the cluster numbers must return to XR4's and K1, U3 must FAIL ***")

import k_contrarian_clusterbtfr as KC          # noqa: E402  (committed 09-03; main() NOT called)
import k_contrarian_dwarfefe as KD             # noqa: E402
from hunt_lib import A0                        # noqa: E402  (9.36e-11 / 1.13e-10, the footings XR4 used)

G, MSUN, MPC = KC.G, KC.MSUN, KC.MPC
KPC = MPC / 1e3
FCOS = 0.157
XR4R = json.load(open(os.path.join(HERE, "XR4_efe_under_region_kernel_results.json")))["numbers"]
L388R = json.load(open(os.path.join(REPO, "real_research", "dark_sector_2026", "L388_linear_gate_pooled_results.json")))["numbers"]
MS3R = json.load(open(os.path.join(REPO, "real_research", "mond_sector_gate_2026",
                                   "MS3_cosmic_shear_bound_mond_sector_results.json")))["numbers"]

# ------------------------------------------------------------------ the switch's cosmology (GP0's, in which MS3 set v_cap)
HH = 0.6736
OMM = (0.02237 + 0.1200) / HH ** 2; OML = 1.0 - OMM; FBC = 0.02237 / (0.02237 + 0.1200)
H0S = 100.0 * HH * 1e3 / MPC
E2 = lambda z: OMM * (1 + z) ** 3 + OML
Hz = lambda z: H0S * math.sqrt(E2(z))
Omz = lambda z: OMM * (1 + z) ** 3 / E2(z)
XC0, PG = 2.5, 1.0
xceff = lambda z: XC0 * E2(z) ** PG                 # = x_c0 [Omega_L0/Omega_L(z)]^p  (Omega_L0/Omega_L(z) = E^2)
VCAP_CAND = 325.0e3                                 # m/s: L395 VCAP_CODE2 = 3.25^2 (100 km/s)^2; MS3 K1 v_cap = 325.3
VCAP = math.inf if MUTATE else VCAP_CAND
GAPS = (("Dirichlet", 0.0), ("1/m=0.2", 0.2), ("1/m=0.5", 0.5))   # L361 R4: KiDS needs 1/m <= 0.5 Mpc

# ------------------------------------------------------------------ nu_mono, rebuilt from L340:103-117 (the same lines)
def _h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore", invalid="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)


def _dh_rar(y, e=1e-6):
    return (_h_rar(y * (1 + e)) - _h_rar(y * (1 - e))) / (2 * y * e)


Y_P = brentq(lambda y: float(_dh_rar(y)), 1.0, 5.0); H_P = float(_h_rar(Y_P)); DELTA = 0.05
LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
DH_MONO = np.maximum(_dh_rar(YG), DELTA * H_P / (YG + Y_P))
H_MONO = float(_h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH_MONO[1:] + DH_MONO[:-1]) * np.diff(YG))])


def nu_rar(y):
    y = np.maximum(np.asarray(y, float), 1e-300); return 1.0 / (-np.expm1(-np.sqrt(y)))


def nu_mono(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0 + np.interp(np.log10(y), LYG, H_MONO) / y


def dnu_mono(y):
    """d nu_mono/dy = h'(y)/y - h(y)/y^2 with h' the tabulated monotone derivative (exact for the construction)."""
    y = np.maximum(np.asarray(y, float), 1e-12); ly = np.log10(y)
    return np.interp(ly, LYG, DH_MONO) / y - np.interp(ly, LYG, H_MONO) / y ** 2


def fb_profile(x, f500):
    """XR4's template (XR4_efe_under_region_kernel.py:78-81): f_b = f500 inside R500, log-linear to cosmic at 2 R500."""
    t = np.clip(np.log(np.maximum(x, 1e-9)) / math.log(2.0), 0.0, 1.0)
    return f500 + (FCOS - f500) * t


# ------------------------------------------------------------------ the switch
def ms_profile(r, Mb, a0):
    """spherical MOND-sector field of a baryonic mass profile M_b(<r) [kg] on a grid r [m], untruncated (the phantom as if
    switched on everywhere, L395's Phi_all): e = G M_b/r^2, g_ms = nu(e/a0) e, D = -div g_ms = (1/r^2) d(r^2 g_ms)/dr,
    qb = 4 pi G (baryon excess density) = G dM_b/dr / r^2."""
    dMb = np.gradient(Mb, r)
    e = G * Mb / r ** 2; y = e / a0; nu_ = nu_mono(y)
    dydr = (G / (a0 * r ** 2)) * (dMb - 2.0 * Mb / r)
    D = (G / r ** 2) * (dMb * nu_ + Mb * dnu_mono(y) * dydr)
    return e, nu_ * e, D, G * dMb / r ** 2


def switch_state(z, D, qb, g, vcap, extra=0.0, Dextra=0.0, gextra=0.0):
    """L395 'msc': x = 1.5 Om(z) f_b (ambient baryons) + (4 pi G)(drho_b + max(rho_ph, 0))/H^2 (+ a second system's positive
    density), threshold x_c,eff max(1, v_loc^2/v_cap^2), v_loc^2 = |g|^2/(-div g) (0 where -div g <= 0)."""
    H = Hz(z); xc = xceff(z)
    x = 1.5 * Omz(z) * FBC + (qb + np.maximum(D - qb, 0.0) + extra) / H ** 2
    Dt = D + Dextra
    vl2 = np.where(Dt > 0, (g ** 2 + gextra ** 2) / np.maximum(Dt, 1e-300), 0.0)
    thr = xc * np.maximum(1.0, vl2 / vcap ** 2)
    return x >= thr, x, thr, vl2


def region_edge(r, on):
    """outer edge of the ON set that contains the innermost ON point (first ON, then the first OFF after it)."""
    ion = np.where(on)[0]
    if ion.size == 0:
        return float(r[0]), False
    i0 = ion[0]; off = np.where(~on[i0:])[0]
    if off.size == 0:
        return float(r[-1]), True
    i1 = i0 + off[0]
    return float(math.sqrt(r[i1 - 1] * r[i1])), True


def transmit(rho, r_cap, minv):
    """L361's screened w outside a region (monopole Yukawa exterior matched to the in-region field at r_cap):
    field(rho)/field_unscreened(rho) = exp[-m (rho - r_cap)] (1 + m rho)/(1 + m r_cap); Dirichlet (m -> inf) gives 0."""
    if minv <= 0:
        return 0.0
    m = 1.0 / (minv * MPC)
    return math.exp(-m * (rho - r_cap)) * (1.0 + m * rho) / (1.0 + m * r_cap)


def galaxy_region(Mg, Rk, z, a0, e_loc, g_h, D_h, qb_h, vcap):
    """A galaxy's own region in its host's (untruncated) MOND-sector field: the host's local density D_h, qb_h and field
    g_h plus the galaxy's phantom (baryons Mg [kg]) in the host's external field e_loc (scalar-sum form).  Returns (disc_on, R_e [m],
    region reaches R_k).  R_k = the radius the galaxy's kinematics sample (R_HI, or r_1/2)."""
    H = Hz(z); xc = xceff(z)
    GM = G * Mg
    Dd = 3.0 * GM / Rk ** 3; gd = GM / Rk ** 2               # the galaxy inside R_k: its mean baryon density (a lower bound)
    on_d, _, _, _ = switch_state(z, np.array([D_h]), np.array([qb_h]), np.array([g_h]), vcap,
                                 extra=Dd, Dextra=Dd, gextra=gd)
    s = np.geomspace(Rk, 8.0 * MPC, 1200)
    gN = GM / s ** 2; y = (gN + e_loc) / a0
    gg = nu_mono(y) * gN
    Dg = -2.0 * GM ** 2 * dnu_mono(y) / (s ** 5 * a0)
    on, _, _, _ = switch_state(z, np.full_like(s, D_h), np.full_like(s, qb_h), np.full_like(s, g_h), vcap,
                               extra=np.maximum(Dg, 0.0), Dextra=Dg, gextra=gg)
    if not on[0]:
        return bool(on_d[0]), float(Rk), False
    off = np.where(~on)[0]
    Re = float(s[-1]) if off.size == 0 else float(math.sqrt(s[off[0] - 1] * s[off[0]]))
    return bool(on_d[0]), Re, True


# ============================================================================================ K0 / K5 kernel and switch
banner("K0/K5  THE KERNEL AND THE SWITCH: nu_mono against XC4; the cap's equivalent form; MS3's design target")
ys = np.logspace(-6, math.log10(2.337), 4001)
d_lo = float(np.max(np.abs(nu_mono(ys) / nu_rar(ys) - 1)))
yall = np.logspace(-3, 4, 14001)
d_max = float(np.max(np.abs(np.log10(nu_mono(yall) / nu_rar(yall)))))
rng0 = np.random.default_rng(1)
okeq = True
for _ in range(20000):                                          # the equivalent form of the capped switch
    H_ = 10 ** rng0.uniform(-18.5, -17.0); xc_ = 10 ** rng0.uniform(0.0, 1.5); vc_ = 10 ** rng0.uniform(4.5, 6.5)
    rho4 = 10 ** rng0.uniform(-38, -28); gg_ = 10 ** rng0.uniform(-14, -9)
    a = rho4 / H_ ** 2 >= xc_ * max(1.0, gg_ ** 2 / rho4 / vc_ ** 2)
    b = rho4 >= max(xc_ * H_ ** 2, math.sqrt(xc_) * H_ * gg_ / vc_)
    okeq &= (a == b)
P(f"    nu_mono: phantom peak y_p = {Y_P:.4f}; max |nu_mono/nu_RAR - 1| for y <= 2.337: {d_lo:.1e}; max |dlog| over 1e-3..1e4: {d_max:.5f} dex")
check("K0 the kernel is L340's nu_mono (= nu_RAR to 1e-6 for y <= 2.337; max |dlog nu| = 0.0104 dex, XC4's 0.01037), and the "
      "capped switch x >= x_c max(1, v_loc^2/v_cap^2) equals 4 pi G rho >= max(x_c H^2, sqrt(x_c) H |g|/v_cap) on 20000 "
      "random draws", f"{d_lo:.1e}; {d_max:.5f} dex; equivalence {'holds' if okeq else 'FAILS'}",
      d_lo < 1e-6 and abs(d_max - 0.01037) < 3e-4 and okeq)

K5 = {}
for lab, Mbp, vc in (("host above v_cap, 3e12", 3e12, VCAP_CAND), ("host above v_cap, 1e13", 1e13, VCAP_CAND),
                     ("KiDS lens 3e11", 3e11, VCAP_CAND), ("KiDS lens 3e11, no cap", 3e11, math.inf)):
    rr = np.geomspace(0.05 * MPC, 30 * MPC, 6000)
    e_, g_, D_, qb_ = ms_profile(rr, np.full_like(rr, Mbp * MSUN), A0["canonical"])
    on_, *_ = switch_state(0.5, D_, qb_, g_, vc)
    K5[lab] = region_edge(rr, on_)[0] / MPC
r_ms3 = float(MS3R["K1_design"]["r_cap_z05"]); v_ms3 = float(MS3R["K1_design"]["v_cap"])
target = VCAP_CAND / (Hz(0.5) * math.sqrt(xceff(0.5))) / MPC
P(f"    local-form edges at z = 0.5 (canonical): " + ", ".join(f"{k}: {v:.3f} Mpc" for k, v in K5.items())
  + f";  v_cap/(H sqrt(x_c,eff)) = {target:.3f} Mpc; MS3 K1: r_cap = {r_ms3} Mpc (v_cap = {v_ms3:.1f} km/s)")
check("K5 the local cap reproduces MS3's design target: deep-MOND hosts above v_cap end at MS3's 1.75 Mpc at z = 0.5 (within "
      "the kernel's non-deep correction, <= 3%), and a KiDS lens (M_b = 3e11, v_f = 247 km/s) keeps its uncapped edge",
      f"3e12: {K5['host above v_cap, 3e12']:.3f}, 1e13: {K5['host above v_cap, 1e13']:.3f} Mpc vs {r_ms3}; KiDS lens "
      f"{K5['KiDS lens 3e11']:.3f} vs uncapped {K5['KiDS lens 3e11, no cap']:.3f} Mpc",
      abs(K5["host above v_cap, 3e12"] / r_ms3 - 1) < 0.03 and abs(K5["host above v_cap, 1e13"] / r_ms3 - 1) < 0.06
      and abs(K5["KiDS lens 3e11"] / K5["KiDS lens 3e11, no cap"] - 1) < 2e-3 and abs(target / r_ms3 - 1) < 0.01)
OUT["numbers"]["K0K5"] = dict(y_p=Y_P, max_rel_below_2337=d_lo, max_dlog=d_max, K5_edges_Mpc=K5, target=target)

# ============================================================================================ PART A clusters
banner("PART A -- the cluster-infall BTFR (k_contrarian_clusterbtfr, N = 314) under the candidate")
gal = KC.build(1.0); cls = KC.clusters()
idx, xr500, Rp = KC.assign(gal, cls)
memb = idx >= 0
V = np.array([x["V"] for x in gal]); Mb = np.array([x["Mb"] for x in gal]) * MSUN
lHIall = np.array([x["lMHI"] for x in gal]); RHI = KC.rhi_wang(lHIall); gN = G * Mb / RHI ** 2
lMb_all = np.log10(Mb / MSUN)
used = sorted(set(int(j) for j in idx[memb]))
for j in used:
    c = cls[j]
    c["r200"] = brentq(lambda r: KC.nfw_menc(r, c["M500"], c["r500"]) * MSUN / (4 / 3 * math.pi * r ** 3) - 200 * KC.rho_c(c["z"]),
                       0.3 * c["r500"], 6.0 * c["r500"])
P(f"  members N = {memb.sum()} in {len(used)} PSZ2 clusters (committed 314)")


def cluster_Mb(c, f500, extent, r):
    Mbr = fb_profile(r / c["r500"], f500) * KC.nfw_menc(r, c["M500"], c["r500"]) * MSUN
    if extent == "r200":
        r2 = c["r200"]
        Mbr = np.where(r > r2, fb_profile(r2 / c["r500"], f500) * KC.nfw_menc(r2, c["M500"], c["r500"]) * MSUN, Mbr)
    return Mbr


def cluster_switch(c, a0, f500, extent, vcap):
    r = np.geomspace(0.05 * c["r500"], 40.0 * MPC, 4000)
    Mbr = cluster_Mb(c, f500, extent, r)
    e, g, D, qb = ms_profile(r, Mbr, a0)
    on, x, thr, vl2 = switch_state(c["z"], D, qb, g, vcap)
    re, found = region_edge(r, on)
    ie = min(np.searchsorted(r, re), len(r) - 1)
    return dict(r=r, Mb=Mbr, e=e, g=g, D=D, qb=qb, r_e=re, found=found, vloc_edge=math.sqrt(max(vl2[ie], 0.0)))


def xr4_edge_Mpc(Mb_msun, a0, xc0=2.5):
    """XR4's on-branch closed-form edge (XR4_efe_under_region_kernel.py:62-66)."""
    vf = (G * Mb_msun * MSUN * a0) ** 0.25
    return vf / (67.4e3 / MPC * math.sqrt(xc0 + 1.5 * 0.3134)) / MPC


def regress(D, m, lge):
    A = np.column_stack([np.ones(m.sum()), lMb_all[m], lHIall[m], lge])
    return np.linalg.lstsq(A, D[m], rcond=None)[0][-1], A


def boot_err(D, m, lge, nb=3000, seed=3):
    s, A = regress(D, m, lge); rng = np.random.default_rng(seed); n = m.sum(); bs = np.empty(nb)
    for k in range(nb):
        kk = rng.integers(0, n, n); bs[k] = np.linalg.lstsq(A[kk], D[m][kk], rcond=None)[0][-1]
    return s, bs.std()


ZP_CACHE = {}


def zero_point(Dobs, Dpre, key):
    """XR4's zero_point (XR4:98-107): joint regression on [1, log M_b, log M_HI, member]; bootstrap error of the observed."""
    keep = np.isfinite(Dobs) & np.isfinite(lHIall) & np.isfinite(lMb_all)
    lo, hi = np.percentile(lMb_all[memb], 2), np.percentile(lMb_all[memb], 98)
    use = keep & (lMb_all > lo) & (lMb_all < hi); ind = memb.astype(float)
    Aj = np.column_stack([np.ones(use.sum()), lMb_all[use], lHIall[use], ind[use]])
    co = np.linalg.lstsq(Aj, Dobs[use], rcond=None)[0][-1]; cp = np.linalg.lstsq(Aj, Dpre[use], rcond=None)[0][-1]
    if key not in ZP_CACHE:
        rng = np.random.default_rng(23); nn = use.sum(); bj = np.empty(1500)
        for k in range(1500):
            kk = rng.integers(0, nn, nn); bj[k] = np.linalg.lstsq(Aj[kk], Dobs[use][kk], rcond=None)[0][-1]
        ZP_CACHE[key] = bj.std()
    return co, cp, ZP_CACHE[key]


def predict(e, a0, nuf):
    """XR4's two forms: scalar sum nu((gN + e)/a0) G M_b/R_HI, and the 1-D QUMOND subtract form."""
    Dp = np.log10(np.sqrt(nuf((gN + e) / a0) * G * Mb / RHI)) - 0.25 * np.log10(G * Mb * a0)
    gi = nuf((gN + e) / a0) * (gN + e) - np.where(e > 0, nuf(np.maximum(e, 1e-30) / a0) * e, 0.0)
    Dq = np.log10(np.sqrt(np.maximum(gi, 1e-30) * RHI)) - 0.25 * np.log10(G * Mb * a0)
    return Dp, Dq


F500S = (0.10, 0.13, FCOS)
GEOS = (("R_proj", 1.0), ("1.3 R_proj", 1.3))
EXTS = ("extended", "r200")
RESA = {}
NEWFAIL = []
CLASS = {}
EDGES = {}
ymax_seen = 0.0
for foot, a0 in A0.items():
    Dobs = np.log10(V * 1e3) - 0.25 * np.log10(G * Mb * a0)
    for geo, dp in GEOS:
        r_m = np.zeros(len(gal)); x_m = np.zeros(len(gal)); ge = np.zeros(len(gal))
        for i in np.where(memb)[0]:
            c = cls[idx[i]]; r = max(Rp[i] * dp, 0.05 * c["r500"])
            r_m[i] = r; x_m[i] = r / c["r500"]
            ge[i] = G * KC.nfw_menc(r, c["M500"], c["r500"]) * MSUN / r ** 2
        lge = np.log10(ge[memb] / a0)
        sobs, eobs = boot_err(Dobs, memb, lge)
        for f500 in F500S:
            for ext in EXTS:
                key = f"{foot}/{geo}/{f500}/{ext}"
                # per-cluster switch: capped (the candidate, or none under MUTATE) and uncapped
                sw = {j: cluster_switch(cls[j], a0, f500, ext, VCAP) for j in used}
                swu = {j: cluster_switch(cls[j], a0, f500, ext, math.inf) for j in used}
                if geo == "R_proj":
                    EDGES[f"{foot}/{f500}/{ext}"] = {cls[j]["name"]: dict(capped=sw[j]["r_e"] / MPC, uncapped=swu[j]["r_e"] / MPC,
                                                                          xr4=xr4_edge_Mpc(FCOS * KC.nfw_menc(2 * cls[j]["r500"], cls[j]["M500"], cls[j]["r500"]), a0),
                                                                          vloc_edge_kms=sw[j]["vloc_edge"] / 1e3,
                                                                          z=cls[j]["z"]) for j in used}
                # in-region field of every member (the host's baryons at the member's radius) and the classification
                e_in = np.zeros(len(gal)); e_B = np.zeros(len(gal)); cls_lab = np.array([""] * len(gal), dtype=object)
                e_gap = {g_: np.zeros(len(gal)) for g_, _ in GAPS}
                Re_gal = np.full(len(gal), np.nan); nbeyond = 0; nbeyond_unc = 0
                for i in np.where(memb)[0]:
                    j = int(idx[i]); c = cls[j]; S = sw[j]; r = r_m[i]
                    e_i = G * float(cluster_Mb(c, f500, ext, np.array([r]))[0]) / r ** 2
                    e_in[i] = e_i; e_B[i] = e_i
                    if r > swu[j]["r_e"]:
                        nbeyond_unc += 1
                    if r <= S["r_e"]:
                        cls_lab[i] = "a"
                        for g_, _ in GAPS: e_gap[g_][i] = e_i
                        continue
                    lr = np.log(S["r"])
                    at = lambda arr: float(np.interp(math.log(r), lr, arr))
                    disc_on, Re, reach = galaxy_region(Mb[i], RHI[i], c["z"], a0, at(S["e"]), at(S["g"]), at(S["D"]),
                                                       at(S["qb"]), VCAP)
                    Re_gal[i] = Re
                    if (not disc_on) or (not reach):
                        NEWFAIL.append(dict(key=key, agc=gal[i]["agc"], disc_on=disc_on, Re_kpc=Re / KPC, RHI_kpc=RHI[i] / KPC))
                    if r - Re <= S["r_e"]:
                        cls_lab[i] = "a (merged)"
                        for g_, _ in GAPS: e_gap[g_][i] = e_i
                        continue
                    cls_lab[i] = "b"; nbeyond += 1
                    Mcap = float(np.interp(math.log(S["r_e"]), lr, S["Mb"]))
                    rho = r - Re
                    for g_, minv in GAPS:
                        e_gap[g_][i] = G * Mcap / rho ** 2 * transmit(rho, S["r_e"], minv)
                ymax_seen = max(ymax_seen, float(np.max((gN[memb] + e_in[memb]) / a0)))
                rows = {}
                scen = {}
                if ext == "extended":
                    e0 = np.zeros(len(gal)); e0[memb] = fb_profile(x_m[memb], f500) * ge[memb]
                    scen["S0 XR4 switch, no cap (nu_RAR)"] = (e0, KC.nu)
                scen["S1 MOND-sector switch, no cap"] = (e_in, nu_mono)
                for g_, _ in GAPS:
                    scen[f"S{2 + [x[0] for x in GAPS].index(g_)} capped, operator A, gap {g_}"] = (e_gap[g_], nu_mono)
                scen["S5 capped, operator B (PM: all baryons in nu)"] = (e_B, nu_mono)
                for sname, (ee, nuf) in scen.items():
                    Dp, Dq = predict(ee, a0, nuf)
                    sp, _ = regress(Dp, memb, lge); sq, _ = regress(Dq, memb, lge)
                    co, cp, sej = zero_point(Dobs, Dp, f"{foot}/{geo}")
                    rows[sname] = dict(slope_scalar=float(sp), sigma_scalar=float(abs(sobs - sp) / eobs),
                                       slope_subtract=float(sq), sigma_subtract=float(abs(sobs - sq) / eobs),
                                       zp_obs=float(co), zp_pred=float(cp), zp_err=float(sej), zp_sigma=float(abs(co - cp) / sej))
                RESA[key] = dict(obs=float(sobs), err=float(eobs), n_beyond_cap=int(nbeyond), n_beyond_uncapped=int(nbeyond_unc),
                                 n_members=int(memb.sum()), rows=rows,
                                 Re_over_RHI_min=float(np.nanmin(Re_gal[memb] / RHI[memb])) if np.any(np.isfinite(Re_gal[memb])) else None,
                                 Re_kpc_median=float(np.nanmedian(Re_gal[memb]) / KPC) if np.any(np.isfinite(Re_gal[memb])) else None)
                if geo == "R_proj" and f500 == 0.13 and ext == "extended":
                    CLASS[foot] = {k_: int(np.sum(cls_lab[memb] == k_)) for k_ in ("a", "a (merged)", "b")}

# ---- the edges
P("\n  THE SWITCH ON THE 21 CLUSTERS (committed geometry, f_b(R500) = 0.13, extended baryons):")
for foot in A0:
    Ed = EDGES[f"{foot}/0.13/extended"]
    cap = [v["capped"] for v in Ed.values()]; unc = [v["uncapped"] for v in Ed.values()]; x4 = [v["xr4"] for v in Ed.values()]
    vl = [v["vloc_edge_kms"] for v in Ed.values()]
    P(f"    {foot:9s}: region edge {'(no cap) ' if MUTATE else 'capped '}{min(cap):.2f}-{max(cap):.2f} Mpc; uncapped MOND-sector "
      f"{min(unc):.1f}-{max(unc):.1f} Mpc; XR4's on-branch {min(x4):.1f}-{max(x4):.1f} Mpc; v_loc at the region edge "
      f"{min(vl):.0f}-{max(vl):.0f} km/s (v_cap 325)")
    P(f"               classification of the 314 members: {CLASS[foot]}  (a = inside the cluster's region, b = own region beyond it)")
OUT["numbers"]["cluster_edges"] = EDGES
OUT["numbers"]["classification"] = CLASS

# ---- control C1
d_c1 = 0.0
for foot in A0:
    ref = XR4R["clusters"][foot]
    for f500 in F500S:
        row = RESA[f"{foot}/R_proj/{f500}/extended"]["rows"]["S0 XR4 switch, no cap (nu_RAR)"]
        rv = ref["variants"][str(f500)]
        for k_ in ("slope_scalar", "sigma_scalar", "slope_subtract", "sigma_subtract", "zp_obs", "zp_pred", "zp_err", "zp_sigma"):
            d_c1 = max(d_c1, abs(row[k_] - rv[k_]))
    d_c1 = max(d_c1, abs(RESA[f"{foot}/R_proj/0.13/extended"]["obs"] - ref["obs"]), abs(RESA[f"{foot}/R_proj/0.13/extended"]["err"] - ref["err"]))
check("C1 CONTROL: with XR4's switch and no cap (S0) XR4's committed cluster numbers are reproduced -- every f_b(R500), both "
      "forms, the zero point, both footings", f"max |diff| = {d_c1:.1e}", d_c1 < 1e-9)

# ---- tables
P("\n  PREDICTED SLOPE d Delta/d log g_e (sigma from the observed) and the zero point, f_b(R500) = 0.13; ranges over f_b in the JSON")
for foot in A0:
    for geo, _ in GEOS:
        for ext in EXTS:
            R_ = RESA[f"{foot}/{geo}/0.13/{ext}"]
            P(f"   {foot:9s} r = {geo:10s} baryons {ext:8s} observed {R_['obs']:+.4f} +/- {R_['err']:.4f}; members beyond the "
              f"{'region edge' if MUTATE else 'capped edge'}: {R_['n_beyond_cap']}/{R_['n_members']}")
            for sname, row in R_["rows"].items():
                P(f"      {sname:46s} scalar {row['slope_scalar']:+.4f} ({row['sigma_scalar']:4.2f}s)  subtract {row['slope_subtract']:+.4f} "
                  f"({row['sigma_subtract']:4.2f}s)  zero point {row['zp_pred']:+.4f} vs {row['zp_obs']:+.4f} +/- {row['zp_err']:.4f} ({row['zp_sigma']:4.2f}s)")
OUT["numbers"]["clusters"] = RESA

# ---- K1, N1, V1-V3
fr = [RESA[f"{f}/R_proj/{f5}/extended"]["n_beyond_cap"] / RESA[f"{f}/R_proj/{f5}/extended"]["n_members"] for f in A0 for f5 in F500S]
check("K1 THE CAP MOVES CLUSTER MEMBERS OUT OF THEIR CLUSTER'S MOND REGION: >= 10% of the 314 members lie beyond the capped "
      "edge (committed geometry, every f_b(R500), both footings) -- MUTATE (no cap) must fail this",
      f"fraction beyond: {min(fr):.3f}-{max(fr):.3f}", min(fr) >= 0.10)
nf_keys = sorted(set(x["key"] for x in NEWFAIL))
remin = [RESA[k]["Re_over_RHI_min"] for k in RESA if RESA[k]["Re_over_RHI_min"] is not None]
check("N1 NO NEW FAILURE (pre-declared): every member beyond the cap keeps its disc switched on and its own MOND region out to "
      "at least R_HI, so none is Newtonian with its carrier cleared (every variant, both footings)",
      (f"{len(NEWFAIL)} member-variants fail ({len(nf_keys)} variants); " if NEWFAIL else "none fail; ")
      + (f"min R_e/R_HI over all beyond-cap members and variants = {min(remin):.1f}; median R_e "
         f"{min(RESA[k]['Re_kpc_median'] for k in RESA if RESA[k]['Re_kpc_median']):.0f}-"
         f"{max(RESA[k]['Re_kpc_median'] for k in RESA if RESA[k]['Re_kpc_median']):.0f} kpc" if remin else "no member beyond any edge"),
      len(NEWFAIL) == 0, load_bearing=False)
OUT["numbers"]["new_failures"] = NEWFAIL[:200]
capA = [k_ for k_ in RESA[f"canonical/R_proj/0.13/extended"]["rows"] if "operator A" in k_]
sigA = [RESA[k]["rows"][s][f] for k in RESA for s in capA for f in ("sigma_scalar", "sigma_subtract")]
worse = all(RESA[k]["rows"][s][f] > RESA[k]["rows"]["S1 MOND-sector switch, no cap"][f] + 1e-9
            for k in RESA for s in capA for f in ("sigma_scalar", "sigma_subtract"))
zpA = [RESA[k]["rows"][s]["zp_sigma"] for k in RESA for s in capA]
zp1 = [RESA[k]["rows"]["S1 MOND-sector switch, no cap"]["zp_sigma"] for k in RESA]
check("V1 THE CAP RESCUES THE CLUSTER SLOPE (pre-declared): every operator-A variant < 3 sigma from the observed slope",
      f"operator-A sigma range {min(sigA):.2f}-{max(sigA):.2f} (f_b x form x gap x geometry x extent x footing): scalar form "
      f"{min(RESA[k]['rows'][s]['sigma_scalar'] for k in RESA for s in capA):.2f}-{max(RESA[k]['rows'][s]['sigma_scalar'] for k in RESA for s in capA):.2f} "
      f"(uncapped {min(RESA[k]['rows']['S1 MOND-sector switch, no cap']['sigma_scalar'] for k in RESA):.2f}-"
      f"{max(RESA[k]['rows']['S1 MOND-sector switch, no cap']['sigma_scalar'] for k in RESA):.2f}), subtract form "
      f"{min(RESA[k]['rows'][s]['sigma_subtract'] for k in RESA for s in capA):.2f}-{max(RESA[k]['rows'][s]['sigma_subtract'] for k in RESA for s in capA):.2f} "
      f"(uncapped {min(RESA[k]['rows']['S1 MOND-sector switch, no cap']['sigma_subtract'] for k in RESA):.2f}-"
      f"{max(RESA[k]['rows']['S1 MOND-sector switch, no cap']['sigma_subtract'] for k in RESA):.2f})",
      max(sigA) < 3.0, load_bearing=False)
d_sig = [RESA[k]["rows"][s][f] - RESA[k]["rows"]["S1 MOND-sector switch, no cap"][f]
         for k in RESA for s in capA for f in ("sigma_scalar", "sigma_subtract")]
check("V2 THE CAP MAKES THE SLOPE WORSE (pre-declared): every operator-A variant sits further from the observed slope than "
      "the same variant uncapped (S1) -- members beyond the cap lose their deficit, the members inside keep it, and the "
      "predicted contrast between low and high external field grows",
      f"change in sigma, capped - uncapped: {min(d_sig):+.2f} to {max(d_sig):+.2f}", worse, load_bearing=False)
imp = max(-v for v in d_sig)
d_sub = [RESA[k]["rows"][s]["sigma_subtract"] - RESA[k]["rows"]["S1 MOND-sector switch, no cap"]["sigma_subtract"] for k in RESA for s in capA]
where_imp = sorted(set(k for k in RESA for s in capA for f in ("sigma_scalar", "sigma_subtract")
                       if RESA[k]["rows"][s][f] < RESA[k]["rows"]["S1 MOND-sector switch, no cap"][f] - 1e-12))
check("V2b (reported, POST-HOC: written after V2 failed, to describe its exception) no operator-A variant moves toward the data by "
      "more than 0.1 sigma, and every subtract-form variant moves away by more than 0.5 sigma",
      f"largest improvement {imp:.2f} sigma (only in: {', '.join(where_imp) or 'none'}); subtract-form change {min(d_sub):+.2f} to "
      f"{max(d_sub):+.2f} sigma", imp <= 0.1 and min(d_sub) > 0.5, load_bearing=False)
check("V3 (reported) THE ZERO POINT (members - field) UNDER THE CAP: operator-A sigma range against the uncapped range",
      f"capped {min(zpA):.2f}-{max(zpA):.2f} sigma; uncapped (S1) {min(zp1):.2f}-{max(zp1):.2f} sigma", True, load_bearing=False)
OUT["numbers"]["cluster_summary"] = dict(operatorA_sigma_range=[min(sigA), max(sigA)], capped_minus_uncapped=[min(d_sig), max(d_sig)],
                                         zp_operatorA=[min(zpA), max(zpA)], zp_uncapped=[min(zp1), max(zp1)],
                                         max_y_members=ymax_seen)
P(f"    (the kernel's argument at the members stays below y = {ymax_seen:.2f} < 2.337: nu_mono = nu_RAR there)")

# ============================================================================================ PART B dwarfs
banner("PART B -- the Local Volume dwarfs (k_contrarian_dwarfefe, N = 92) under the candidate")
d = KD.load(ups_v=2.0)
lsig = np.log10(np.array([g_["sig"] for g_ in d])); lM = np.log10(np.array([g_["Mb"] for g_ in d]))
lrh = np.log10(np.array([g_["rh"] / KD.PC for g_ in d]))
dmw = np.array([g_["dmw"] for g_ in d]); dm31 = np.array([g_["dm31"] for g_ in d])
gNe0 = np.array([g_["gNe"] for g_ in d])
fmw = np.where(np.isfinite(dmw) & (dmw > 0), G * KD.M_MW_BAR * MSUN / (np.where(np.isfinite(dmw) & (dmw > 0), dmw, 1.0) * KD.KPC) ** 2, 0.0)
f31 = np.where(np.isfinite(dm31) & (dm31 > 0), G * KD.M_M31_BAR * MSUN / (np.where(np.isfinite(dm31) & (dm31 > 0), dm31, 1.0) * KD.KPC) ** 2, 0.0)
host_mw = fmw >= f31
r_host = np.where(host_mw, dmw, dm31) * KD.KPC
M_host = np.where(host_mw, KD.M_MW_BAR, KD.M_M31_BAR)
RESB = {}; DW = {}
for foot, a0 in A0.items():
    lge = np.log10(KD.true_external_field(gNe0, a0) / a0)
    q = [lM, lrh, lM * lM, lrh * lrh, lM * lrh, lge]
    cobs, _ = KD.partial_slope(lsig, q); eobs = KD.boot_slope(lsig, q)

    def pred_slope(gNe_new):
        dd = [dict(g_, gNe=gg) for g_, gg in zip(d, gNe_new)]
        return KD.partial_slope(np.log10(KD.predict_sigma(dd, a0)), q)[0]

    row = dict(obs=float(cobs), err=float(eobs), committed=float(pred_slope(gNe0)), variants={}, candidate={})
    for cgm in (1.0, 1.5, 2.0):
        for scr in (None, 1.2):
            g_new = gNe0 * cgm
            if scr is not None:
                far = np.fmin(np.where(np.isfinite(dmw), dmw, np.inf), np.where(np.isfinite(dm31), dm31, np.inf)) > 1e3 * scr
                g_new = np.where(far, 1e-30, g_new)
            sp = pred_slope(g_new)
            row["variants"][f"cgm{cgm}_screen{scr}"] = dict(slope=float(sp), sigma=float(abs(cobs - sp) / eobs))
        # the candidate: each host's MOND-sector region (MW 6e10, M31 1.2e11, x cgm), the capped switch at z = 0
        edges = {}; vmaxd = {}; margin_min = np.inf; prof = {}
        for hname, Mh in (("MW", KD.M_MW_BAR * cgm), ("M31", KD.M_M31_BAR * cgm)):
            rr = np.geomspace(5.0 * KPC, 6.0 * MPC, 5000)
            e_, g_, D_, qb_ = ms_profile(rr, np.full_like(rr, Mh * MSUN), a0)
            on_, x_, thr_, vl2_ = switch_state(0.0, D_, qb_, g_, VCAP)
            edges[hname] = region_edge(rr, on_)[0]
            deep = (e_ / a0 < 0.1) & (rr < edges[hname])
            vmaxd[hname] = float(np.sqrt(np.max(vl2_[deep]))) if deep.any() else 0.0
            prof[hname] = (rr, x_ / thr_)
        inside = np.where(host_mw, r_host < edges["MW"], r_host < edges["M31"])
        for hname in ("MW", "M31"):
            sel = (host_mw if hname == "MW" else ~host_mw) & inside
            if sel.any():
                margin_min = min(margin_min, float(np.min(np.interp(np.log(r_host[sel]), np.log(prof[hname][0]), prof[hname][1]))))
        g_c = np.where(inside, gNe0 * cgm, 1e-30)
        sp = pred_slope(g_c)
        row["candidate"][f"cgm{cgm}"] = dict(slope=float(sp), sigma=float(abs(cobs - sp) / eobs), n_outside=int((~inside).sum()),
                                             edges_Mpc={k_: v_ / MPC for k_, v_ in edges.items()},
                                             vloc_max_deep_kms={k_: v_ / 1e3 for k_, v_ in vmaxd.items()},
                                             min_switch_margin_at_dwarfs=margin_min)
        DW[f"{foot}/{cgm}"] = row["candidate"][f"cgm{cgm}"]
        P(f"  {foot:9s} host baryons x{cgm:.1f}: MOND-sector edges MW {edges['MW'] / MPC:.2f} / M31 {edges['M31'] / MPC:.2f} Mpc; max v_loc in "
          f"the hosts' deep-MOND zones {vmaxd['MW'] / 1e3:.0f} / {vmaxd['M31'] / 1e3:.0f} km/s; switch margin x/thr at the dwarfs >= "
          f"{margin_min:.0f}; dwarfs outside {int((~inside).sum())} -> predicted {sp:+.4f} vs observed {cobs:+.4f} +/- {eobs:.4f} "
          f"({abs(cobs - sp) / eobs:.2f} sigma)")
    RESB[foot] = row
OUT["numbers"]["dwarfs"] = RESB
d_c2 = 0.0
for foot in A0:
    ref = XR4R["dwarfs"][foot]
    d_c2 = max(d_c2, abs(RESB[foot]["obs"] - ref["obs"]), abs(RESB[foot]["err"] - ref["err"]), abs(RESB[foot]["committed"] - ref["committed"]))
    for k_, v_ in ref["variants"].items():
        d_c2 = max(d_c2, abs(RESB[foot]["variants"][k_]["slope"] - v_["slope"]), abs(RESB[foot]["variants"][k_]["sigma"] - v_["sigma"]))
check("C2 CONTROL: XR4's committed dwarf numbers reproduced (statistic C; host baryons x1/x1.5/x2, with and without the 1.2 Mpc "
      "screen; both footings)", f"max |diff| = {d_c2:.1e}", d_c2 < 1e-9)
vm = max(max(v["vloc_max_deep_kms"].values()) for v in DW.values())
mm = min(v["min_switch_margin_at_dwarfs"] for v in DW.values())
check("D1 THE CAP BINDS NOWHERE IN THE LOCAL GROUP'S HOST REGIONS: v_loc < v_cap in every host's deep-MOND zone (hosts x1-x2), and "
      "every dwarf's position is switched ON (x above the capped threshold) inside its host's MOND-sector region",
      f"max v_loc (deep zone) {vm:.0f} km/s vs 325; min x/threshold at the dwarfs {mm:.2f}; dwarfs outside their host's region: "
      + ", ".join(f"{k}: {v['n_outside']}" for k, v in DW.items()),
      vm < 325.0 and mm > 1.0)
sigD = [v["sigma"] for f in RESB for v in RESB[f]["candidate"].values()]
check("D2 THE DWARF LIABILITY STANDS under the candidate (pre-declared: every variant >= 3 sigma) -- the MOND-sector reading and "
      "the cap leave the in-region EFE of the MW and M31 baryons exactly as XR4 scored it",
      f"sigma range {min(sigD):.2f}-{max(sigD):.2f}", min(sigD) >= 3.0, load_bearing=False)
# the two EFE samples in quadrature, as XR4 quoted them (treated as independent; like footing with like footing)
comb = {}
for foot in A0:
    cl = [RESA[k]["rows"][s][f] for k in RESA if k.startswith(foot + "/") for s in capA for f in ("sigma_scalar", "sigma_subtract")]
    cl1 = [RESA[k]["rows"]["S1 MOND-sector switch, no cap"][f] for k in RESA if k.startswith(foot + "/") for f in ("sigma_scalar", "sigma_subtract")]
    dw = [v["sigma"] for v in RESB[foot]["candidate"].values()]
    comb[foot] = dict(capped=[math.hypot(min(cl), min(dw)), math.hypot(max(cl), max(dw))],
                      uncapped=[math.hypot(min(cl1), min(dw)), math.hypot(max(cl1), max(dw))])
OUT["numbers"]["efe_combined"] = comb
check("D3 (reported) THE TWO EFE SAMPLES IN QUADRATURE (XR4's convention: cluster slope (+) dwarf statistic, independent samples)",
      "; ".join(f"{f}: capped operator A {v['capped'][0]:.1f}-{v['capped'][1]:.1f} sigma, uncapped {v['uncapped'][0]:.1f}-"
                f"{v['uncapped'][1]:.1f} sigma" for f, v in comb.items()), True, load_bearing=False)

# ============================================================================================ PART C Coma UDGs
banner("PART C -- the eleven Coma ultra-diffuse galaxies (L23's pipeline, rebuilt) under the candidate")
G23 = 6.674e-11; MS23 = 1.989e30; kpc23 = 3.0857e19; Mpc23 = 3.0857e22; m_p = 1.67262e-27; keV = 1.602176634e-16
A0L = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
S_SAT, D_SAT = 2.540, 0.6476


def Delta(s):
    s = np.asarray(s, float); sc = np.minimum(s, S_SAT)
    dd = np.where(sc > 0, sc / np.expm1(np.sqrt(np.maximum(sc, 1e-300))), 0.0)
    return np.where(s > S_SAT, D_SAT, dd)


def nus(y):
    y = max(float(y), 1e-14); return float(1.0 + Delta(np.array(y)) / y)


def y_of_x(x):
    x = float(x)
    if x <= 0: return 0.0
    return brentq(lambda yy: yy * nus(yy) - x, 1e-14, 1e8, xtol=1e-16, rtol=1e-14)


def Lslope(y, dd=1e-5):
    return (math.log(nus(y * (1 + dd))) - math.log(nus(y * (1 - dd)))) / (2 * dd)


rows_ = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", "freundlich2022_coma_udgs.tsv"))
         if l.strip() and not l.startswith("#")]
hd = {h_: i for i, h_ in enumerate(rows_[0])}
UDG = []
for r_ in rows_[1:]:
    f_ = lambda k: float(r_[hd[k]])
    u = dict(name=r_[hd["name"]], dproj=f_("d_kpc"), dmean=f_("dmean_kpc"), L=f_("L_1e8") * 1e8, Re=f_("Re_kpc"), ML=f_("ML"),
             sig=f_("sig"), elgb=f_("elgbar"), elgo=f_("elgobs"))
    u["r12"] = 4.0 / 3.0 * u["Re"] * kpc23; u["Mst"] = u["L"] * u["ML"] * MS23
    u["gobs"] = 3.0 * (u["sig"] * 1e3) ** 2 / u["r12"]; u["gbar"] = G23 * (u["Mst"] / 2.0) / u["r12"] ** 2
    u["err"] = math.hypot(u["elgo"], u["elgb"])
    UDG.append(u)


def wmean(off, err):
    w = 1.0 / np.asarray(err) ** 2
    return float(np.sum(w * np.asarray(off)) / np.sum(w)), float(1.0 / math.sqrt(np.sum(w)))


def m_nfw(x): return math.log(1 + x) - x / (1 + x)


def g_nfw(r_kpc, M200=1.3e15, c=5.0, R200_kpc=2900.0):
    return G23 * M200 * m_nfw(c * r_kpc / R200_kpc) / m_nfw(c) * MS23 / (r_kpc * kpc23) ** 2


hL = 0.674; H0L = 100 * hL * 1e3 / Mpc23; ZCOMA = 0.0231
rho_cL = 3 * H0L ** 2 / (8 * math.pi * G23) * (0.315 * (1 + ZCOMA) ** 3 + 0.685)
R200_true = (3 * 1.3e15 * MS23 / (4 * math.pi * 200 * rho_cL)) ** (1 / 3.0) / Mpc23
kT_C, rc_C, bet_C, mu_mol = 8.6 * keV, 276.0 * kpc23, 0.71, 0.6


def g_beta(r_kpc):
    r = r_kpc * kpc23; return (3 * bet_C * kT_C / (mu_mol * m_p)) * r / (r ** 2 + rc_C ** 2)


MODELS = {"h9 NFW (R200 2900 kpc)": g_nfw, f"NFW self-consistent (R200 {R200_true * 1e3:.0f} kpc)": (lambda r: g_nfw(r, R200_kpc=R200_true * 1e3)),
          "Freundlich+2022 beta-model": g_beta}
BETA = "Freundlich+2022 beta-model"
coma = [c for c in cls if c["name"].startswith("PSZ2 G057.80+88.00")][0]
R500C = coma["r500"] / KPC                                             # kpc (PSZ2, as KC reads it)


def run(a0, gfn, rkey, arg="newtonian", coupling="sphere", ml_scale=1.0, sig_scale=1.0, dist_scale=1.0, r_over=None,
        f500=0.13, efield=None):
    """L23's run() (L23_udg_verify.py:341-365), plus two arguments: 'baryonic' (L361: nu reads the host's in-region BARYONS,
    e_N = f_b(r) g_true, no closure inversion) and 'given' (a transmitted field per UDG, efield[i] in m/s^2)."""
    oi, oe, er, xs = [], [], [], []
    for i, u in enumerate(UDG):
        r = r_over if r_over is not None else u[rkey]
        gobs = u["gobs"] * sig_scale ** 2 / dist_scale; gbar = u["gbar"] * ml_scale
        xobs = gfn(r) / a0
        if arg == "newtonian": ya = y_of_x(xobs)
        elif arg == "observed": ya = xobs
        elif arg == "baryonic": ya = float(fb_profile(np.array(r / R500C), f500)) * xobs
        else: ya = efield[i] / a0
        yi = gbar / a0; ytot = yi + ya; fext = ya / ytot
        cpl = nus(ytot) * (1 + fext * Lslope(ytot) / 3) if coupling == "sphere" else nus(ytot)
        oi.append(math.log10(gobs) - math.log10(nus(gbar / a0) * gbar))
        oe.append(math.log10(gobs) - math.log10(cpl * gbar))
        er.append(u["err"]); xs.append(ya)
    mi, si = wmean(oi, er); me, se = wmean(oe, er)
    return dict(mi=mi, si=si, me=me, se=se, oi=np.array(oi), oe=np.array(oe), err=np.array(er), ya=np.array(xs))


def budget(arm, extra=None):
    """L23's systematic budget (L23:417-481), every EFE-dependent entry recomputed on the given arm."""
    base = arm(A0L["canonical"], BETA, "dmean")["me"]
    S = {}
    S["stellar M/L and IMF"] = abs(arm(A0L["canonical"], BETA, "dmean", ml_scale=1.41)["me"] - base)
    rr_ = [2 * math.log10(math.sqrt(nus(u["gbar"] / A0L["canonical"]) * u["gbar"] * u["r12"] / 3.0)
                          / (((4 / 81.) * G23 * u["Mst"] * A0L["canonical"]) ** 0.25)) for u in UDG]
    S["sigma -> acceleration estimator"] = float(np.std(rr_) + abs(np.mean(rr_)))
    S["aperture + orbital anisotropy"] = 0.12
    sig_inst = 2.99792458e5 / (4800 * 2.3548)
    prop = [(sig_inst / u["sig"]) ** 2 * 0.05 for u in UDG if u["name"] not in ("DF44", "DFX1")]
    S["instrumental (9 of 11)"] = float(2 * np.median(prop) / math.log(10)) * (9 / 11.)
    spread = [arm(A0L["canonical"], m_, k_)["me"] for m_ in MODELS for k_ in ("dproj", "dmean")]
    S["Coma mass model + 3-D position"] = float((max(spread) - min(spread)) / 2)
    S["distance to Coma (+-5%)"] = abs(arm(A0L["canonical"], BETA, "dmean", dist_scale=1.05)["me"] - base)
    S["a0 footing"] = abs(arm(A0L["alt"], BETA, "dmean")["me"] - base)
    if extra: S.update(extra)
    return S, math.sqrt(sum(v_ ** 2 for v_ in S.values()))


arm_L23 = lambda a0, m_, k_, **kw: run(a0, MODELS[m_], k_, "newtonian", "sphere", **kw)
BEST = {f: arm_L23(A0L[f], BETA, "dmean") for f in A0L}
S23, syst23 = budget(arm_L23)
tot23 = math.sqrt(BEST["canonical"]["se"] ** 2 + syst23 ** 2)
sig23 = BEST["canonical"]["me"] / tot23; sig23a = BEST["alt"]["me"] / math.sqrt(BEST["alt"]["se"] ** 2 + syst23 ** 2)
df44 = wmean(BEST["canonical"]["oe"][[0]], BEST["canonical"]["err"][[0]])
inf23 = run(A0L["canonical"], g_beta, "dmean", r_over=9000.0)
check("C3 CONTROL: L23's committed Coma numbers are reproduced -- +1.159 / +1.112 dex (beta-model, Einasto 3-D, closure-"
      "inverted field, isotropic coupling), systematic floor 0.227 dex, 4.9 / 4.7 sigma, DF44 alone +0.938 +- 0.139, first "
      "infall at 9 Mpc +0.635", f"{BEST['canonical']['me']:+.4f} / {BEST['alt']['me']:+.4f}; floor {syst23:.4f}; {sig23:.2f} / "
      f"{sig23a:.2f} sigma; DF44 {df44[0]:+.4f} +- {df44[1]:.4f}; 9 Mpc {inf23['me']:+.4f}",
      abs(BEST["canonical"]["me"] - 1.159) < 6e-4 and abs(BEST["alt"]["me"] - 1.112) < 6e-4 and abs(syst23 - 0.227) < 6e-4
      and abs(sig23 - 4.9) < 0.05 and abs(sig23a - 4.7) < 0.05 and abs(df44[0] - 0.938) < 6e-4 and abs(df44[1] - 0.139) < 6e-4
      and abs(inf23["me"] - 0.635) < 6e-4)

# ---- Coma's MOND-sector region under the candidate (each mass model; the host's baryons = f_b(r) x its total mass)
COMA = {}
for foot, a0 in A0L.items():
    for mname, gfn in MODELS.items():
        for f500 in F500S:
            rk = np.geomspace(50.0, 40000.0, 5000)                              # kpc
            Mtot = np.array([gfn(x_) for x_ in rk]) * (rk * kpc23) ** 2 / G23
            Mbk = fb_profile(rk / R500C, f500) * Mtot
            rm = rk * kpc23
            e_, g_, D_, qb_ = ms_profile(rm, Mbk, a0)
            on_, *_ = switch_state(ZCOMA, D_, qb_, g_, VCAP)
            onu, *_ = switch_state(ZCOMA, D_, qb_, g_, math.inf)
            COMA[f"{foot}/{mname}/{f500}"] = dict(r_cap_kpc=region_edge(rm, on_)[0] / kpc23, r_uncapped_kpc=region_edge(rm, onu)[0] / kpc23,
                                                  prof=(rm, Mbk, e_, g_, D_, qb_))
rc_all = [v["r_cap_kpc"] for v in COMA.values()]
dmax_pos = max(max(u["dproj"], u["dmean"]) for u in UDG)
P(f"  Coma's MOND-sector region at z = {ZCOMA} ({'no cap' if MUTATE else 'capped'}): edge {min(rc_all) / 1e3:.2f}-{max(rc_all) / 1e3:.2f} Mpc "
  f"over 3 mass models x 3 f_b x 2 footings (uncapped: {min(v['r_uncapped_kpc'] for v in COMA.values()) / 1e3:.1f}-"
  f"{max(v['r_uncapped_kpc'] for v in COMA.values()) / 1e3:.1f} Mpc); the UDGs' farthest position (projected or Einasto 3-D) "
  f"{dmax_pos / 1e3:.2f} Mpc")
check("U1 ALL ELEVEN COMA UDGs LIE INSIDE COMA'S (CAPPED) MOND REGION -- at the projected and at the Einasto 3-D positions, for "
      "every Coma mass model, f_b and footing -- so under the candidate the EFE acts on them (case a)",
      f"nearest edge {min(rc_all) / 1e3:.2f} Mpc vs farthest UDG {dmax_pos / 1e3:.2f} Mpc", min(rc_all) > dmax_pos)

# ---- the candidate's EFE on the UDGs: the host's in-region BARYONS, no closure inversion
arm_C = lambda a0, m_, k_, f500=0.13, **kw: run(a0, MODELS[m_], k_, "baryonic", "sphere", f500=f500, **kw)
CAND = {f"{f}/{f5}": arm_C(A0L[f], BETA, "dmean", f500=f5) for f in A0L for f5 in F500S}
fbspread = (max(CAND[f"canonical/{f5}"]["me"] for f5 in F500S) - min(CAND[f"canonical/{f5}"]["me"] for f5 in F500S)) / 2
SC, systC = budget(arm_C, extra={"f_b(R500) template 0.10-0.157 (new)": fbspread})
totC = math.sqrt(CAND["canonical/0.13"]["se"] ** 2 + systC ** 2)
sigC = CAND["canonical/0.13"]["me"] / totC
sigCa = CAND["alt/0.13"]["me"] / math.sqrt(CAND["alt/0.13"]["se"] ** 2 + systC ** 2)
efeC = CAND["canonical/0.13"]["me"] - CAND["canonical/0.13"]["mi"]
df44C = wmean(CAND["canonical/0.13"]["oe"][[0]], CAND["canonical/0.13"]["err"][[0]])
ratio_e = np.array([CAND["canonical/0.13"]["ya"][i] / y_of_x(g_beta(u["dmean"]) / A0L["canonical"]) for i, u in enumerate(UDG)])
P("  the external field in nu's argument, candidate (host baryons, Newtonian) / L23 (closure-inverted total field), per UDG: "
  + ", ".join(f"{v_:.2f}" for v_ in ratio_e))
P(f"  {'arm':70s} {'offset':>8s} {'sigma':>6s}")
P(f"  {'L23 (committed): closure-inverted total field, beta-model, Einasto 3-D, canonical':70s} {BEST['canonical']['me']:+8.3f} {sig23:6.2f}")
P(f"  {'L23 (committed), alt':70s} {BEST['alt']['me']:+8.3f} {sig23a:6.2f}")
for f5 in F500S:
    for foot in A0L:
        R_ = CAND[f"{foot}/{f5}"]
        s_ = R_["me"] / math.sqrt(R_["se"] ** 2 + systC ** 2)
        P(f"  {'candidate (in-region baryons, f_b(R500) = ' + str(f5) + '), beta-model, Einasto 3-D, ' + foot:70s} {R_['me']:+8.3f} {s_:6.2f}")
spreadC = {f"{m_}/{k_}": arm_C(A0L["canonical"], m_, k_)["me"] for m_ in MODELS for k_ in ("dproj", "dmean")}
P("  candidate, canonical, f_b = 0.13, by mass model / position: " + "; ".join(f"{k}: {v:+.3f}" for k, v in spreadC.items()))
P("  candidate systematic budget (L23's entries recomputed on this arm): " + "; ".join(f"{k} {v:.3f}" for k, v in SC.items())
  + f"  -> floor {systC:.3f} dex (L23: {syst23:.3f})")
P(f"  candidate: DF44 alone {df44C[0]:+.3f} +- {df44C[1]:.3f}; the EFE term alone (offset minus isolated) {efeC:+.3f} dex; "
  f"isolated offset (no EFE at all) {CAND['canonical/0.13']['mi']:+.3f} / {CAND['alt/0.13']['mi']:+.3f} dex = "
  f"{CAND['canonical/0.13']['mi'] / totC:.2f} sigma")
allC = [CAND[k]["me"] / math.sqrt(CAND[k]["se"] ** 2 + systC ** 2) for k in CAND]
# the EFE term alone (the framework's SEP violation, g_obs cancels), with L23's own budget for it (L23:546-558), recomputed
_ml = arm_C(A0L["canonical"], BETA, "dmean", ml_scale=1.41)
_sp = [arm_C(A0L["canonical"], m_, k_)["me"] - arm_C(A0L["canonical"], m_, k_)["mi"] for m_ in MODELS for k_ in ("dproj", "dmean")]
_fb = [CAND[f"canonical/{f5}"]["me"] - CAND[f"canonical/{f5}"]["mi"] for f5 in F500S]
sys_efeC = math.sqrt(abs((_ml["me"] - _ml["mi"]) - efeC) ** 2 + ((max(_sp) - min(_sp)) / 2) ** 2
                     + abs((CAND["alt/0.13"]["me"] - CAND["alt/0.13"]["mi"]) - efeC) ** 2 + ((max(_fb) - min(_fb)) / 2) ** 2)
sig_efeC = efeC / math.sqrt(CAND["canonical/0.13"]["se"] ** 2 + sys_efeC ** 2)
P(f"  the EFE term alone (the SEP violation itself; g_obs cancels): candidate {efeC:+.3f} dex with its own floor {sys_efeC:.3f} -> "
  f"{sig_efeC:.1f} sigma (L23: +0.763 dex, 6.0 sigma)")
check("U2 THE UDG LIABILITY FLIPS under the candidate (pre-declared: the central arm -- beta-model, Einasto 3-D, f_b(R500) = "
      "0.13 -- is < 3 sigma on both footings with the systematic floor recomputed on the candidate's arm)",
      f"offset {CAND['canonical/0.13']['me']:+.3f} / {CAND['alt/0.13']['me']:+.3f} dex = {sigC:.2f} / {sigCa:.2f} sigma "
      f"(L23: {BEST['canonical']['me']:+.3f} / {BEST['alt']['me']:+.3f} = {sig23:.2f} / {sig23a:.2f}); over f_b and footing "
      f"{min(allC):.2f}-{max(allC):.2f} sigma", sigC < 3.0 and sigCa < 3.0, load_bearing=False)

# ---- the first-infall radius (9 Mpc) under the candidate
INF = {}
for foot, a0 in A0L.items():
    for mname in MODELS:
        for f500 in F500S:
            Cm = COMA[f"{foot}/{mname}/{f500}"]; rm, Mbk, e_, g_, D_, qb_ = Cm["prof"]
            r9 = 9000.0 * kpc23; rcap = Cm["r_cap_kpc"] * kpc23
            at = lambda arr: float(np.interp(math.log(r9), np.log(rm), arr))
            if r9 <= rcap:
                INF[f"{foot}/{mname}/{f500}"] = dict(beyond=False, T_max=1.0); continue
            Tm = 0.0; efs = {}
            for gname, minv in GAPS:
                ef = []
                for u in UDG:
                    don, Re, reach = galaxy_region(u["Mst"], u["r12"], ZCOMA, a0, at(e_), at(g_), at(D_), at(qb_), VCAP)
                    Mcap = float(np.interp(math.log(rcap), np.log(rm), Mbk)); rho = r9 - Re
                    ef.append(G * Mcap / rho ** 2 * transmit(rho, rcap, minv))
                efs[gname] = ef; Tm = max(Tm, max(ef) / at(e_))
            INF[f"{foot}/{mname}/{f500}"] = dict(beyond=True, T_max=Tm,
                                                 offsets={gn: run(a0, MODELS[mname], "dmean", "given", "sphere", r_over=9000.0,
                                                                  efield=ef)["me"] for gn, ef in efs.items()})
nb9 = sum(1 for v in INF.values() if v["beyond"])
ib = INF[f"canonical/{BETA}/0.13"]
P(f"  first-infall radius 9 Mpc: beyond Coma's {'capped ' if not MUTATE else ''}edge in {nb9}/{len(INF)} cases; "
  + (f"canonical beta f_b 0.13 offsets by gap: " + ", ".join(f"{k}: {v:+.3f}" for k, v in ib["offsets"].items())
     + f" (max transmitted fraction {ib['T_max']:.1e}); L23 at 9 Mpc +{inf23['me']:.3f}, 2.7 sigma" if ib["beyond"] else
     f"inside the region: the EFE acts there (candidate arm at 9 Mpc {arm_C(A0L['canonical'], BETA, 'dmean', r_over=9000.0)['me']:+.3f})"))
check("U3 THE CAP REMOVES COMA'S FIELD AT THE FIRST-INFALL RADIUS: 9 Mpc lies beyond Coma's capped edge for every mass model, "
      "f_b and footing, so a UDG observed there would be isolated -- MUTATE (no cap) must fail this",
      f"{nb9}/{len(INF)} cases beyond the edge", nb9 == len(INF))

# ---- the carrier inside r_1/2, and the re-equilibration clock (reported)
ret = max(L388R["retention_by_mass"][k]["2.5e+14-1.0e+17"][0] for k in L388R["retention_by_mass"])
dmx = 0.0
for i, u in enumerate(UDG):
    r = u["dmean"]; dr = 1.0
    Mt = lambda x_: g_beta(x_) * (x_ * kpc23) ** 2 / G23
    rho_t = (Mt(r + dr) - Mt(r - dr)) / (2 * dr * kpc23) / (4 * math.pi * (r * kpc23) ** 2)
    rho_c_ = ret * (1 - float(fb_profile(np.array(r / R500C), 0.10))) * rho_t
    g_car = 4 * math.pi / 3 * G23 * rho_c_ * u["r12"]
    ya = CAND["canonical/0.13"]["ya"][i]; yi = u["gbar"] / A0L["canonical"]; yt = yi + ya
    cpl = nus(yt) * (1 + ya / yt * Lslope(yt) / 3)
    dmx = max(dmx, math.log10(1 + g_car / (cpl * u["gbar"])))
check("U4 (reported, pre-declared bound 0.01 dex) Coma's retained carrier (L388: up to %.2f of it kept in >= 2.5e14 hosts) inside a "
      "UDG's r_1/2 lowers the offset by < 0.01 dex: a 575-650 km/s kick leaves no UDG-bound carrier, and the cluster's smooth "
      "carrier is ~uniform across a UDG (its isotropic tidal compression, (4 pi/3) G rho_car r)" % ret,
      f"largest shift {dmx:.3f} dex (at the Einasto 3-D radius, f_b floor 0.10), against the candidate's +{CAND['canonical/0.13']['me']:.3f} "
      f"dex offset", dmx < 0.01, load_bearing=False)
tcr = []
rcb = COMA[f"canonical/{BETA}/0.13"]["r_cap_kpc"]
for u in UDG:
    tdyn = u["r12"] / (u["sig"] * 1e3) / 3.156e16
    tc = (rcb - u["dmean"]) * kpc23 / 3.0e6 / 3.156e16
    tcr.append(tc / tdyn)
P(f"  re-equilibration: at <= 3000 km/s a UDG needs >= {min(tcr):.1f}-{max(tcr):.1f} of its own dynamical times (r_1/2/sigma) to fall from "
  f"Coma's capped edge ({rcb / 1e3:.2f} Mpc) to its Einasto 3-D radius -- a first-infall reading needs it to still carry its "
  f"isolated dispersion after that")
OUT["numbers"]["udg"] = dict(L23=dict(me=[BEST["canonical"]["me"], BEST["alt"]["me"]], floor=syst23, sigma=[sig23, sig23a],
                                      df44=list(df44), first_infall=inf23["me"], budget=S23),
                             candidate=dict(me={k: v["me"] for k, v in CAND.items()}, mi={k: v["mi"] for k, v in CAND.items()},
                                            floor=systC, sigma=[sigC, sigCa], sigma_range=[min(allC), max(allC)],
                                            efe_term=efeC, efe_term_floor=sys_efeC, efe_term_sigma=sig_efeC,
                                            df44=list(df44C), by_model_position=spreadC, budget=SC,
                                            field_ratio_to_L23=list(ratio_e)),
                             coma_edges_kpc={k: dict(capped=v["r_cap_kpc"], uncapped=v["r_uncapped_kpc"]) for k, v in COMA.items()},
                             first_infall=INF, carrier_shift_max_dex=dmx, retention_used=ret,
                             tcross_over_tdyn=[float(min(tcr)), float(max(tcr))])

# ============================================================================================ summary
banner("SUMMARY")
cS1 = RESA["canonical/R_proj/0.13/extended"]["rows"]["S1 MOND-sector switch, no cap"]
cS2 = RESA["canonical/R_proj/0.13/extended"]["rows"]["S2 capped, operator A, gap Dirichlet"]
cS4 = RESA["canonical/R_proj/0.13/extended"]["rows"]["S4 capped, operator A, gap 1/m=0.5"]
EDc = EDGES['canonical/0.13/extended']
P(f"""  CLUSTER-INFALL BTFR (N = 314).  {'NO CAP (MUTATE): every member inside its cluster region; the numbers are XR4s.' if MUTATE else 'The capped MOND-sector edge sits at ' + format(min(v['capped'] for v in EDc.values()), '.2f') + '-' + format(max(v['capped'] for v in EDc.values()), '.2f') + ' Mpc for EVERY cluster (v_loc at the edge ' + format(min(v['vloc_edge_kms'] for v in EDc.values()), '.0f') + '-' + format(max(v['vloc_edge_kms'] for v in EDc.values()), '.0f') + ' km/s).'}
  {RESA['canonical/R_proj/0.13/extended']['n_beyond_cap']} of 314 members lie beyond it (committed geometry); each keeps its own region (>= {min(remin) if remin else float('nan'):.1f} R_HI): no Newtonian member.
  Canonical, f_b 0.13, committed geometry -- slope, scalar / subtract form: uncapped {cS1['slope_scalar']:+.4f} ({cS1['sigma_scalar']:.2f}s) / {cS1['slope_subtract']:+.4f} ({cS1['sigma_subtract']:.2f}s);
  capped, Dirichlet gap {cS2['slope_scalar']:+.4f} ({cS2['sigma_scalar']:.2f}s) / {cS2['slope_subtract']:+.4f} ({cS2['sigma_subtract']:.2f}s); capped, 1/m = 0.5 {cS4['slope_scalar']:+.4f} ({cS4['sigma_scalar']:.2f}s) / {cS4['slope_subtract']:+.4f} ({cS4['sigma_subtract']:.2f}s).
  Over every operator-A variant: slope {min(sigA):.2f}-{max(sigA):.2f} sigma (change vs uncapped {min(d_sig):+.2f} to {max(d_sig):+.2f}); zero point {min(zpA):.2f}-{max(zpA):.2f} sigma
  (uncapped {min(zp1):.2f}-{max(zp1):.2f}).  The cap turns the external-field effect into a STEP at r_cap: members inside keep the
  deficit, members beyond lose it, so the predicted slope steepens while the mean offset shrinks.  Operator B (the PM phantom,
  all baryons in nu) screens nothing: its numbers are the uncapped ones.
  LOCAL VOLUME DWARFS (N = 92): the cap binds nowhere in the MW/M31 regions; statistic C unchanged, {min(sigD):.2f}-{max(sigD):.2f} sigma.
  EFE samples combined (quadrature, XR4's convention): {', '.join(f"{f} {v['capped'][0]:.1f}-{v['capped'][1]:.1f}" for f, v in comb.items())} sigma capped (uncapped {', '.join(f"{v['uncapped'][0]:.1f}-{v['uncapped'][1]:.1f}" for v in comb.values())}).
  COMA UDGs: inside Coma's capped region at every measured position; the candidate's EFE reads Coma's baryons only (L361), not
  L23's closure-inverted total field (0.25-0.50 of it): {CAND['canonical/0.13']['me']:+.3f} / {CAND['alt/0.13']['me']:+.3f} dex = {sigC:.2f} / {sigCa:.2f} sigma (L23 {BEST['canonical']['me']:+.3f} / {BEST['alt']['me']:+.3f} = {sig23:.2f} / {sig23a:.2f});
  the EFE term alone {efeC:+.3f} dex, {sig_efeC:.1f} sigma (L23 6.0).  At the first-infall radius (9 Mpc) the cap removes Coma's field
  entirely (isolated, +{CAND['canonical/0.13']['mi']:.3f} dex, {CAND['canonical/0.13']['mi'] / totC:.1f} sigma) -- a hypothesis about the sample, not a repair.""")

n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"] = len(CH); OUT["n_fail_load_bearing"] = n_lb_fail; OUT["elapsed_s"] = time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=float)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(0 if n_lb_fail == 0 else 1)
