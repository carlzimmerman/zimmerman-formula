#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR7 -- ONE NUMBER FOR THE KICK AND THE CAP?  The carrier's retention transition against MS3's MOND-region cap.

THE CLAIM UNDER TEST (a parallel session's synthesis, 2026-09-26; not committed anywhere): the carrier converts at shell
crossing with a kick v_k ~ 600 km/s (L388's pooled window 575-650 km/s); every system whose escape speed is below what the
kick needs to unbind the daughters loses its carrier, deeper wells keep most of it; cosmic shear scored resolution-free
(MS3 K1) needs MOND regions capped at ~1.75 Mpc at z = 0.5, v_cap ~ 325 km/s (M_b ~ 9e11 Msun via v^4 = G M a0); the cap,
~250-325 km/s, is about half the kick speed and EQUALS the escape speed of the systems the kick empties, so one number
would set both.

REVIEWED (read-only; nothing is imported or executed from them, and no simulation is run):
  real_research/dark_sector_2026/L388_linear_gate_pooled_results.json            per-halo retention, p = 1, x_c0 = 2.5
  real_research/dark_sector_2026/L380_pooled_window_fixed_cell_clearing_results.json   the same at p = 2, x_c0 = 2
  real_research/dark_sector_2026/L366_triggered_carrier_cluster_retention_results.json Newtonian, one box, 550-850 km/s
  real_research/dark_sector_2026/L375_..._results.json, L376_..._results.json (+ their host constants, read as text)
  real_research/dark_sector_2026/L321_carrier_z0_retention_gate.py (its unbinding criterion, read as text; L371's S2 shape)
  real_research/mond_sector_gate_2026/MS3_cosmic_shear_bound_mond_sector_results.json    K1 rows, K1_design, U1
  real_research/generated_phantom_2026/GP0_bound_baryon_census.py  (M_bound 'observed', re-implemented, checked on MS3 U1)
  fable_independent_2026/lean_2026/I27_kick_escape.lean  (kick_unbinds' hypothesis, read as text)

WHAT IS COMPUTED
  T  THE RETENTION TRANSITION in L388's per-halo data (40 peaks x 3 boxes; eps = carrier mass within 1 Mpc/h over LCDM's,
     z = 0, M = LCDM mass within 1 Mpc/h in Msun/h): the mass where the retention crosses 50% and the X-COP floor
     (canonical 0.286, alt 0.220: L354's rows via L366's eps_bounds), for each kick 575-650 km/s.  Three estimators: the
     lanes' own binned medians (L371's bins, as L388 and MS3 use them), a 3-parameter logistic in ln v_c, and isotonic
     regression; a halo bootstrap (1000) and per-box values.  Halos below 6e13 (two peaks) are outside L371's bins and are
     reported, not fitted.  L380 (the p = 2 cell) is scored separately (cells are never pooled); L366 gives the kick
     scaling over 550-850 km/s (Newtonian, one box, same peaks as L388's box 7).
  V  EACH CROSSING AS VELOCITIES, in the lanes' conventions: v_c = sqrt(G M/R) at R = 1 Mpc/h (model-free; the mesh's
     81-cell sphere, R_eff = 1.048 Mpc/h, as a systematic); NFW with Dutton-Maccio 2014 c(M) (L321/L375/MS3), M200c, v200,
     v_max; escape speeds with Phi(inf) = 0 (I27's definition) and with Phi(2 r200) (L371-S3's marginally-bound
     reference) at 1 Mpc/h, r200, the trigger radius (NFW density = rho_bar + (10/3) rho_c, i.e. x~ = 5, I27's
     self_limiting_trigger) and the centre; the baryons' deep-MOND flat speed (G M_b a0)^(1/4) -- v_cap's own velocity
     type -- for cosmic f_b and GP0's observed bound baryons, both footings.
  K  THE KICK PHYSICS: the exact isotropic-kick unbound fraction; what I27's v_k > |v_o| + v_esc is; three orbit classes;
     and an idealised STATIC single-halo model (NFW, isotropic Jeans, all carrier inside r200 decays at once in the
     pre-decay potential, no assembly) -- the picture in which "half the kick" appears.
  G  THE EMPTIED END: L375's decayed-daughter retention around the KiDS hosts and L376's emptied interiors, with host v200.
  S  MS3's OWN K1 ROWS as the one-number test: its committed 'cleared<1e13' scenario is a retention step at M200 = 1e13
     Msun, v200(z = 0.5) = 337 km/s -- a transition AT the cap scale.
CHECKS
  C1 CONTROL: L388's and L380's pooled and per-box X-COP medians and counts, their L371-bin medians and counts, and L366's
     cluster medians are reproduced EXACTLY from the per-halo lists, before any of them is used.
  C2 CONTROL: MS3's v_cap (325.28 km/s), M_b,cap (9.008e11 Msun) and KiDS v_f are reproduced from r_cap, H(0.5), x_lin and
     a0 (to 1e-9), and the re-implemented GP0 M_bound reproduces MS3's committed U1 bound baryons (to 1e-9).
  C3 CONTROL: the closed-form unbound fraction matches a Monte Carlo over kick directions (max |diff| < 0.005), and I27's
     hypothesis v_k > |v_o| + v_esc is exactly its f = 1 edge on a 40x40x40 grid.
  T0 THE TRANSITION EXISTS (the load-bearing measurement MUTATE must break): for every L388 kick the pooled retention of
     the >= 6e13 halos rises with mass (Spearman rho > 0 at p < 1e-3), the binned medians cross 50% inside the bins, and
     the logistic 50% point lies inside the data.
  V1 (reported either way) THE CLAIM: does the 50% transition, in any circular-speed convention, touch the cap band?
MUTATE=1 scrambles the retention-mass pairing (one fixed permutation of halos, every dataset) after C1: T0 must FAIL (rc=1).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR7_kick_escape_vs_cap.py
Single-threaded, numpy/scipy only, ~1 min.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, time, re, ast, warnings
import numpy as np
from scipy.optimize import brentq, curve_fit
from scipy.stats import spearmanr

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR7_kick_escape_vs_cap"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR7", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 116); P(t); P("=" * 116)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the retention-mass pairing is scrambled after C1 -- T0 must FAIL ***")

# ============================================================================================ inputs (read-only)
DS = os.path.join(REPO, "real_research", "dark_sector_2026")
jl = lambda *p: json.load(open(os.path.join(*p)))
L388 = jl(DS, "L388_linear_gate_pooled_results.json")["numbers"]
L380 = jl(DS, "L380_pooled_window_fixed_cell_clearing_results.json")["numbers"]
L366 = jl(DS, "L366_triggered_carrier_cluster_retention_results.json")["numbers"]
L375 = jl(DS, "L375_triggered_carrier_galaxy_retention_results.json")["numbers"]
L376 = jl(DS, "L376_triggered_carrier_inner_galaxies_results.json")["numbers"]
MS3 = jl(REPO, "real_research", "mond_sector_gate_2026", "MS3_cosmic_shear_bound_mond_sector_results.json")["numbers"]
SRC375 = open(os.path.join(DS, "L375_triggered_carrier_galaxy_retention.py")).read()
SRC376 = open(os.path.join(DS, "L376_triggered_carrier_inner_galaxies.py")).read()
SRC321 = open(os.path.join(DS, "L321_carrier_z0_retention_gate.py")).read()
SRCI27 = open(os.path.join(REPO, "fable_independent_2026", "lean_2026", "I27_kick_escape.lean")).read()

# ============================================================================================ constants (the lanes' own)
G = 4.30091e-9                                   # Mpc (km/s)^2 / Msun  (L375: 4.30091e-6 kpc (km/s)^2 / Msun)
h = 0.6736
OM_PM = 0.3138                                   # L362/L366's box cosmology
WB = (0.02237 / h ** 2) / OM_PM                  # L366's baryon share of the matter (the PM's baryons track it)
RHOC0 = 2.775e11 * h ** 2                        # Msun / Mpc^3 (L321's RHO_C0, L366's RHO_M = 2.775e11 Om per (Mpc/h)^3)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
G_SI, MSUN, MPC_M = 6.67430e-11, 1.98892e30, 3.0856775814913673e22     # GP0/GP3's constants (MS3's G, MS, MPC)
OM_GP0 = (0.02237 + 0.1200) / h ** 2; OL_GP0 = 1 - OM_GP0; FB_GP0 = 0.02237 / (0.02237 + 0.1200)
R_AP = 1.0                                       # Mpc/h: L366's aperture (comoving = physical at z = 0)
D_CELL = 100.0 / 256                             # L366's mesh (Mpc/h)
MBINS = ((6e13, 1e14), (1e14, 1.5e14), (1.5e14, 2.5e14), (2.5e14, 1e17))   # L371's bins, used by L388 and MS3
M_MIN = 6e13
BOXES = ("7", "17", "29")
EPSB = L366["eps_bounds"]                        # L354's two-sided X-COP rows, per footing (L366's eps_bounds)
LEVELS = {"50%": 0.5, "floor_can": float(EPSB["canonical"][0]), "floor_alt": float(EPSB["alt"][0])}
LEVEL_TXT = {"50%": "50% retention", "floor_can": f"X-COP floor canonical ({LEVELS['floor_can']:.3f})",
             "floor_alt": f"X-COP floor alt ({LEVELS['floor_alt']:.3f})"}
TAG388 = ("v575", "v600", "v625", "v650"); TAG380 = ("v600", "v625", "v650", "v675")
TAG366 = ("v550", "v600", "v650", "v700", "v850")
vk_of = lambda t: float(t[1:])
NBOOT = 1000
mfun = lambda x: np.log1p(x) - x / (1 + x)

# ============================================================================================ C1 exact reproduction
banner("C1  CONTROL: the committed retention numbers, reproduced EXACTLY from the per-halo lists")


def reproduce(num, tags):
    H = num["halos"]; dmax, nbad, nnum = 0.0, 0, 0
    for t in tags:
        Ms = [np.array(H[s]["M_lt_1Mpc_h"], float) for s in BOXES]; Es = [np.array(H[s]["eps"][t], float) for s in BOXES]
        for s, M_, E_ in zip(BOXES, Ms, Es):                      # per-box X-COP median (>= 1e14) and count
            sel = M_ >= 1e14
            dmax = max(dmax, abs(float(np.median(E_[sel])) - num["table"][s][t]["eps_cl"])); nnum += 1
            nbad += int(int(sel.sum()) != num["table"][s][t]["n_cl"])
        Mp, Ep = np.concatenate(Ms), np.concatenate(Es); sel = Mp >= 1e14
        dmax = max(dmax, abs(float(np.median(Ep[sel])) - num["table"]["pooled"][t]["eps_cl"])); nnum += 1
        nbad += int(int(sel.sum()) != num["table"]["pooled"][t]["n_cl"])
        for b0, b1 in MBINS:                                      # L371-bin medians and counts
            k_ = f"{b0:.1e}-{b1:.1e}"; sel = (Mp >= b0) & (Mp < b1); ref = num["retention_by_mass"][t][k_]
            dmax = max(dmax, abs(float(np.median(Ep[sel])) - ref[0])); nnum += 1
            nbad += int(int(sel.sum()) != ref[1])
    return dmax, nbad, nnum


d388, b388, n388 = reproduce(L388, TAG388)
d380, b380, n380 = reproduce(L380, TAG380)
M366 = np.array(L366["halo_mass"], float); d366 = 0.0
for t in TAG366:
    e_ = np.array(L366["retention"][t]["eps_halos"], float)
    d366 = max(d366, abs(float(np.median(e_[M366 >= 1e14])) - L366["retention"][t]["median_cl"]))
same7 = float(np.max(np.abs(M366 - np.array(L388["halos"]["7"]["M_lt_1Mpc_h"], float))))
P(f"    L388: {n388} committed medians, max |diff| = {d388:.1e}, count mismatches {b388};  e.g. pooled v600 X-COP median "
  f"{L388['table']['pooled']['v600']['eps_cl']:.16f} (n = {L388['table']['pooled']['v600']['n_cl']})")
P(f"    L380: {n380} committed medians, max |diff| = {d380:.1e}, count mismatches {b380}")
P(f"    L366: 5 cluster medians, max |diff| = {d366:.1e};  L366's 40 peaks are L388's box-7 peaks (max |dM| = {same7:.1e})")
check("C1 CONTROL: L388/L380 pooled + per-box X-COP medians and counts, L371-bin medians and counts, and L366's cluster "
      "medians reproduced EXACTLY from the per-halo lists",
      f"L388 {n388} numbers max |diff| {d388:.1e}; L380 {n380} numbers {d380:.1e}; L366 {d366:.1e}; count mismatches {b388 + b380}",
      d388 == 0.0 and d380 == 0.0 and d366 == 0.0 and b388 + b380 == 0 and same7 == 0.0)
OUT["numbers"]["C1"] = dict(L388_max_diff=d388, L380_max_diff=d380, L366_max_diff=d366, n_checked=n388 + n380 + 5)

# ============================================================================================ C2 the cap conversion
banner("C2  CONTROL: MS3's cap in velocity and baryonic mass, and GP0's bound baryons, reproduced")
H0_SI = 100 * h * 1e3 / MPC_M
RHO_CRIT0_GP0 = 3 * H0_SI ** 2 / (8 * math.pi * G_SI) * MPC_M ** 3 / MSUN     # Msun/Mpc^3 (GP0)
E2_05 = OM_GP0 * 1.5 ** 3 + OL_GP0
H05 = math.sqrt(8 * math.pi * G_SI * RHO_CRIT0_GP0 * E2_05 * MSUN / MPC_M ** 3 / 3) * MPC_M / 1e3     # km/s/Mpc
XLIN = 2.5 * E2_05
vcap_of = lambda r: r * H05 * math.sqrt(XLIN)                                  # MS3's door edge law beyond r200
Mb_of_v = lambda v, a0: (v * 1e3) ** 4 / (G_SI * a0) / MSUN
vf_of_Mb = lambda Mb, a0: (G_SI * Mb * MSUN * a0) ** 0.25 / 1e3
K1D = MS3["K1_design"]
vcap = vcap_of(K1D["r_cap_z05"]); Mcap = {f: Mb_of_v(vcap, A0[f]) for f in A0}
kids_can = {k_: vf_of_Mb(float(k_), A0["canonical"]) for k_ in K1D["kids_edges"]}
kids_alt = {k_: vf_of_Mb(float(k_), A0["alt"]) for k_ in K1D["kids_edges"]}
dv = abs(vcap / K1D["v_cap"] - 1); dm = abs(Mcap["canonical"] / K1D["M_b_cap"] - 1)
dk = max(abs(kids_can[k_] / v_["v_f"] - 1) for k_, v_ in K1D["kids_edges"].items())


def moster_Mstar(Mh, z):                         # GP0 (Moster, Naab & White 2013), re-implemented from its source
    zz = z / (1 + z)
    M1 = 10 ** (11.590 + 1.195 * zz); N = 0.0351 - 0.0247 * zz; beta = 1.376 - 0.826 * zz; gamma = 0.608 + 0.329 * zz
    return 2 * N * Mh / ((Mh / M1) ** (-beta) + (Mh / M1) ** gamma)


def M_bound_obs(M, z):                           # GP0's M_bound(M, z, 'observed'), scalar version
    cap = FB_GP0 * M
    Ms = min(moster_Mstar(M, z) * (1 + min(4.0, (M / 1e13) ** 0.4)), cap)
    lMs = math.log10(max(Ms, 1.0)); Mg = min(Ms + 1.33 * (10 ** (-0.6 * (lMs - 10) - 0.6) + 0.08) * Ms, cap)
    fhot = min(1.0, 0.55 * (M / 1e14) ** 0.2) / (1 + (3e12 / M) ** 2)
    return max(Mg, min(cap, fhot * cap))


du = max(abs(M_bound_obs(10 ** float(k_), 0.5) / v_["M_bound"] - 1) for k_, v_ in MS3["U1"].items())
P(f"    H(0.5) = {H05:.4f} km/s/Mpc, x_lin = {XLIN:.6f}; r_cap = {K1D['r_cap_z05']} Mpc -> v_cap = {vcap:.4f} km/s "
  f"(MS3 {K1D['v_cap']:.4f}); M_b,cap canonical {Mcap['canonical']:.4e} (MS3 {K1D['M_b_cap']:.4e}), alt {Mcap['alt']:.4e} Msun")
P("    KiDS lenses' v_f canonical / alt: " + ", ".join(f"M_b {k_}: {kids_can[k_]:.1f} / {kids_alt[k_]:.1f}" for k_ in kids_can)
  + " km/s")
P("    GP0 observed bound baryons at z = 0.5 (MS3 U1): " + ", ".join(f"1e{k_}: {M_bound_obs(10 ** float(k_), 0.5):.4e} "
                                                                     f"(MS3 {v_['M_bound']:.4e})" for k_, v_ in MS3["U1"].items()))
check("C2 CONTROL: MS3's v_cap, M_b,cap and KiDS v_f reproduced from r_cap, H(0.5), x_lin, a0; GP0's observed bound baryons "
      "re-implemented and reproduced on MS3's U1",
      f"v_cap rel. diff {dv:.1e}, M_b,cap {dm:.1e}, KiDS v_f {dk:.1e}, M_bound {du:.1e}", max(dv, dm, dk, du) < 1e-9)

# the cap band: MS3's grid value, the per-footing ceilings (linear interpolation of MS3's committed K1 grid -- not a run),
# and the KiDS floor (every KiDS lens keeps its own region: v_cap >= the largest lens's v_f)
K1 = {float(k_): v_ for k_, v_ in MS3["K1"].items()}
CAPS = sorted(K1)


def ceiling(getR):
    """the largest cap with worst R <= 1.2, linearly interpolated between MS3's grid caps (R rises with the cap)."""
    rs = [(c_, getR(K1[c_])) for c_ in CAPS]
    ok = [c_ for c_, R in rs if R <= 1.2]
    if not ok:
        return float("nan"), float("nan")
    c0 = max(ok); up = [c_ for c_ in CAPS if c_ > c0]
    if not up:
        return c0, c0
    c1 = min(up); R0, R1 = getR(K1[c0]), getR(K1[c1])
    return c0, c0 + (1.2 - R0) / (R1 - R0) * (c1 - c0)


CEIL = {}
for scen, getter in (("L388 retention", lambda f: (lambda row: row[f]["worst"])),
                     ("intact", lambda f: (lambda row: row["intact"][f])),
                     ("cleared<1e13", lambda f: (lambda row: row["cleared<1e13"][f]))):
    per = {f: ceiling(getter(f)) for f in A0}
    CEIL[scen] = dict(grid=min(per[f][0] for f in A0), interp={f: per[f][1] for f in A0},
                      joint_interp=min(per[f][1] for f in A0))
    CEIL[scen]["v_grid"] = vcap_of(CEIL[scen]["grid"]); CEIL[scen]["v_interp"] = {f: vcap_of(per[f][1]) for f in A0}
    CEIL[scen]["v_joint_interp"] = vcap_of(CEIL[scen]["joint_interp"])
    P(f"    MS3 K1, {scen:14s}: largest passing grid cap {CEIL[scen]['grid']:.2f} Mpc ({CEIL[scen]['v_grid']:.0f} km/s); "
      f"interpolated R = 1.2 edge canonical {per['canonical'][1]:.3f} / alt {per['alt'][1]:.3f} Mpc "
      f"({CEIL[scen]['v_interp']['canonical']:.0f} / {CEIL[scen]['v_interp']['alt']:.0f} km/s)")
BAND = dict(kids_floor=dict(canonical=max(kids_can.values()), alt=max(kids_alt.values())), grid=vcap,
            ceiling_alt=CEIL["L388 retention"]["v_interp"]["alt"], ceiling_can=CEIL["L388 retention"]["v_interp"]["canonical"])
BAND_LO, BAND_HI = min(BAND["kids_floor"].values()), max(BAND["ceiling_alt"], BAND["ceiling_can"])
P(f"    THE CAP BAND: {BAND_LO:.0f} km/s (largest KiDS lens v_f, canonical; alt {BAND['kids_floor']['alt']:.0f}) to "
  f"{BAND['grid']:.0f} (MS3's grid) / {BAND['ceiling_alt']:.0f} (alt-limited interpolated edge) / {BAND_HI:.0f} km/s (canonical edge)")
OUT["numbers"]["cap"] = dict(H05=H05, x_lin=XLIN, v_cap=vcap, M_b_cap=Mcap, kids_vf=dict(canonical=kids_can, alt=kids_alt),
                             ceilings=CEIL, band=BAND, band_lo=BAND_LO, band_hi=BAND_HI)

# ============================================================================================ C3 the unbinding relation
banner("C3  CONTROL: the isotropic-kick unbound fraction, and what I27's hypothesis is")


def f_unbound(vo, vk, ve):
    """fraction of daughters unbound by a kick of speed vk in a uniformly random direction, orbital speed vo, local escape
    speed ve (Phi = -ve^2/2, zero at infinity): |vo + vk n| > ve  <=>  cos(theta) > (ve^2 - vo^2 - vk^2)/(2 vo vk)."""
    vo, vk, ve = np.broadcast_arrays(np.asarray(vo, float), np.asarray(vk, float), np.asarray(ve, float))
    with np.errstate(divide="ignore", invalid="ignore"):
        f = ((vo + vk) ** 2 - ve ** 2) / (4 * vo * vk)
    f = np.where(vo * vk > 0, f, np.where(np.maximum(vo, vk) > ve, 1.0, 0.0))
    return np.clip(f, 0.0, 1.0)


rng_c3 = np.random.default_rng(27)
nh = rng_c3.normal(size=(400000, 3)); nh /= np.linalg.norm(nh, axis=1)[:, None]
dmc = 0.0
for vo, vk, ve in ((200, 600, 500), (400, 600, 700), (600, 600, 900), (100, 650, 800), (300, 575, 300), (500, 650, 1100),
                   (250, 600, 850), (700, 600, 800)):
    mc = float(np.mean(np.linalg.norm(np.array([vo, 0, 0])[None, :] + vk * nh, axis=1) > ve))
    dmc = max(dmc, abs(mc - float(f_unbound(vo, vk, ve))))
g = np.linspace(1, 1000, 40); VO, VK, VE = np.meshgrid(g, g, g, indexing="ij")
bound = VO < VE                                                   # daughters of bound orbits
F = f_unbound(VO, VK, VE)
i27 = VK > VO + VE
equiv = bool(np.all(F[bound & i27] == 1.0) and np.all(VK[bound & (F == 1.0)] >= VO[bound & (F == 1.0)] + VE[bound & (F == 1.0)] - 1e-9))
m27 = re.search(r"theorem kick_unbinds.*?\(hfast : ([^)]*)\)", SRCI27, re.S)
m321 = re.search(r"bound = (E < 0)", SRC321)
P(f"    I27 kick_unbinds hypothesis (read from the Lean file): {m27.group(1) if m27 else 'NOT FOUND'};  L321's retained() "
  f"(L371's S2 shape) counts a daughter as kept iff {m321.group(1) if m321 else 'NOT FOUND'} in the post-decay potential")
check("C3 CONTROL: the closed form f = clip(((v_o + v_k)^2 - v_esc^2)/(4 v_o v_k), 0, 1) matches a Monte Carlo over kick "
      "directions, and I27's v_k > |v_o| + v_esc is exactly its f = 1 edge (every direction unbinds)",
      f"max |closed form - MC| = {dmc:.4f} (4e5 directions); f = 1 <=> v_k >= v_o + v_esc on 64000 bound grid points: {equiv}",
      dmc < 0.005 and equiv and m27 is not None and m321 is not None)

# ============================================================================================ data (the scramble for MUTATE)
def dataset(num, tags):
    H = num["halos"]
    M = np.concatenate([np.array(H[s]["M_lt_1Mpc_h"], float) for s in BOXES])
    B = np.concatenate([np.full(len(H[s]["M_lt_1Mpc_h"]), int(s)) for s in BOXES])
    E = {t: np.concatenate([np.array(H[s]["eps"][t], float) for s in BOXES]) for t in tags}
    return M, B, E


D = {"L388": dataset(L388, TAG388), "L380": dataset(L380, TAG380),
     "L366": (M366, np.full(len(M366), 7), {t: np.array(L366["retention"][t]["eps_halos"], float) for t in TAG366})}
if MUTATE:
    for k_ in D:
        M_, B_, E_ = D[k_]; perm = np.random.default_rng(20260926).permutation(len(M_))
        D[k_] = (M_, B_, {t: e_[perm] for t, e_ in E_.items()})

# ============================================================================================ estimators
def crossing(x, y, L, extrapolate):
    """first upward crossing of level L by the piecewise-linear curve (x, y); flags 'in', 'below', 'above', 'none'."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 2:
        return float("nan"), "none"
    if y[0] >= L:
        if extrapolate and y[1] > y[0]:
            return float(x[0] + (L - y[0]) * (x[1] - x[0]) / (y[1] - y[0])), "below"
        return float("nan"), "below"
    for i in range(len(x) - 1):
        if y[i] < L <= y[i + 1]:
            return float(x[i] + (L - y[i]) * (x[i + 1] - x[i]) / (y[i + 1] - y[i])), "in"
    if extrapolate and y[-1] > y[-2]:
        return float(x[-2] + (L - y[-2]) * (x[-1] - x[-2]) / (y[-1] - y[-2])), "above"
    return float("nan"), "above"


def binned_points(M, E):
    pts = []
    for b0, b1 in MBINS:
        s = (M >= b0) & (M < b1)
        if s.any():
            pts.append((float(np.median(np.log10(M[s]))), float(np.median(E[s])), int(s.sum())))
    return pts


def x_binned(M, E, L):
    pts = binned_points(M, E)
    return crossing([p_[0] for p_ in pts], [p_[1] for p_ in pts], L, extrapolate=True)


def logistic(x, A, x0, w):
    return A / (1 + np.exp(-(x - x0) / w))


def fit_logistic(M, E):
    x = np.log10(M)
    try:
        p_, _ = curve_fit(logistic, x, E, p0=(0.9, 14.2, 0.2), bounds=([0.2, 12.0, 0.01], [1.6, 16.5, 3.0]), maxfev=20000)
        return p_
    except Exception:
        return None


def x_logistic(p_, L, xr):
    if p_ is None or p_[0] <= L:
        return float("nan"), "none"
    x = float(p_[1] - p_[2] * math.log(p_[0] / L - 1))
    return x, ("in" if xr[0] <= x <= xr[1] else ("below" if x < xr[0] else "above"))


def pava(y):
    blocks = []
    for yi in y:
        blocks.append([float(yi), 1])
        while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] > blocks[-1][0] / blocks[-1][1]:
            s_, c_ = blocks.pop(); blocks[-1][0] += s_; blocks[-1][1] += c_
    return blocks


def x_isotonic(M, E, L):
    o = np.argsort(M); x = np.log10(M[o]); y = E[o]; xs, ys, i = [], [], 0
    for s_, c_ in pava(y):
        xs.append(float(np.mean(x[i:i + c_]))); ys.append(s_ / c_); i += c_
    return crossing(xs, ys, L, extrapolate=False)


def classify(x, fl, xr):
    """flag a crossing by the DATA's mass range: 'in' (inside the data; for the binned estimator also between bin
    centres), 'extrap' (binned: beyond the bin centres but inside the data), 'below data' / 'above data' (not measured:
    the value is censored at the data edge for every interval below), 'none'."""
    if not np.isfinite(x):
        return x, ("below data" if fl == "below" else ("above data" if fl == "above" else "none"))
    if x < xr[0]:
        return x, "below data"
    if x > xr[1]:
        return x, "above data"
    return x, ("in" if fl == "in" else "extrap")


def censored(x, flag, xr):
    """the value used in intervals: clipped to the data's mass range (a crossing outside it is not measured)."""
    if flag == "below data":
        return xr[0]
    if flag in ("above data", "none"):
        return xr[1]
    return x


def estimates(M, E):
    sel = M >= M_MIN; M, E = M[sel], E[sel]; xr = (float(np.log10(M.min())), float(np.log10(M.max())))
    p_ = fit_logistic(M, E); out = {}
    for lv, L in LEVELS.items():
        out[lv] = {m_: classify(*r_, xr) for m_, r_ in (("binned", x_binned(M, E, L)), ("logistic", x_logistic(p_, L, xr)),
                                                         ("isotonic", x_isotonic(M, E, L)))}
    return out, p_, xr


def bootstrap(M, E, nb, seed):
    sel = M >= M_MIN; M, E = M[sel], E[sel]; n = len(M); rng = np.random.default_rng(seed)
    xr = (float(np.log10(M.min())), float(np.log10(M.max())))
    res = {lv: {m_: [] for m_ in ("binned", "logistic", "isotonic")} for lv in LEVELS}
    cen = {lv: {m_: 0 for m_ in ("binned", "logistic", "isotonic")} for lv in LEVELS}
    for _ in range(nb):
        idx = rng.integers(0, n, n)
        e_, _, _ = estimates(M[idx], E[idx])
        for lv in LEVELS:
            for m_ in res[lv]:
                x_, fl = e_[lv][m_]
                x_, fl = classify(x_, fl, xr)                      # against the FULL sample's range
                res[lv][m_].append(censored(x_, fl, xr)); cen[lv][m_] += int(fl in ("below data", "above data", "none"))
    q = {}
    for lv in LEVELS:
        q[lv] = {m_: dict(pct=np.percentile(np.array(a_, float), [2.5, 16, 50, 84, 97.5]).tolist(),
                          frac_censored=cen[lv][m_] / nb) for m_, a_ in res[lv].items()}
    return q


# ============================================================================================ conversions
def c_dm14(M200, z=0.0):                         # L376's z-dependent Dutton & Maccio 2014 (L321/L375/MS3's form at z = 0)
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(M200 / (1e12 / h)))


def rho_c(z, om=OM_PM):
    return RHOC0 * (om * (1 + z) ** 3 + 1 - om)


class NFW:
    def __init__(self, M200, z=0.0, om=OM_PM):
        self.M200, self.z = M200, z; self.c = c_dm14(M200, z)
        self.r200 = (3 * M200 / (4 * math.pi * 200 * rho_c(z, om))) ** (1 / 3); self.rs = self.r200 / self.c
        self.v200 = math.sqrt(G * M200 / self.r200); self.mc = float(mfun(self.c))

    def M(self, r):
        return self.M200 * float(mfun(r / self.rs)) / self.mc

    def phi(self, r):                            # Phi(inf) = 0 (I27's definition)
        if r <= 0:
            return -G * self.M200 / (self.mc * self.rs)
        return -G * self.M200 / self.mc * math.log1p(r / self.rs) / r

    def vesc(self, r, ref="inf"):
        pr = 0.0 if ref == "inf" else self.phi(2 * self.r200)
        d = pr - self.phi(r)
        return math.sqrt(2 * d) if d > 0 else float("nan")

    def vmax(self):
        r = 2.16258 * self.rs
        return math.sqrt(G * self.M(r) / r)

    def rho(self, r):
        x = r / self.rs
        return self.M200 / (4 * math.pi * self.rs ** 3 * self.mc) / (x * (1 + x) ** 2)


def nfw_from_aperture(Mx):
    """M200c (Msun) whose NFW mass within 1 Mpc/h (physical at z = 0) equals Mx (Msun/h), Dutton-Maccio c(M)."""
    Mt, R = Mx / h, R_AP / h
    return NFW(10 ** brentq(lambda lm: math.log(NFW(10 ** lm).M(R) / Mt), 10.0, 17.5))


NCELL = sum(1 for i in range(-4, 5) for j in range(-4, 5) for k in range(-4, 5) if (i * i + j * j + k * k) * D_CELL ** 2 <= R_AP ** 2)
R_EFF = (NCELL * D_CELL ** 3 * 3 / (4 * math.pi)) ** (1 / 3)


def convert(lgMx):
    """one crossing mass (log10 of M within 1 Mpc/h, Msun/h, z = 0) in every velocity convention."""
    if not np.isfinite(lgMx):
        return None
    Mx = 10 ** lgMx; o = dict(M_lt_1Mpc_h=Mx, v_c_1Mpc_h=math.sqrt(G * Mx / R_AP), v_c_Reff=math.sqrt(G * Mx / R_EFF))
    H_ = nfw_from_aperture(Mx); rtr = brentq(lambda r: H_.rho(r) - (OM_PM + 10 / 3) * RHOC0, 1e-3 * H_.r200, 100 * H_.r200)
    o.update(M200=H_.M200, c=H_.c, r200=H_.r200, v200=H_.v200, v_max=H_.vmax(), r_trig_over_r200=rtr / H_.r200)
    for nm, r in (("1Mpc_h", R_AP / h), ("r200", H_.r200), ("r_trig", rtr), ("centre", 0.0)):
        o[f"vesc_inf_{nm}"] = H_.vesc(r, "inf"); o[f"vesc_2r200_{nm}"] = H_.vesc(r, "2r200")
    o["M_b_cosmic"] = WB * H_.M200; o["M_b_observed"] = M_bound_obs(H_.M200, 0.0)
    for f in A0:
        o[f"v_f_cosmic_{f}"] = vf_of_Mb(o["M_b_cosmic"], A0[f]); o[f"v_f_observed_{f}"] = vf_of_Mb(o["M_b_observed"], A0[f])
    return o


CIRC = ("v_c_1Mpc_h", "v_c_Reff", "v200", "v_max", "v_f_cosmic_canonical", "v_f_cosmic_alt", "v_f_observed_canonical",
        "v_f_observed_alt")
ESC = ("vesc_inf_1Mpc_h", "vesc_inf_r200", "vesc_inf_r_trig", "vesc_inf_centre", "vesc_2r200_1Mpc_h", "vesc_2r200_r200",
       "vesc_2r200_centre")

# ============================================================================================ T  the transition
banner("T  THE RETENTION TRANSITION in L388's per-halo data (and L380's cell, L366's kick scaling)")
M, B, E = D["L388"]
low = np.where(M < M_MIN)[0]
P(f"    L388: {len(M)} peaks, {int((M >= M_MIN).sum())} at M(<1 Mpc/h) >= 6e13 Msun/h (fitted); below 6e13 (outside L371's bins, not "
  f"fitted): " + "; ".join(f"box {B[i]} M {M[i]:.2e}, v_c {math.sqrt(G * M[i]):.0f} km/s, eps " +
                           "/".join(f"{E[t][i]:.2f}" for t in TAG388) for i in low))
P(f"    the mesh sphere: {NCELL} cells of {D_CELL:.4f} Mpc/h -> R_eff = {R_EFF:.4f} Mpc/h (v_c lower by {1 - math.sqrt(R_AP / R_EFF):.1%})")
TR, SP = {}, {}
for t in TAG388:
    sel = M >= M_MIN
    rho_s, p_s = spearmanr(np.log10(M[sel]), E[t][sel])
    rng_p = np.random.default_rng(1000 + int(vk_of(t)))
    null = np.array([spearmanr(np.log10(M[sel]), rng_p.permutation(E[t][sel]))[0] for _ in range(2000)])
    p_perm = float((np.sum(null >= rho_s) + 1) / (len(null) + 1))
    est, par, xr = estimates(M, E[t])
    bs = bootstrap(M, E[t], NBOOT, 7000 + int(vk_of(t)))
    per_box, per_box_xr = {}, {}
    for bx in (7, 17, 29):
        mb = B == bx
        per_box[bx], _, per_box_xr[bx] = estimates(M[mb], E[t][mb])
    TR[t] = dict(est=est, logistic_params=(None if par is None else [float(v_) for v_ in par]), data_range_log10M=xr,
                 boot=bs, per_box=per_box, per_box_range=per_box_xr, bins=binned_points(M[sel], E[t][sel]))
    SP[t] = dict(rho=float(rho_s), p=float(p_s), p_perm=p_perm, null_max=float(null.max()))
    pts = TR[t]["bins"]
    P(f"\n    {t}: Spearman rho(log M, eps) = {rho_s:+.3f} (p = {p_s:.1e}; permutation p = {p_perm:.1e}, null max {null.max():+.3f}); "
      f"L371-bin medians " + ", ".join(f"1e{x_:.2f}: {y_:.3f} (n={n_})" for x_, y_, n_ in pts)
      + ("" if par is None else f"; logistic A {par[0]:.2f}, log10 M_h {par[1]:.2f}, width {par[2]:.2f} dex"))
    vv = lambda z_: math.sqrt(G * 10 ** z_)

    def show(x_, fl, xr_):
        if fl == "below data":
            return f"<{vv(xr_[0]):.0f}"
        if fl in ("above data", "none"):
            return f">{vv(xr_[1]):.0f}"
        return f"{vv(x_):.0f}" + ("" if fl == "in" else "~")

    for lv in LEVELS:
        row = []
        for m_ in ("binned", "logistic", "isotonic"):
            x_, fl = est[lv][m_]; q = bs[lv][m_]["pct"]; fc = bs[lv][m_]["frac_censored"]
            row.append(f"{m_} {show(x_, fl, xr)} [68% {vv(q[1]):.0f}-{vv(q[3]):.0f}; 95% {vv(q[0]):.0f}-{vv(q[4]):.0f}"
                       + (f"; {fc:.0%} censored" if fc > 0 else "") + "]")
        boxes_ = "; ".join(f"box {bx}: " + "/".join(show(*per_box[bx][lv][m_], per_box_xr[bx])
                                                    for m_ in ("binned", "logistic", "isotonic")) for bx in (7, 17, 29))
        P(f"      {LEVEL_TXT[lv]:28s} v_c(1 Mpc/h), km/s: " + " | ".join(row))
        P(f"      {'':28s} per box (binned/logistic/isotonic): {boxes_}")
    P("      (~ = binned value extrapolated past the lowest/highest bin centre but inside the data; <x / >x = outside the data, "
      "censored at its edge in every interval)")
OUT["numbers"]["transition_L388"] = TR; OUT["numbers"]["spearman_L388"] = SP
ALL120 = {}
for t in TAG388:                                                  # sensitivity: the two sub-6e13 peaks included
    p_all = fit_logistic(M, E[t]); xr_all = (float(np.log10(M.min())), float(np.log10(M.max())))
    ALL120[t] = classify(*x_logistic(p_all, 0.5, xr_all), xr_all)
P("\n    SENSITIVITY, all 120 peaks (the two sub-6e13 peaks included), logistic 50% crossing v_c(1 Mpc/h): " + "; ".join(
    f"{t}: " + (f"{math.sqrt(G * 10 ** ALL120[t][0]):.0f}" if ALL120[t][1] in ("in", "extrap") else ALL120[t][1]) for t in TAG388))
OUT["numbers"]["sensitivity_all120_logistic50"] = ALL120

# T0: the transition exists (the load-bearing measurement; MUTATE must break it)
t0_ok = all(SP[t]["rho"] > 0 and SP[t]["p"] < 1e-3 and TR[t]["est"]["50%"]["binned"][1] == "in"
            and TR[t]["est"]["50%"]["logistic"][1] == "in" for t in TAG388)
check("T0 THE TRANSITION EXISTS: for every L388 kick the >= 6e13 retention rises with mass (Spearman rho > 0, p < 1e-3), the "
      "L371-bin medians cross 50% inside the bins, and the logistic 50% point lies inside the data",
      "; ".join(f"{t}: rho {SP[t]['rho']:+.2f} p {SP[t]['p']:.0e}, binned {TR[t]['est']['50%']['binned'][1]}, logistic "
                f"{TR[t]['est']['50%']['logistic'][1]}" for t in TAG388), t0_ok,
      "the committed retention has a mass transition to locate; a scrambled pairing has none")

# L380 (p = 2 cell) and L366 (Newtonian, one box): point estimates, and the kick scaling
TRX = {}
for nm, tags in (("L380", TAG380), ("L366", TAG366)):
    Mx_, Bx_, Ex_ = D[nm]; TRX[nm] = {}
    for t in tags:
        est, par, xr = estimates(Mx_, Ex_[t]); TRX[nm][t] = dict(est=est, data_range_log10M=xr)
    def show2(x_, fl, xr_):
        if fl == "below data":
            return f"<{math.sqrt(G * 10 ** xr_[0]):.0f}"
        if fl in ("above data", "none"):
            return f">{math.sqrt(G * 10 ** xr_[1]):.0f}"
        return f"{math.sqrt(G * 10 ** x_):.0f}" + ("" if fl == "in" else "~")
    for lv in ("50%", "floor_can"):
        P(f"\n    {nm} ({'p = 2, x_c0 = 2 cell, pooled 3 boxes' if nm == 'L380' else 'Newtonian, box 7 only'}): {LEVEL_TXT[lv]} at "
          "v_c(1 Mpc/h), binned/logistic/isotonic: " + "; ".join(f"{t}: " + "/".join(
              show2(*TRX[nm][t]['est'][lv][m_], TRX[nm][t]['data_range_log10M']) for m_ in ("binned", "logistic", "isotonic"))
              for t in tags))
OUT["numbers"]["transition_other"] = TRX


def scaling(trd, tags, m_="logistic"):
    xs, ys = [], []
    for t in tags:
        x_, fl = trd[t]["est"]["50%"][m_]
        if fl in ("in", "extrap"):
            xs.append(math.log(vk_of(t))); ys.append(math.log(math.sqrt(G * 10 ** x_)))
    if len(xs) < 2:
        return float("nan"), len(xs)
    return float(np.polyfit(xs, ys, 1)[0]), len(xs)


SCL = {"L388": {m_: scaling(TR, TAG388, m_) for m_ in ("binned", "logistic", "isotonic")},
       "L380": {m_: scaling(TRX["L380"], TAG380, m_) for m_ in ("binned", "logistic", "isotonic")},
       "L366": {m_: scaling(TRX["L366"], TAG366, m_) for m_ in ("binned", "logistic", "isotonic")}}
P("\n    KICK SCALING of the 50% crossing, v_c,50 ~ v_k^alpha (crossings inside the data only): " + "; ".join(
    f"{nm}: " + ", ".join(f"{m_} {a_:.2f} (n={n_})" for m_, (a_, n_) in d_.items()) for nm, d_ in SCL.items()))
OUT["numbers"]["kick_scaling_alpha"] = SCL

# ============================================================================================ V  velocities and the claim
banner("V  THE CROSSINGS AS VELOCITIES (lanes' conventions, z = 0) AGAINST THE CAP AND THE KICK")
P("    conventions: v_c at 1 Mpc/h and at the mesh sphere's R_eff; NFW (Dutton-Maccio 2014, M200c) v200, v_max; baryons' "
  "deep-MOND flat speed (G M_b a0)^1/4 with cosmic f_b (PM) or GP0's observed bound baryons; escape speeds Phi(inf) = 0 / "
  "Phi(2 r200)")
VT = {}
for t in TAG388:
    VT[t] = {}
    xr = TR[t]["data_range_log10M"]
    for lv in LEVELS:
        meas = [(m_,) + tuple(TR[t]["est"][lv][m_]) for m_ in ("binned", "logistic", "isotonic")
                if TR[t]["est"][lv][m_][1] in ("in", "extrap")]          # crossings inside the data
        prim = next((c_ for c_ in meas if c_[0] == "binned"), meas[0] if meas else None)
        lo_candidates = []                                        # the lowest plausible crossing (most favourable to the claim)
        for m_ in ("binned", "logistic", "isotonic"):
            lo_candidates.append(TR[t]["boot"][lv][m_]["pct"][0])      # bootstrap 2.5%, censored at the data's lower edge
            for bx in (7, 17, 29):
                x_, fl = TR[t]["per_box"][bx][lv][m_]
                if fl in ("in", "extrap"):
                    lo_candidates.append(x_)
        allx = [c_[1] for c_ in meas]
        VT[t][lv] = dict(primary=(None if prim is None else dict(method=prim[0], flag=prim[2], conv=convert(prim[1]))),
                         not_measured_below=(None if meas else convert(xr[0])),
                         method_range=([convert(min(allx)), convert(max(allx))] if allx else None),
                         lowest_plausible=convert(min(lo_candidates)),
                         lowest_is_data_edge=bool(abs(min(lo_candidates) - xr[0]) < 1e-12))
OUT["numbers"]["velocities_L388"] = VT


def fmt(cv, keys):
    return ", ".join(f"{k_} {cv[k_]:.0f}" for k_ in keys if cv is not None and np.isfinite(cv.get(k_, float("nan"))))


for t in TAG388:
    vk = vk_of(t)
    P(f"\n    {t}  (v_k/2 = {vk / 2:.0f} km/s)")
    for lv in LEVELS:
        pr = VT[t][lv]["primary"]
        if pr is None:
            nb_ = VT[t][lv]["not_measured_below"]
            P(f"      {LEVEL_TXT[lv]}: NOT MEASURED -- every estimator puts it below the data (v_c < {nb_['v_c_1Mpc_h']:.0f}, v200 < "
              f"{nb_['v200']:.0f} km/s)"); continue
        cv = pr["conv"]; mr = VT[t][lv]["method_range"]; lp = VT[t][lv]["lowest_plausible"]
        P(f"      {LEVEL_TXT[lv]} ({pr['method']}, {pr['flag']}): M(<1 Mpc/h) {cv['M_lt_1Mpc_h']:.2e} Msun/h -> M200 {cv['M200']:.2e} Msun, "
          f"c {cv['c']:.2f}, r_trig {cv['r_trig_over_r200']:.2f} r200")
        P(f"        circular: {fmt(cv, CIRC)}  [x v_cap: {cv['v_c_1Mpc_h'] / vcap:.2f} (v_c), {cv['v200'] / vcap:.2f} (v200), "
          f"{cv['v_f_observed_canonical'] / vcap:.2f}-{cv['v_f_cosmic_alt'] / vcap:.2f} (v_f)]")
        P(f"        escape:   {fmt(cv, ESC)}  [x v_k/2: {cv['vesc_inf_1Mpc_h'] / (vk / 2):.1f} at 1 Mpc/h, {cv['vesc_inf_r_trig'] / (vk / 2):.1f} "
          f"at r_trig; Phi(2 r200) at 1 Mpc/h {cv['vesc_2r200_1Mpc_h'] / (vk / 2):.1f}]")
        P(f"        baryons: cosmic {cv['M_b_cosmic']:.2e}, observed bound {cv['M_b_observed']:.2e} Msun = x{cv['M_b_observed'] / Mcap['canonical']:.0f} "
          f"(canonical) / x{cv['M_b_observed'] / Mcap['alt']:.0f} (alt) M_b,cap")
        if mr and lp:
            P(f"        estimator spread v_c(1 Mpc/h) {mr[0]['v_c_1Mpc_h']:.0f}-{mr[1]['v_c_1Mpc_h']:.0f}; lowest plausible (bootstrap 2.5% / "
              f"in-data per-box minimum{', = the data edge' if VT[t][lv]['lowest_is_data_edge'] else ''}): v_c {lp['v_c_1Mpc_h']:.0f}, "
              f"v200 {lp['v200']:.0f}, v_max {lp['v_max']:.0f}, v_f {min(lp[k_] for k_ in CIRC[4:]):.0f} km/s")

# the claim, both ways: min over kicks, estimators, bootstrap, boxes and circular conventions of transition / cap-band top
lp_min = {}
for lv in LEVELS:
    vals = []
    for t in TAG388:
        lp = VT[t][lv]["lowest_plausible"]
        if lp is not None:
            vals.append(min(lp[k_] for k_ in CIRC))
    lp_min[lv] = min(vals) if vals else float("nan")
prim50 = {t: (VT[t]["50%"]["primary"]["conv"] if VT[t]["50%"]["primary"] else None) for t in TAG388}
HAVE50 = [t for t in TAG388 if prim50[t] is not None]
r50 = {t: {k_: prim50[t][k_] / vcap for k_ in CIRC} for t in HAVE50}
coincide = bool(np.isfinite(lp_min["50%"]) and lp_min["50%"] <= BAND_HI) if t0_ok else None
OUT["numbers"]["claim"] = dict(lowest_plausible_circular=lp_min, band_hi=BAND_HI, ratio_50_to_vcap=r50,
                               ratio_lowest_50_to_band_hi=lp_min["50%"] / BAND_HI, coincide=coincide)
P(f"\n    MOST FAVOURABLE TO THE CLAIM (lowest plausible crossing over kicks 575-650, three estimators, bootstrap 2.5%, in-range "
  f"per-box minima, every circular convention incl. both footings' v_f): 50% at {lp_min['50%']:.0f} km/s; canonical floor "
  f"{lp_min['floor_can']:.0f}; alt floor {lp_min['floor_alt']:.0f}  -- against the cap band's top {BAND_HI:.0f} km/s")
check("V1 (reported either way) THE CLAIM: the 50% retention transition, in some circular-speed convention, touches the cap "
      f"band ({BAND_LO:.0f}-{BAND_HI:.0f} km/s)",
      f"lowest plausible 50% crossing {lp_min['50%']:.0f} km/s = {lp_min['50%'] / BAND_HI:.2f} x the band's top; point estimates "
      + ", ".join(f"{t}: v_c {prim50[t]['v_c_1Mpc_h']:.0f} ({r50[t]['v_c_1Mpc_h']:.2f} v_cap)" for t in HAVE50),
      True, ("NOT EVALUATED: T0 failed, there is no retention transition in these data" if coincide is None else
             ("COINCIDE: some reading of the 50% transition reaches the cap band" if coincide else
              "DO NOT COINCIDE: every reading of the 50% transition sits above the cap band")), load_bearing=False)

# ============================================================================================ K  the kick physics
banner("K  THE KICK PHYSICS: the unbinding relation, I27, and an idealised static single-halo model")
P("    exact, isotropic kick: f_unbound = clip(((v_o + v_k)^2 - v_esc^2) / (4 v_o v_k), 0, 1).  f = 1 (every direction) iff "
  "v_k >= v_o + v_esc (I27's hypothesis); f = 1/2 iff v_k^2 = v_esc^2 - v_o^2 (the kick supplies the binding energy); "
  "f = 0 iff v_k <= v_esc - v_o")
ORB = {}
for qn, q in (("at rest (v_o = 0)", 0.0), ("circular, point mass (v_o = v_esc/sqrt2)", 1 / math.sqrt(2)),
              ("marginally bound infall (v_o = v_esc)", 1.0)):
    all_ = 1 / (1 + q); half = (1 / math.sqrt(1 - q * q)) if q < 1 else float("inf"); none_ = (1 / (1 - q)) if q < 1 else float("inf")
    ORB[qn] = dict(vesc_over_vk_all=all_, vesc_over_vk_half=half, vesc_over_vk_none=none_)
    P(f"    {qn:44s}: every daughter unbound for v_esc <= {all_:.3f} v_k ({all_ * 575:.0f}-{all_ * 650:.0f} km/s); half at v_esc = "
      + (f"{half:.3f} v_k" if np.isfinite(half) else "never below half (f >= 1/2 + v_k/(4 v_esc))")
      + "; none for v_esc >= " + (f"{none_:.3f} v_k" if np.isfinite(none_) else "never"))
OUT["numbers"]["orbit_classes"] = ORB
P("    => v_esc = v_k/2 is the every-direction (I27) edge ONLY for daughters moving at the escape speed; the half-unbinding "
  "point is set by the binding energy, v_k = sqrt(v_esc^2 - v_o^2), which for bound orbits means v_esc >= v_k")

# the idealised static model: NFW (z = 0, Dutton-Maccio), isotropic Jeans, all carrier inside r200 decays at once, the
# pre-decay potential held fixed (no assembly, no self-consistent shallowing, no progenitors), retained = bound after the
# kick / bound before (L321's control ratio)
YG = np.geomspace(1e-5, 1e5, 40000); FY = mfun(YG) / (YG ** 3 * (1 + YG) ** 2)
TAILY = np.concatenate([np.cumsum((0.5 * (FY[1:] + FY[:-1]) * np.diff(YG))[::-1])[::-1], [0.0]])
rng_s = np.random.default_rng(20260926); NS_ = 40000
U_ = rng_s.random(NS_); GV = rng_s.normal(size=(NS_, 3)); NK = rng_s.normal(size=(NS_, 3)); NK /= np.linalg.norm(NK, axis=1)[:, None]


def static_retained(M200, vk, ref):
    Hh = NFW(M200); c = Hh.c; xg = np.geomspace(1e-4, c, 4000); x = np.interp(U_ * float(mfun(c)), mfun(xg), xg)
    s2 = (c / float(mfun(c))) * x * (1 + x) ** 2 * np.interp(np.log(x), np.log(YG), TAILY)       # sigma_r^2 / v200^2
    v = GV * np.sqrt(s2)[:, None] * Hh.v200
    phi = -(Hh.v200 ** 2 * c / float(mfun(c))) * np.log1p(x) / x
    pref = 0.0 if ref == "inf" else -(Hh.v200 ** 2 * c / float(mfun(c))) * math.log1p(2 * c) / (2 * c)
    b0 = 0.5 * np.sum(v ** 2, 1) + phi < pref; b1 = 0.5 * np.sum((v + vk * NK) ** 2, 1) + phi < pref
    return float(b1.sum() / max(b0.sum(), 1))


LMG = np.arange(11.5, 15.01, 0.05); STAT = {}
for vk in (575.0, 600.0, 625.0, 650.0):
    for ref in ("inf", "2r200"):
        ret = np.array([static_retained(10 ** lm, vk, ref) for lm in LMG])
        row = {}
        for lv, L in LEVELS.items():
            x_, fl = crossing(LMG, ret, L, extrapolate=False)
            row[lv] = dict(log10M200=x_, flag=fl, v200=(NFW(10 ** x_).v200 if np.isfinite(x_) else float("nan")))
        STAT[f"{int(vk)}/{ref}"] = row
    P(f"    static model, v_k {vk:.0f}: 50% retained at v200 = {STAT[f'{int(vk)}/inf']['50%']['v200']:.0f} km/s (Phi(inf)) / "
      f"{STAT[f'{int(vk)}/2r200']['50%']['v200']:.0f} km/s (Phi(2 r200)) = {STAT[f'{int(vk)}/inf']['50%']['v200'] / vk:.2f} / "
      f"{STAT[f'{int(vk)}/2r200']['50%']['v200'] / vk:.2f} v_k;  canonical floor at v200 {STAT[f'{int(vk)}/inf']['floor_can']['v200']:.0f} / "
      f"{STAT[f'{int(vk)}/2r200']['floor_can']['v200']:.0f}")
OUT["numbers"]["static_model"] = STAT
st50 = [STAT[k_]["50%"]["v200"] for k_ in STAT if np.isfinite(STAT[k_]["50%"]["v200"])]
pm50 = [prim50[t]["v200"] for t in HAVE50]
st_overlap = bool(st50) and min(st50) <= BAND_HI and max(st50) >= BAND_LO
P(f"    => the idealised static halo puts half-retention at v200 = {min(st50):.0f}-{max(st50):.0f} km/s "
  f"({'overlapping' if st_overlap else 'not overlapping'} the cap band {BAND_LO:.0f}-{BAND_HI:.0f})"
  + (f"; the construction's committed retention (L388, with assembly) puts it at v200 = {min(pm50):.0f}-{max(pm50):.0f} km/s, "
     f"x{min(pm50) / max(st50):.1f}-{max(pm50) / min(st50):.1f} the static values" if (pm50 and t0_ok) else ""))
OUT["numbers"]["static_vs_pm"] = dict(static_v200_50=st50, pm_v200_50=pm50, static_overlaps_band=st_overlap)

# ============================================================================================ G  the emptied end
banner("G  THE EMPTIED END: galaxy hosts (L375 resolved shell model, L376 interiors)")
mb = re.search(r"M200_BINS = \[([^\]]*)\]", SRC375); M200B = [float(s_) for s_ in mb.group(1).split(",")]
ZL = float(re.search(r"ZL = ([0-9.]+)", SRC375).group(1))
mh = re.search(r"HOSTS = (\{[^}]*\})", SRC376); HOSTS = ast.literal_eval(mh.group(1))
OM375 = (0.02237 + 0.1200) / h ** 2
GAL = {"L375": [], "L376": {}}
for i, M0 in enumerate(M200B):
    Hh = NFW(M0, ZL, OM375); row = dict(M200=M0, z=ZL, v200=Hh.v200, vesc_inf_r200=Hh.vesc(Hh.r200), vesc_inf_centre=Hh.vesc(0.0))
    for t, key in (("v600", "v600"), ("v650", "fid"), ("v700", "v700")):
        S, Sc = L375["table"][key]["S"][i], L375["table"][key]["S_cold"][i]
        row[t] = dict(S=S, S_cold=Sc, daughters_kept=(S - Sc) / (1 - Sc))
    GAL["L375"].append(row)
    P(f"    L375 KiDS host M200 {M0:.2e} (z = {ZL}): v200 {Hh.v200:.0f} km/s, pre-decay v_esc(r200) {row['vesc_inf_r200']:.0f}, centre "
      f"{row['vesc_inf_centre']:.0f};  S(<0.5 Mpc/h) 600/650/700: " + "/".join(f"{row[t]['S']:.3f}" for t in ("v600", "v650", "v700"))
      + ", of which undecayed " + "/".join(f"{row[t]['S_cold']:.3f}" for t in ("v600", "v650", "v700"))
      + " -> decayed daughters kept " + "/".join(f"{row[t]['daughters_kept']:.2f}" for t in ("v600", "v650", "v700")))
for hn, (M0, Mb0) in HOSTS.items():
    Hh = NFW(M0, 0.0, OM375); w = max(v_["Delta_dex"] for v_ in L376["rar"][hn].values())
    w0 = max(v_["Delta_dex"] for v_ in L376["rar"][hn + "_nodecay"].values())
    GAL["L376"][hn] = dict(M200=M0, M_b=Mb0, v200=Hh.v200, vesc_inf_r200=Hh.vesc(Hh.r200), vesc_inf_centre=Hh.vesc(0.0),
                           rar_shift_worst=w, rar_shift_nodecay=w0, v_f=dict((f, vf_of_Mb(Mb0, A0[f])) for f in A0))
    P(f"    L376 {hn:9s} M200 {M0:.0e} (z = 0): v200 {Hh.v200:.0f} km/s, pre-decay v_esc(r200) {Hh.vesc(Hh.r200):.0f}, centre "
      f"{Hh.vesc(0.0):.0f}; carrier's RAR shift at 2-8 R_d {w:.1e} dex (decay off {w0:.2f}) at v_k = 650: EMPTIED")
P(f"    L376 RC100: carrier inside R_e / LCDM's at z = 1, 2 = {L376['rc100']['z1']['carrier_ratio']:.0e}, {L376['rc100']['z2']['carrier_ratio']:.0e}")
emp_hi = max([r_["v200"] for r_ in GAL["L375"]] + [v_["v200"] for v_ in GAL["L376"].values()])
pm_lo = math.sqrt(G * float(np.min(M[M >= M_MIN])))
lowbin = [TR[t]["bins"][0][1] for t in TAG388]
gap_eps = [float(E[t][i]) for i in low for t in TAG388]
gap_v = [math.sqrt(G * M[i]) for i in low]
in_gap = BAND_LO >= emp_hi and BAND_HI <= pm_lo
P(f"    => the committed runs show emptying up to v200 ~ {emp_hi:.0f} km/s, and {min(lowbin):.2f}-{max(lowbin):.2f} kept (median of "
  f"L371's lowest bin over the kicks) from v_c(1 Mpc/h) ~ {pm_lo:.0f} km/s up; the cap band ({BAND_LO:.0f}-{BAND_HI:.0f}) "
  f"{'lies inside' if in_gap else 'overlaps'} the UNMEASURED gap between them.  The only committed peaks in the gap "
  f"(v_c {min(gap_v):.0f}-{max(gap_v):.0f} km/s) keep {min(gap_eps):.2f}-{max(gap_eps):.2f}.")
OUT["numbers"]["galaxies"] = GAL
OUT["numbers"]["gap"] = dict(emptied_up_to_v200=emp_hi, pm_lowest_v_c=pm_lo, lowest_bin_median=lowbin, gap_peaks_v_c=gap_v,
                             gap_peaks_eps_range=[min(gap_eps), max(gap_eps)], cap_band_inside_gap=in_gap)

# ============================================================================================ S  MS3's own rows
banner("S  MS3's OWN K1 ROWS AS THE ONE-NUMBER TEST: a retention step AT the cap scale")
r200_step = (3 * 1e13 / (4 * math.pi * 200 * RHO_CRIT0_GP0 * E2_05)) ** (1 / 3); v200_step_gp0 = math.sqrt(G * 1e13 / r200_step)
Mb_step = MS3["U1"]["13.0"]["M_bound"]
row175 = K1[1.75]
P(f"    'cleared<1e13' = carrier removed below M200 = 1e13 Msun, kept above: v200(z = 0.5) = {v200_step_gp0:.0f} km/s, bound baryons "
  f"{Mb_step:.2e} Msun -> v_f {vf_of_Mb(Mb_step, A0['canonical']):.0f} / {vf_of_Mb(Mb_step, A0['alt']):.0f} km/s (canonical/alt): a "
  f"transition AT the cap scale ({vcap:.0f} km/s)")
P(f"    at MS3's 1.75 Mpc cap: worst R with L388's retention {row175['canonical']['worst']:.3f}/{row175['alt']['worst']:.3f} (pass); with the "
  f"step at the cap scale {row175['cleared<1e13']['canonical']:.3f}/{row175['cleared<1e13']['alt']:.3f} (FAIL, gate 1.2)")
P(f"    with the step at the cap scale the largest passing cap is {CEIL['cleared<1e13']['grid']:.2f} Mpc on MS3's grid "
  f"({CEIL['cleared<1e13']['v_grid']:.0f} km/s), {CEIL['cleared<1e13']['joint_interp']:.2f} Mpc interpolated ({CEIL['cleared<1e13']['v_joint_interp']:.0f} km/s) "
  f"= {CEIL['cleared<1e13']['v_joint_interp'] / v200_step_gp0:.2f} x the step's own v200")
OUT["numbers"]["one_number_test_MS3"] = dict(step_M200=1e13, step_v200_z05=v200_step_gp0, step_Mb=Mb_step,
                                              R_at_175=dict(L388=[row175["canonical"]["worst"], row175["alt"]["worst"]],
                                                            step=[row175["cleared<1e13"]["canonical"], row175["cleared<1e13"]["alt"]]),
                                              cap_with_step=CEIL["cleared<1e13"])

# ============================================================================================ verdict
banner("VERDICT")
step_fails = bool(row175["cleared<1e13"]["canonical"] > 1.2 or row175["cleared<1e13"]["alt"] > 1.2)
if not t0_ok or not HAVE50:
    OUT["numbers"]["verdict"] = dict(coincide=None, note="T0 failed: no retention transition in these data")
    P("  T0 FAILED: the retention does not rise with host mass in these data (MUTATE scrambles the pairing), so there is no\n"
      "  transition to compare with the cap and no verdict is drawn from this run.")
else:
    v50 = [prim50[t]["v_c_1Mpc_h"] for t in HAVE50]; v50_200 = [prim50[t]["v200"] for t in HAVE50]
    ve50 = [prim50[t]["vesc_inf_1Mpc_h"] for t in HAVE50]; vk50 = [v50[i] / vk_of(t) for i, t in enumerate(HAVE50)]
    fl = [(t, VT[t]["floor_can"]["primary"]) for t in TAG388 if VT[t]["floor_can"]["primary"]]
    fl_c = [p_["conv"]["v_c_1Mpc_h"] for _, p_ in fl]
    OUT["numbers"]["verdict"] = dict(coincide=coincide, v50_vc=v50, v50_v200=v50_200, v50_vesc_1Mpc_h=ve50, floor_can_vc=fl_c,
                                     floor_can_flags=[p_["flag"] for _, p_ in fl], ratio_v50_vcap=[x_ / vcap for x_ in v50],
                                     ratio_v50_vk=vk50, ratio_vcap_vk=[vcap / vk_of(t) for t in TAG388],
                                     step_at_cap_fails_shear=step_fails)
    emp_esc = max(max(r_["vesc_inf_r200"] for r_ in GAL["L375"]), max(v_["vesc_inf_r200"] for v_ in GAL["L376"].values()))
    emp_esc0 = max(max(r_["vesc_inf_centre"] for r_ in GAL["L375"]), max(v_["vesc_inf_centre"] for v_ in GAL["L376"].values()))
    OUT["numbers"]["verdict"].update(emptied_vesc_r200_max=emp_esc, emptied_vesc_centre_max=emp_esc0)
    P(f"""  THE TRANSITION.  The committed retention (L388, pooled, >= 6e13 Msun/h) crosses 50% at v_c(1 Mpc/h) = {min(v50):.0f}-{max(v50):.0f} km/s
  over v_k = 575-650 (v200 {min(v50_200):.0f}-{max(v50_200):.0f}; Phi(inf) escape speed at 1 Mpc/h {min(ve50):.0f}-{max(ve50):.0f}): x{min(v50) / vcap:.1f}-{max(v50) / vcap:.1f} v_cap,
  x{min(vk50):.2f}-{max(vk50):.2f} v_k, and an escape speed x{min(ve50[i] / (vk_of(t) / 2) for i, t in enumerate(HAVE50)):.1f}-{max(ve50[i] / (vk_of(t) / 2) for i, t in enumerate(HAVE50)):.1f} v_k/2.  The canonical X-COP floor is crossed at v_c
  {min(fl_c):.0f}-{max(fl_c):.0f} (flags {[p_['flag'] for _, p_ in fl]}).  The lowest plausible 50% crossing (any estimator, bootstrap 2.5%,
  any box, any circular convention incl. both footings' v_f) is {lp_min['50%']:.0f} km/s, against the cap band's top {BAND_HI:.0f} km/s.
  THE EMPTIED END.  The kick empties hosts up to v200 ~ {emp_hi:.0f} km/s whose pre-decay escape speeds reach {emp_esc:.0f} (r200) and
  {emp_esc0:.0f} km/s (centre), i.e. deeper than v_k/2; the edge itself lies in the unmeasured gap {emp_hi:.0f}-{pm_lo:.0f} km/s.
  THE KICK.  v_cap / v_k = {vcap / 650:.2f}-{vcap / 575:.2f}: "about half the kick" holds as arithmetic.  v_esc = v_k/2 is I27's every-direction
  edge only for daughters moving at the escape speed; half-unbinding needs v_k^2 = v_esc^2 - v_o^2.  The idealised static halo puts
  half-retention at v200 {min(st50):.0f}-{max(st50):.0f} (near v_k/2); the construction's runs (with assembly) at v200 {min(v50_200):.0f}-{max(v50_200):.0f}.
  MS3's OWN ROWS.  A retention step AT the cap scale (v200 = {v200_step_gp0:.0f} km/s): {row175['cleared<1e13']['canonical']:.2f}/{row175['cleared<1e13']['alt']:.2f} at the 1.75 Mpc cap
  ({'FAILS' if step_fails else 'passes'} the 1.2 gate); its largest passing cap is ~{CEIL['cleared<1e13']['v_joint_interp']:.0f} km/s = x{CEIL['cleared<1e13']['v_joint_interp'] / v200_step_gp0:.2f} the step.
  VERDICT: {'the scales COINCIDE within the uncertainties' if coincide else 'the two scales DO NOT COINCIDE'}.""")

n_lb_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), n_lb_fail, time.time() - T0
fn = os.path.join(HERE, f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json")
json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: (o.tolist() if hasattr(o, "tolist") else str(o)))
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {n_lb_fail}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(0 if n_lb_fail == 0 else 1)
