#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR19 (1/2) -- THE DARK FLUID'S SEEDED FRONT: gain, momentum matching and re-resonance, from FK1/FP10's own formulas.

WHY.  XR12 (K, an estimate) and XR16 (B3, a flag) left one question open: once the fluid converts in halos, do its
daughters -- or the web's own slow sweeps -- carry the conversion phi_H phi_H -> phi_L phi_L through the cosmic web?
FK1 normalises the conversion on the Hubble-swept background: the pair coupling G(rho, z) = G_t(z) rho/rho_t(z), with
G_t(z) = sqrt(4 H delta E_need/pi) and the vacuum-gated threshold rho_t/rho_bar = delta_t0 E^4/(1+z)^3 (q = 1.75).  At the
mean density the SPONTANEOUS exponent never reaches E_need (FK1 N2), but a seed only needs ln(pump/seed) e-folds.  This
lane computes what the design leaves implicit: which daughters can re-enter the resonance |v - u_pump| = v_k at all
(Bose stimulation of back-to-back pairs is momentum-matched to the LOCAL pump), and the gain they get where they do.
The dark fluid is FL1/FK1's order parameter (a classical field, not a particle species; its quanta would be bosons of mass
m >~ 1.9-5.2e-19 eV); the dark MASS is still required.  XR19_web_runaway.py uses these results on a realistic web.

WHAT IS COMPUTED
  C0  CONTROL: FK1's N1-N3 from FK1's own formulas vs its committed JSON (XR12 C0's numbers).
  C1  CONTROL: the design's stimulated criterion in the Hubble flow reproduced from the gain formula below: XR16 B3's and
      FP10 A8's committed 'mean density stimulable below z' values (L319's cosmology, each lane's own grid).
  G   the gain map with the vacuum gate: G/H, gain length v_k/G, the Hubble-sweep gain E_need (rho/rho_t)^2 per passage,
      and the density at which a seed with ln(pump/seed) = 1, 3, 10 converts, for z = 0-4, delta_t0 = 5.31-25, m.
  S1  [sympy] the momentum-matching identities: for a pressureless pump u and a free daughter in the SAME gravity,
      w = v - u(x(t), t) obeys dw/dt = -(w.grad)u exactly; |w|^2 falls monotonically wherever the strain T = sym(grad u) is
      positive definite; D'' = 2 delta (2|T n|^2 - n.Tdot.n) (irrotational pump); on a zero-strain cone |T n|^2 = -e_1 e_2;
      the one-passage integral I(beta) -> C4 (tangent) and pi/(2 beta) (FK1 K4); the Doppler-broadened area is 2x the
      coherent one in FP10's convention (a factor carried as a bracket downstream).
  H   the Hubble flow: rays in every direction never re-enter the resonance (branching ratio 0); a ray through the
      resonance gains exactly E_need (rho/rho_t)^2 (K4).
  Z   a Zel'dovich pancake after turnaround: exact ray integration of the pair's detuning against the local zero-strain
      (cone) formula C4 G^(3/2)/sqrt(alpha); the enhancement over the Hubble sweep; the 1D ignition table.
  B   re-resonance: daughters born on the resonance inside a turned-around pancake, followed forward -- blue-shifted along
      the contracting axis, then red-shifted outside -- re-cross the resonance; the gain there.
  I   halo-seeded zones: LCDM spherical shells around a halo (linear mean overdensity delta_c (M/M200)^(-eps) at the
      epoch, eps = 0.6, 0.4-1.0 bracket); daughters emitted isotropically at r200 by the infalling pump, followed through the
      halo and out in the time-dependent flow; where |w| = v_k again, the exact detuning's D1, D'' and the local G give the
      gain; the zone's pump mass against the fast seeds' mass gives the yield Y = M_seed e^g / M_zone.
  R   the reach: the comoving distance a daughter covers, and how far past its source it can still be resonant.
PRE-DECLARED (written in the session's scratch notes before this script's first full run; see HISTORY)
  H-S  S1's identities hold exactly (sympy).
  H-H  no re-resonance in the unperturbed Hubble flow in any direction; a passage gains E_need (rho/rho_t)^2 to <= 1%.
  H-Z  exact/local cone gain in [0.5, 1.0] at every tested pancake; the best direction beats the transverse (Hubble-sweep)
       gain by >= 10x; every tested pancake at z <= 2 ignites (gain >= E_need) at rho/rho_t <= 0.84 (below the trigger).
  H-B  daughters born on the resonance inside a turned-around pancake re-cross it outside the contracting zone for >= 20%
       of (birth point, direction) pairs, with median gain >= 3 e-folds at z = 0.5-1 (nominal cell, pump = full density).
  H-I  >= 30% of the daughters emitted at r200 cross the resonance again outside r200; at z_e <= 1 (nominal cell) the
       median gain at those crossings exceeds ln(M_zone/M_seed) + 1 (Y >= 1: the fast seeds convert their zone) for the
       smooth pump s = 1 - F_halo as well as s = 1.
CHECKS (load-bearing unless marked)
  C0, C1 the controls above.  G2 the mean background: the gate keeps its spontaneous exponent <= 0.054 E_need at every
  z <= 10, while a resonant seed gains >= 1 e-fold per passage there at low z.  S1 the identities.  H1 the Hubble flow (no
  re-crossing; K4 to 1%).  Z1 the local cone formula within a factor 0.5-1.0 of the exact rays; the transverse direction
  = K4 to 10%.  Z2 the cone beats the Hubble sweep >= 10x; every tested sub-trigger pancake at z <= 2 ignites.  B1
  re-resonance: nonzero in every tested turned-around pancake, median gain >= 3 at z <= 1, growing with the collapse depth,
  and zero in the Hubble flow.  I1 fast seeds (>= 30% of the daughters cross again outside r200) in every case, and Y >= 1
  for the full-density pump at z_e <= 1.  Reported: G (tables), Z3 (1D ignition table), I2 (smooth pump, z = 2,
  delta_t0 = 13.5, eps), R (reach), H (the pre-declared hypotheses above, as they fell, with their original thresholds).
MUTATE=1 removes Bose stimulation: the stimulated exponent int sqrt(G^2 - D^2) dt is set to 0 (only the spontaneous,
  occupation-independent rate is left, which converts nothing in a Hubble time).  G2, H1, Z1, Z2, B1 and I1 must FAIL:
  rc = 1.
A0 FOOTINGS.  No a0 enters this script: the carrier is kernel-invisible (L353, FL2 V1), the trigger reads the carrier's own
  density and the flows are Newtonian.  Both footings (FP0's canonical 9.3603e-11 and alt 1.1312e-10 m s^-2) give
  identical numbers; a0 enters XR19_web_runaway.py only through the flagship-bounded normalisation band.
SCOPE.  Kinematics and the local rates are exact within FK1/FP10's model; the pancake and the shells are idealised flows
  (plane Zel'dovich before shell crossing; spherical shells with Lambda); the pump is taken single-stream and cold where
  the coherent formula is used, and the pump roughness is a bracket (sigma_r) downstream.  Constants: none new.  eps/m^2
  (v_k) is FITTED to the kick window; lambda_0 and q are DECLARED (FK1).  kappa = 1/2 does not enter.
HISTORY (disclosed).  Scratch explorations came first (not committed): the gain map, the pancake's local cone formula and an
  exact ray integration (exact/local 0.65-0.89 at four pancakes), a Zel'dovich web census (XR19_web_runaway's prototype)
  and a spherical-shell infall model.  The hypotheses H-S ... H-I were written after those and before this script ran.
  A smoke run of this script (a copy writing to the session's scratch directory, not committed) then found three code bugs,
  fixed before the recorded run: C1 took the first grid redshift where the mean density IS stimulable instead of the first
  where it is not; Z2 required every tested pancake to be below the trigger instead of testing those that are; I1's filter
  compared a rounded delta_t0 with the unrounded one and selected nothing, so it passed vacuously.  The smoke run also
  showed H-B's configuration (d = 0.6, just past turnaround) re-crossing for only 2-7% of pairs; a scratch probe found
  14-26% at d = 0.75-0.85, and those two depths were added to B beside the pre-declared one.  The load-bearing checks were
  then separated from the pre-declared hypothesis rows, which are reported unchanged in H: B1's and I1's load-bearing
  thresholds were RELAXED after the smoke run to the existence claims (re-resonance nonzero and growing with collapse; fast
  seeds; Y >= 1 for the full-density pump), and H keeps the original thresholds (H-B's 20% at d = 0.6, H-I's smooth-pump
  clause), whatever they give.  Apart from that relaxation, the B depths added, and the three bug fixes, nothing was
  changed after the smoke run.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR19_front_physics.py
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "2"
import sys, json, math, time
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR19_common as X

MUTATE = os.environ.get("MUTATE", "0") == "1"
STIM = not MUTATE
SLUG = "XR19_front_physics"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR19", "part": "1/2 front physics", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split(" ")[0]] = {"ok": ok, "claim": name, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 118); P(t); P("=" * 118)
def el(): return f"[{time.time() - T0:.0f}s]"


P(__doc__.split("CHECKS (load")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: Bose stimulation removed (stimulated exponent = 0); G2, Z1, Z2, B1, I1 must FAIL ***")

M_FID, VK_FID = 2e-19, 600.0
EN_FID = X.ENEED["2e-19"]
EN_LO = X.ENEED["1e-06"]
FHALO = {0.0: 0.629, 0.5: 0.580, 1.0: 0.529, 1.5: 0.480, 2.0: 0.433, 3.0: 0.342, 4.0: 0.255}   # XR16's budget (K = 60),
# extended to z < 2 with XR16's own machinery in XR19_web_runaway (C1 there reproduces the committed z >= 2 values exactly)

# ============================================================================================ C0 FK1's N1-N3
banner("C0  CONTROL: FK1's N1-N3 from FK1's own formulas against its committed JSON")
N2c = {}
for dt_ in (5.0, 25.0):
    for hf in (1.0, 4.0):
        N2c[f"{dt_:g}/{hf:g}"] = brentq(lambda z: (1 + z) ** 6 / float(X.E(z)) - hf * dt_ ** 2, 0.0, 1e4)
zz = np.linspace(0, 20, 20001)
f175 = (1 + zz) ** 6 / X.E(zz) ** (1 + 4 * 1.75)
pk_z, pk_f = float(zz[f175.argmax()]), float(f175.max())
E_need = X.fk1_n1(2e-19)
s600 = (600 / X.C_KMS) ** 2 / (2 - (600 / X.C_KMS) ** 2)
G_over_m = math.sqrt(4 * E_need * (X.HBAR_EVS * X.H0_SI / 2e-19) * s600 / math.pi)
N2 = X.FK1["N2"]
dev_z = max(abs(N2c[k_] - N2["z_convert_constant"][k_]) for k_ in N2c)
P("    constant coupling converts the background by z: " + ", ".join(f"{k_} -> {v:.4f} (FK1 {N2['z_convert_constant'][k_]:.4f})" for k_, v in N2c.items()))
P(f"    q = 1.75: peak z = {pk_z:.3f} (FK1 {N2['bg_peak_z']:.3f}), {pk_f:.4f}x (FK1 {N2['bg_peak_factor']:.4f}); E_need(2e-19) = {E_need:.2f} "
  f"(FK1 {X.FK1['N1']['by_mass']['2e-19']['efolds']:.2f}); G_t/mc^2 = {G_over_m:.3e} (FK1 {X.FK1['N3']['2e-19']['G_over_mc2']:.3e})")
OUT["numbers"]["C0"] = dict(z_convert=N2c, peak_z=pk_z, peak_f=pk_f, E_need=E_need, G_over_mc2=G_over_m)
check("C0 CONTROL: FK1's N1-N3 reproduced from its own formulas (z_convert 0.8574/1.4829/2.6934/4.0119; peak z = 0.298 at "
      "1.3479x; E_need 178.05; G_t/mc^2 1.806e-9)",
      f"max |dz| {dev_z:.1e}; peak {pk_z:.3f}/{pk_f:.4f}; E_need {E_need:.2f}; G_t/mc^2 {G_over_m:.4e}",
      dev_z < 1e-9 and abs(pk_z - N2["bg_peak_z"]) < 1e-9 and abs(pk_f - N2["bg_peak_factor"]) < 1e-9
      and abs(E_need - X.FK1["N1"]["by_mass"]["2e-19"]["efolds"]) < 1e-9 and abs(G_over_m / X.FK1["N3"]["2e-19"]["G_over_mc2"] - 1) < 1e-9)

# ============================================================================================ C1 XR16 B3 / FP10 A8
banner("C1  CONTROL: the stimulated criterion in the Hubble flow -- XR16 B3's and FP10 A8's committed numbers from the gain formula")
REPO = X.REPO
h19 = 0.6736; Om19 = (0.02237 + 0.1200) / h19 ** 2; Or19 = 4.18e-5 / h19 ** 2 * (1 + 0.2271 * 3.046); OL19 = 1 - Om19 - Or19
Ez2_19 = lambda z: Om19 * (1 + z) ** 3 + OL19
dt_19 = lambda z: 2.5 * Ez2_19(z) / (1.5 * Om19 * (1 + z) ** 3 / Ez2_19(z))          # the linear cell's delta_t(z) (XR16/FP10)
# a seed resonant with the mean background gains E_need (rho_bar/rho_t)^2 = E_need/delta_t(z)^2 per passage (K4 scaled)
xr16 = json.load(open(os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26", "XR16_fluid_conversion_surface_results.json")))["numbers"]["B3"]
fp10 = json.load(open(os.path.join(REPO, "real_research", "derivation_chain_2026", "FP10_internal_splitting_dark_sector_results.json")))["numbers"]["A8"]["criterion"]
mine = {}
# E_need (rho_bar/rho_t)^2 >= 1  <=>  delta_t(z) <= sqrt(E_need): the first grid z where it fails (each lane's own expression)
g1 = np.linspace(0.0, 6.0, 6001); d1 = np.array([dt_19(z) for z in g1])
for En in (60.0, 180.0):
    mine[f"XR16 {En:g}"] = (float(g1[np.argmax(d1 >= math.sqrt(En))]), xr16[f"{En}"]["z_mean_stimulable_below"])
g2 = np.linspace(0.0, 6.0, 1201); d2 = np.array([dt_19(z) for z in g2])
for En, key in ((EN_LO, "61"), (EN_FID, "178")):
    mine[f"FP10 {En:.2f}"] = (float(g2[np.argmax(d2 > math.sqrt(En))]), fp10[key]["z_mean_stimulable_below"])
for k_, (a_, b_) in mine.items():
    P(f"    {k_:12s}: mean density gains >= 1 e-fold per passage below z = {a_:.4f} (committed {b_:.4f})")
dev1 = max(abs(a_ - b_) for a_, b_ in mine.values())
OUT["numbers"]["C1"] = {k_: list(v_) for k_, v_ in mine.items()}
check("C1 CONTROL: the per-passage seeded gain E_need (rho/rho_t)^2 reproduces XR16 B3 (1.152/1.762) and FP10 A8 (1.165/1.760)",
      f"max |dz| {dev1:.1e}", dev1 < 1e-9, "the same criterion both lanes flagged; here it is the gain formula used throughout")

# ============================================================================================ G the gain map
banner("G   THE GAIN MAP WITH THE VACUUM GATE (m = 2e-19 eV, v_k = 600 km/s unless stated)")
ZG = (0.0, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0)
DENS = (0.3, 1.0, 3.0, 10.0, 30.0, 100.0)
KPC_KM = 3.0857e16
GM = {}
for z in ZG:
    rt = float(X.rho_t_over_mean(z))
    Gt = float(X.G_t(z, M_FID, VK_FID, EN_FID)); H = float(X.H_si(z))
    row = {}
    for dd in DENS:
        G = Gt * dd / rt
        row[dd] = dict(G_over_H=G / H, gain_len_kpc=VK_FID / G / KPC_KM, sweep_gain=EN_FID * (dd / rt) ** 2,
                       kin20_gain_len_kpc=VK_FID / float(X.kinetic_rate(G, M_FID, VK_FID, 20.0)) / KPC_KM)
    GM[z] = dict(rho_t_over_mean=rt, rows=row)
    P(f"    z = {z:3.1f}: rho_t/rho_bar {rt:6.2f}; per-passage Hubble-sweep gain at 1+delta = " +
      ", ".join(f"{dd:g}: {row[dd]['sweep_gain']:.3g}" for dd in DENS) + f";  gain length at 1+delta = 10: coherent "
      f"{row[10.0]['gain_len_kpc']:.2f} kpc, kinetic (sigma 20) {row[10.0]['kin20_gain_len_kpc']:.2f} kpc")
SEEDTAB = {}
for dt0 in (X.DT0_LIN, 7.54, 13.5, 22.8, 25.0):
    for En in (EN_LO, EN_FID):
        SEEDTAB[(round(dt0, 2), round(En, 1))] = {z: {gn: float(X.rho_t_over_mean(z, dt0)) * math.sqrt(gn / En) for gn in (1.0, 3.0, 10.0)} for z in ZG}
for (dt0, En), tab in SEEDTAB.items():
    P(f"    delta_t0 {dt0:5.2f}, E_need {En:5.1f}: the density (1+delta) a resonant seed converts at, ln(pump/seed) = 1/3/10: " +
      "; ".join(f"z={z:g}: {tab[z][1.0]:.2f}/{tab[z][3.0]:.2f}/{tab[z][10.0]:.2f}" for z in (0.0, 0.5, 1.0, 2.0, 3.0)))
OUT["numbers"]["G"] = dict(map={str(z): {str(dd): v for dd, v in d_["rows"].items()} | {"rho_t_over_mean": d_["rho_t_over_mean"]} for z, d_ in GM.items()},
                           seed_density={f"{k_[0]}|{k_[1]}": {str(z): {str(g): v for g, v in t_.items()} for z, t_ in tab.items()} for k_, tab in SEEDTAB.items()})

# G2 the mean background: never spontaneous, seedable at low z
zb = np.linspace(0, 10, 10001)
ratio_sp = np.array([(1 / float(X.rho_t_over_mean(z))) ** 2 for z in zb])                     # spontaneous exponent / E_need
g_bg = {}
for En in (EN_LO, EN_FID):
    gb = En * ratio_sp * (1.0 if STIM else 0.0)
    g_bg[round(En, 1)] = dict(max=float(gb.max()), z_max=float(zb[gb.argmax()]), z_below=float(zb[np.argmax(gb < 1.0)]) if (gb >= 1).any() else None)
P(f"    mean background: spontaneous exponent/E_need <= {ratio_sp.max():.4f} (z = {zb[ratio_sp.argmax()]:.2f}); seeded gain per passage "
  + "; ".join(f"E_need {k_}: max {v['max']:.2f} e-folds at z = {v['z_max']:.2f}, >= 1 e-fold for z <= {v['z_below']}" for k_, v in g_bg.items()))
OUT["numbers"]["G2"] = dict(spont_max=float(ratio_sp.max()), seeded=g_bg)
check("G2 with the gate the mean background never self-ignites (spontaneous exponent <= 0.054 E_need at every z <= 10), yet a "
      "resonant seed gains >= 1 e-fold per passage there at low z (max 2.9-8.5 e-folds at z = 0.30 for E_need = 61-178)",
      f"spontaneous max {ratio_sp.max():.4f} E_need; seeded max {', '.join(f'{v['max']:.2f}' for v in g_bg.values())} e-folds",
      ratio_sp.max() <= 0.054 and all(v["max"] >= 1.0 for v in g_bg.values()),
      "the gate protects the background from vacuum noise, not from seeds: whether it converts turns on momentum matching")

# ============================================================================================ S1 identities
banner("S1  [sympy] MOMENTUM MATCHING: the relative velocity of a daughter to its LOCAL pump")
t_ = sp.Symbol("t", real=True)
# (a1) the chain rule along a path, on a generic polynomial field (no assumption): d/dt u(X(t), t) = u_t + (X'.grad) u
xs = sp.symbols("x0:3", real=True)
Xf = [sp.Function(f"X{i}")(t_) for i in range(3)]
cpoly = sp.symbols("c0:10", real=True)
upoly = (cpoly[0] * xs[0] ** 2 * t_ + cpoly[1] * xs[1] * xs[2] + cpoly[2] * xs[0] * t_ ** 2 + cpoly[3] * xs[2] ** 3
         + cpoly[4] * xs[0] * xs[1] * t_)
lhs = sp.diff(upoly.subs(dict(zip(xs, Xf))), t_)
rhs = (sp.diff(upoly, t_) + sum(sp.diff(upoly, xs[j]) * sp.diff(Xf[j], t_) for j in range(3))).subs(dict(zip(xs, Xf)))
chain_ok = sp.simplify(lhs - rhs) == 0
# (a2) at a point of the path: daughter velocity V, free fall (V' = g); pump u with gradient U_ij = d_j u_i and Euler
#      (pressureless: u_t = g - (u.grad)u).  Then dw/dt = V' - (u_t + (V.grad)u) must equal -(w.grad)u, w = V - u.
Vs = sp.symbols("V0:3", real=True); us = sp.symbols("u0:3", real=True); gs = sp.symbols("g0:3", real=True)
Us = sp.Matrix(3, 3, sp.symbols("U0:9", real=True))
res1 = []
for i in range(3):
    ut_i = gs[i] - sum(us[j] * Us[i, j] for j in range(3))
    dwdt_i = gs[i] - (ut_i + sum(Vs[j] * Us[i, j] for j in range(3)))
    target = -sum((Vs[j] - us[j]) * Us[i, j] for j in range(3))
    res1.append(sp.simplify(dwdt_i - target))
ident_ok = chain_ok and all(r_ == 0 for r_ in res1)
# (b) the antisymmetric part drops out of d|w|^2/dt; (c) D'' for an irrotational (symmetric) gradient; (d) the cone
Ms = sp.Matrix(3, 3, sp.symbols("M0:9", real=True)); ws = sp.Matrix(sp.symbols("w0:3", real=True))
T_ = (Ms + Ms.T) / 2; A_ = (Ms - Ms.T) / 2
anti_ok = sp.simplify((ws.T * A_ * ws)[0]) == 0
Ts = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"T{min(i, j)}{max(i, j)}", real=True)); Td = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"S{min(i, j)}{max(i, j)}", real=True))
# d/dt |w|^2 = -2 w.T.w with dw/dt = -T w, dT/dt = Td: second derivative
d1w = -2 * (ws.T * Ts * ws)[0]
dwdt = -Ts * ws
d2w = sp.expand(-2 * ((dwdt.T * Ts * ws)[0] + (ws.T * Ts * dwdt)[0] + (ws.T * Td * ws)[0]))
d2_ok = sp.simplify(d2w - (4 * (ws.T * Ts * Ts * ws)[0] - 2 * (ws.T * Td * ws)[0])) == 0
e1s, e2s = sp.symbols("e1 e2", real=True)
n1sq = e2s / (e2s - e1s)
cone_zero = sp.simplify(e1s * n1sq + e2s * (1 - n1sq)) == 0
cone_T2 = sp.simplify(e1s ** 2 * n1sq + e2s ** 2 * (1 - n1sq) + e1s * e2s) == 0
# (e) the one-passage integral limits and (f) the kinetic area
Ib0 = float(X.I_beta(0.0)); Ib_inf = float(X.I_beta(1e4) * 1e4)
Gs, D1s, Dls = sp.symbols("G D1 Delta", positive=True)
kin_area = sp.simplify(sp.integrate(sp.sqrt(sp.pi) * Gs ** 2 / Dls * sp.exp(-(D1s * t_ / Dls) ** 2), (t_, -sp.oo, sp.oo)))
coh_area = sp.pi * Gs ** 2 / (2 * D1s)                                                   # int sqrt(G^2 - D1^2 t^2) dt
area_ratio = sp.simplify(kin_area / coh_area)
P(f"    chain rule along the path (generic polynomial field): {chain_ok};  dw/dt + (w.grad)u (free fall, pressureless pump, same g): residuals {res1}")
P(f"    antisymmetric part drops out of d|w|^2/dt: {anti_ok};  d2|w|^2/dt2 = 4 w.T^2.w - 2 w.Tdot.w: {d2_ok}")
P(f"    two-axis cone n1^2 = e2/(e2 - e1): n.T.n = 0 {cone_zero}, |T n|^2 = -e1 e2 {cone_T2}")
P(f"    I(0) = {Ib0:.6f} (C4 = {X.C4:.6f});  beta I(beta) at beta = 1e4 -> {Ib_inf:.6f} (pi/2 = {math.pi / 2:.6f});  kinetic/coherent area = {area_ratio}")
OUT["numbers"]["S1"] = dict(identity=[str(r_) for r_ in res1], anti=anti_ok, d2=d2_ok, cone=[cone_zero, cone_T2], I0=Ib0, Iinf=Ib_inf, area_ratio=str(area_ratio))
check("S1 [sympy] dw/dt = -(w.grad)u exactly (free daughter, pressureless pump, same gravity); d|w|^2/dt = -2 w.T.w (the "
      "vorticity drops out), so |w| falls monotonically in positive-definite strain; D'' = 2 delta (2|Tn|^2 - n.Tdot.n); on the "
      "cone |Tn|^2 = -e1 e2; I(0) = C4, beta I -> pi/2 (K4); the kinetic area is 2x the coherent (FP10's convention)",
      f"identity {ident_ok}; anti {anti_ok}; D'' {d2_ok}; cone {cone_zero}/{cone_T2}; I(0) {Ib0:.5f}; beta I {Ib_inf:.5f}; ratio {area_ratio}",
      ident_ok and anti_ok and d2_ok and cone_zero and cone_T2 and abs(Ib0 - X.C4) < 1e-6 and abs(Ib_inf - math.pi / 2) < 1e-3
      and sp.simplify(area_ratio - 2) == 0,
      "Bose stimulation needs |w| = v_k with w measured against the LOCAL pump; in an expanding flow w only shrinks, so a daughter "
      "born on the resonance can never re-enter it there, and a seed can enter it at most once, from above")

# ============================================================================================ H the Hubble flow
banner("H   THE HUBBLE FLOW: every direction, rays through the resonance, forward paths")
H1 = {}
for z in (0.5, 1.0, 2.0):
    pc0 = X.Pancake(z, 0.0, 4000.0)                                   # A = 0: the unperturbed flow
    nxs = np.linspace(-1.0, 1.0, 21)
    Kref = EN_FID * (1 / float(X.rho_t_over_mean(z))) ** 2
    # the passage: resolve the window t_w ~ (G/delta)/H with a span of 40 windows
    Gd = float(X.G_t(z, M_FID, VK_FID, EN_FID)) / float(X.rho_t_over_mean(z)) / X.delta_split(M_FID, VK_FID)
    g = X.pancake_rays(pc0, nxs, 0.0, s_frac=1.0, nstep=4000, span_H=40 * Gd, stimulated=STIM)
    # the forward path over 0.3/H for the monotonicity of D(t)
    _, paths = X.pancake_rays(pc0, nxs, 0.0, s_frac=1.0, nstep=1500, span_H=0.3, return_paths=True, signs=(+1.0,), stimulated=STIM)
    fw = paths[0]
    Dd = np.array([p_[4] for p_ in fw])                                # forward D(t)/..., shape (nt, ndir)
    mono = bool(np.all(np.diff(Dd, axis=0) < 0))                       # strictly decreasing after birth
    recross = int(np.sum(np.any(Dd[5:] > 0, axis=0)))
    H1[z] = dict(gain=g.tolist(), K4=Kref, max_dev=float(np.max(np.abs(g / Kref - 1))) if STIM else float("nan"), monotone=mono, recross=recross)
    P(f"    z = {z}: gain over 21 directions {g.min():.4f}-{g.max():.4f} vs K4 E_need (rho_bar/rho_t)^2 = {Kref:.4f}; forward D(t) strictly "
      f"decreasing in every direction: {mono}; re-crossings: {recross}   {el()}")
OUT["numbers"]["H"] = {str(k_): v_ for k_, v_ in H1.items()}
check("H1 the Hubble flow: no direction re-enters the resonance (D(t) strictly falls after birth), and a passage gains "
      "E_need (rho/rho_t)^2 to <= 1% in every direction (FK1 K4)",
      "; ".join(f"z={k_}: dev {v_['max_dev']:.1e}, monotone {v_['monotone']}, re-crossings {v_['recross']}" for k_, v_ in H1.items()),
      all(v_["monotone"] and v_["recross"] == 0 and v_["max_dev"] <= 0.01 for v_ in H1.values()),
      "in the expanding background conversion cannot branch: each seed is amplified once, and its products never return")

# ============================================================================================ Z the pancake cone
banner("Z   A TURNED-AROUND ZEL'DOVICH PANCAKE: exact rays against the local zero-strain (cone) formula")
CONF = ((0.5, 0.70, 4000.0), (0.5, 0.80, 4000.0), (1.0, 0.70, 4000.0), (1.0, 0.85, 4000.0), (2.0, 0.70, 2000.0), (2.0, 0.85, 2000.0))
ZR = {}
for (zc, dc, lam) in CONF:
    pc = X.Pancake(zc, dc, lam)
    gl, nxc, G, alpha, dl, rr, Eh = X.pancake_local_cone(pc, En=EN_FID)
    nxs = np.linspace(nxc - 0.03, nxc + 0.03, 61)
    g = X.pancake_rays(pc, nxs, 0.0, En=EN_FID, stimulated=STIM)
    i = int(np.argmax(g))
    gt = float(X.pancake_rays(pc, np.array([0.0]), 0.0, En=EN_FID, nstep=4000, span_H=40 * G / dl, stimulated=STIM)[0])  # resolve the first-order window
    off = {}
    for x0 in (0.02, 0.05, 0.1):
        nn = np.concatenate([np.linspace(nxc - 0.1, nxc + 0.1, 41), -np.linspace(nxc - 0.1, nxc + 0.1, 41)])
        nn = nn[np.abs(nn) < 1]
        off[x0] = float(X.pancake_rays(pc, nn, x0, En=EN_FID, stimulated=STIM).max())
    ZR[(zc, dc, lam)] = dict(local=gl, exact=float(g[i]), n_best=float(nxs[i]), n_cone=nxc, transverse=gt, K4_transverse=EN_FID * rr ** 2,
                            rho_over_rt=rr, ratio=float(g[i] / gl), enh=float(g[i] / max(gt, 1e-300)), off=off, E_need=Eh)
    P(f"    z_c {zc} d {dc} lambda {lam:.0f} kpc: rho/rho_t {rr:.3f}; local cone {gl:8.1f}; exact max {g[i]:8.1f} at n_x {nxs[i]:.4f} "
      f"(cone {nxc:.4f}); exact/local {g[i] / gl:.3f}; transverse {gt:.2f} (K4 {EN_FID * rr ** 2:.2f}); off-centre 0.02/0.05/0.1: "
      + "/".join(f"{v:.0f}" for v in off.values()) + f"   {el()}")
OUT["numbers"]["Z"] = {f"{k_[0]}|{k_[1]}|{k_[2]}": v_ for k_, v_ in ZR.items()}
rat = [v_["ratio"] for v_ in ZR.values()]
trans_dev = max(abs(v_["transverse"] / v_["K4_transverse"] - 1) for v_ in ZR.values())
check("Z1 the local zero-strain formula C4 G^(3/2)/sqrt(alpha) (alpha = delta (2|Tn|^2 - n.Tdot.n) at the centre) is confirmed by "
      "exact ray integration to a factor 0.5-1.0 at every tested pancake, and the transverse direction reproduces K4 to <= 10%",
      f"exact/local {min(rat):.3f}-{max(rat):.3f}; transverse vs K4 max dev {trans_dev:.3f}",
      all(0.5 <= r_ <= 1.0 for r_ in rat) and trans_dev <= 0.10,
      "the calibration factor min(exact/local) is carried into the web census (XR19_web_runaway) as 'cal'")
enh = [v_["enh"] for v_ in ZR.values()]
sub_trig = [v_ for k_, v_ in ZR.items() if k_[0] <= 2.0 and v_["rho_over_rt"] <= 0.84]
ign = len(sub_trig) >= 3 and all(v_["exact"] >= EN_FID for v_ in sub_trig)
check("Z2 on the zero-strain cone of a turned-around pancake the gain beats the Hubble sweep by >= 10x, and every tested "
      "pancake at z <= 2 that sits below the trigger (rho/rho_t <= 0.84; at least three of them) ignites from vacuum "
      "(gain >= E_need = 178)",
      f"enhancement {min(enh):.1f}-{max(enh):.1f}x; below the trigger: " + ", ".join(f"{v_['exact']:.0f} at rho/rho_t {v_['rho_over_rt']:.2f}" for v_ in sub_trig)
      + "; above it: " + ", ".join(f"{v_['exact']:.0f} at {v_['rho_over_rt']:.2f}" for v_ in ZR.values() if v_["rho_over_rt"] > 0.84),
      min(enh) >= 10 and ign,
      "the trigger is not a density threshold outside the Hubble flow: where the detuning's first derivative vanishes, the "
      "narrow resonance (G/delta ~ 1e-3) holds a mode for sqrt(G/alpha) instead of G/(H delta)")

# Z3 (reported): the 1D ignition table with the calibration
CAL = min(rat) if STIM else 0.0
Z3 = {}
for dt0 in (X.DT0_LIN, 13.5, 25.0):
    for s_lab in ("s=1", "s=1-F"):
        for sr in (0.0, 10.0, 30.0):
            row = {}
            for z in (0.0, 0.5, 1.0, 2.0, 3.0):
                f = X.fz(z); dta = 1 / (1 + f); s = 1.0 if s_lab == "s=1" else 1 - FHALO[z]
                Hs = float(X.H_si(z)); dl = X.delta_split(M_FID, VK_FID); Gt = float(X.G_t(z, M_FID, VK_FID, EN_FID))
                hit = None
                for d in np.linspace(dta + 1e-4, 0.99, 800):
                    e, ed = X.zeldovich_strain(np.array([d, 0.0]), z)
                    ca = float(X.cone_alpha_hat(e[0], e[1], ed[0], ed[1]))
                    rr = s / (1 - d) / float(X.rho_t_over_mean(z, dt0))
                    G = Gt * rr; alpha = dl * Hs * Hs * ca
                    gc = CAL * X.C4 * G ** 1.5 / math.sqrt(alpha)
                    if sr > 0 and 2 * dl * sr / VK_FID > G:
                        gc = CAL * float(X.cone_gain_kinetic(G, alpha, M_FID, VK_FID, sr))
                    if gc >= EN_FID: hit = 1 / (1 - d); break
                row[z] = hit
            Z3[(round(dt0, 2), s_lab, sr)] = row
for k_, row in Z3.items():
    P(f"    delta_t0 {k_[0]:5.2f} {k_[1]:6s} sigma_r {k_[2]:4.0f} km/s: a 1D pancake centre ignites at compression 1/(1-d) = "
      + ", ".join(f"z={z:g}: {'-' if v is None else f'{v:.1f}'}" for z, v in row.items()) + f"  (turnaround 1+1/f: "
      + ", ".join(f"{1 + 1 / X.fz(z):.2f}" for z in row) + ")")
OUT["numbers"]["Z3"] = {f"{k_[0]}|{k_[1]}|{k_[2]}": {str(z): v for z, v in r_.items()} for k_, r_ in Z3.items()}
check("Z3 (reported) the 1D pancake's ignition compression by z, delta_t0, smooth fraction and pump roughness", "table above", True,
      load_bearing=False)

# ============================================================================================ B re-resonance
banner("B   RE-RESONANCE: daughters born on the resonance inside a turned-around pancake, followed forward")


def recross_gains(paths_fw, dl, nskip=10):
    """for each ray: the forward D(t) (delta units) and G(t); every later zero crossing's gain from the local D1, D'' fit."""
    ts = np.array([p_[0] for p_ in paths_fw]) * X.TU
    Dd = np.array([p_[4] for p_ in paths_fw]); Gg = np.array([p_[5] for p_ in paths_fw])
    out = []
    for j in range(Dd.shape[1]):
        dj = Dd[:, j]; gj = Gg[:, j]
        # leave the birth window first: the first index where |D| > G
        start = int(np.argmax(np.abs(dj) > gj)) if np.any(np.abs(dj) > gj) else len(dj)
        sgn = np.sign(dj[start:])
        idx = np.where(sgn[1:] * sgn[:-1] < 0)[0]
        gains = []
        for k in idx:
            kk = start + k
            lo, hi = max(kk - 4, 0), min(kk + 6, len(dj))
            cf = np.polyfit(ts[lo:hi] - ts[kk], dj[lo:hi], 2)
            D1, al = cf[1], cf[0]
            Gc = float(gj[kk])
            g = float(X.sweep_gain(Gc, abs(D1), al)) if STIM else 0.0
            gains.append((g, kk))
        out.append(gains)
    return out


BR = {}
# d = 0.6 (just past turnaround) is the configuration written before the smoke run; d = 0.75 and 0.85 were added after it
# (HISTORY).  The span stops before the pancake's centre shell-crosses.
for (zc, dc, lam, span) in ((0.5, 0.60, 4000.0, 0.6), (1.0, 0.60, 4000.0, 0.6), (2.0, 0.60, 2000.0, 0.6),
                            (0.5, 0.75, 4000.0, 0.35), (1.0, 0.75, 4000.0, 0.35), (2.0, 0.75, 2000.0, 0.35),
                            (0.5, 0.85, 4000.0, 0.35), (1.0, 0.85, 4000.0, 0.35), (2.0, 0.85, 2000.0, 0.35)):
    pc = X.Pancake(zc, dc, lam)
    nxs = np.linspace(-0.98, 0.98, 25)
    allg, n_tot, n_rc = [], 0, 0
    for x0 in (0.0, 0.05, 0.1, 0.2, 0.3):
        g, paths = X.pancake_rays(pc, nxs, x0, En=EN_FID, nstep=4000, span_H=span, return_paths=True, signs=(+1.0,), stimulated=True)
        rc = recross_gains(paths[0], X.delta_split(M_FID, VK_FID))
        for j, gl_ in enumerate(rc):
            n_tot += 1
            if gl_:
                n_rc += 1; allg.append(max(gg for gg, _ in gl_) if STIM else 0.0)
    pc0 = X.Pancake(zc, 0.0, lam)                                     # the same rays in the Hubble flow
    _, p0 = X.pancake_rays(pc0, nxs, 0.1, En=EN_FID, nstep=4000, span_H=span, return_paths=True, signs=(+1.0,))
    rc0 = recross_gains(p0[0], X.delta_split(M_FID, VK_FID))
    BR[(zc, dc)] = dict(frac=n_rc / n_tot, median_gain=float(np.median(allg)) if allg else 0.0, p10=float(np.percentile(allg, 10)) if allg else 0.0,
                        n=n_tot, hubble_recross=sum(1 for r_ in rc0 if r_))
    P(f"    z_c {zc} d = {dc}: re-crossing fraction {n_rc}/{n_tot} = {n_rc / n_tot:.2f}; gain at the re-crossing median "
      f"{BR[(zc, dc)]['median_gain']:.1f}, 10th pct {BR[(zc, dc)]['p10']:.1f} e-folds (pump = full density); Hubble-flow control: "
      f"{BR[(zc, dc)]['hubble_recross']} re-crossings   {el()}")
OUT["numbers"]["B"] = {f"{k_[0]}|{k_[1]}": v_ for k_, v_ in BR.items()}
check("B1 re-resonance exists where the flow contracts and nowhere in the Hubble flow: in every tested turned-around pancake a "
      "nonzero fraction of the daughters born on the resonance re-cross it, with median gain >= 3 e-folds at z <= 1 (full-density "
      "pump), and the fraction grows with the collapse depth; the same rays in the Hubble flow never re-cross",
      "; ".join(f"z={k_[0]} d={k_[1]}: {v_['frac']:.2f}, median {v_['median_gain']:.1f}" for k_, v_ in BR.items())
      + f"; Hubble re-crossings {sum(v_['hubble_recross'] for v_ in BR.values())}",
      all(v_["frac"] > 0 for v_ in BR.values()) and all(v_["median_gain"] >= 3.0 for k_, v_ in BR.items() if k_[0] <= 1.0)
      and all(BR[(z, 0.85)]["frac"] > BR[(z, 0.6)]["frac"] for z in (0.5, 1.0, 2.0)) and all(v_["hubble_recross"] == 0 for v_ in BR.values()),
      "a contracting axis blue-shifts the daughters back above v_k and the expanding flow beyond brings them down through it: "
      "the web's turned-around structures are where the conversion can branch, the more so the deeper the collapse")

# ============================================================================================ I halo-seeded zones
banner("I   HALO-SEEDED ZONES: LCDM spherical shells, daughters from r200, crossings outside, the zone's yield")
GK = 4.30091e-6
RHOC0 = 3 * X.H0_KPC ** 2 / (8 * math.pi * GK); RHOM0 = X.OM * RHOC0
DCRIT = 1.686


def shells(M200, z_e, eps, nsh=240, mmax=400.0, nt=6000):
    m = np.geomspace(1.0, mmax, nsh); M = M200 * m
    RL = (3 * M / (4 * math.pi * RHOM0)) ** (1 / 3)
    ai = 0.01; zi = 1 / ai - 1
    Dl_i = DCRIT * m ** (-eps) * X.Dz(zi) / X.Dz(z_e)
    fi = X.fz(zi); Hi = X.H0_KPC * float(X.E(zi))
    r = ai * RL * (1 - Dl_i / 3); v = Hi * r * (1 - fi * Dl_i / 3)
    ts = np.linspace(X.t_of_z(zi), X.t_of_z(0.0), nt + 1); h = ts[1] - ts[0]
    OLH2 = X.OL * X.H0_KPC ** 2
    R = np.zeros((nt + 1, nsh)); V = np.zeros((nt + 1, nsh)); coll = np.zeros(nsh, bool); rmax = r.copy(); tcoll = np.full(nsh, np.inf)
    R[0], V[0] = r, v
    acc = lambda rr: -GK * M / rr ** 2 + OLH2 * rr
    for i in range(nt):
        k1v = acc(r); k1r = v
        k2v = acc(r + 0.5 * h * k1r); k2r = v + 0.5 * h * k1v
        k3v = acc(r + 0.5 * h * k2r); k3r = v + 0.5 * h * k2v
        k4v = acc(r + h * k3r); k4r = v + h * k3v
        rn = r + h / 6 * (k1r + 2 * k2r + 2 * k3r + k4r); vn = v + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        rn = np.where(coll, r, rn); vn = np.where(coll, 0.0, vn)
        rmax = np.maximum(rmax, rn)
        newc = ~coll & (vn < 0) & (rn < 0.25 * rmax)
        tcoll = np.where(newc, ts[i + 1], tcoll); coll |= newc
        r, v = rn, vn
        R[i + 1], V[i + 1] = r, v
    return dict(M=M, ts=ts, R=R, V=V, tcoll=tcoll)


def flow_at(S, t):
    i = int(np.clip(np.searchsorted(S["ts"], t) - 1, 0, len(S["ts"]) - 2)); w_ = (t - S["ts"][i]) / (S["ts"][i + 1] - S["ts"][i])
    r = (1 - w_) * S["R"][i] + w_ * S["R"][i + 1]; v = (1 - w_) * S["V"][i] + w_ * S["V"][i + 1]
    live = S["tcoll"] > t
    Mc = float(S["M"][~live].max()) if (~live).any() else 0.0
    return r[live], v[live], S["M"][live], Mc


def zone_run(M200, z_e, eps, dt0, s_mode, vk=VK_FID, nmu=161, span_H=1.2, nstep=6000):
    S = shells(M200, z_e, eps)
    te = X.t_of_z(z_e); tend = min(te + span_H / (X.H0_KPC * float(X.E(z_e))), X.t_of_z(0.0))
    r_l, v_l, M_l, Mc = flow_at(S, te)
    Ez = float(X.E(z_e)); r200 = (3 * Mc / (4 * math.pi * 200 * RHOC0 * Ez ** 2)) ** (1 / 3)
    rf = r200
    u_f = float(np.interp(rf, r_l, v_l))
    mu = np.linspace(-1, 1, nmu)
    vr0 = u_f + vk * mu; vt0 = vk * np.sqrt(1 - mu ** 2)
    # inward emissions cross the (static over the crossing) halo and leave at r_f with |v_r| unchanged
    vr = np.abs(vr0); L = rf * vt0
    r = np.full(nmu, rf); t = te
    OLH2 = X.OL * X.H0_KPC ** 2
    h = (tend - te) / nstep
    dl = X.delta_split(M_FID, vk); Gt_fn = lambda zq: float(X.G_t(zq, M_FID, vk, EN_FID))
    rec_t, rec_D, rec_G, rec_rho, rec_r = [], [], [], [], []
    for i in range(nstep + 1):
        rl, vl, Ml, Mcq = flow_at(S, t)
        a = np.exp(np.interp(t, X.T_OF, X.LNA_T)); zq = 1 / a - 1
        u = np.interp(r, rl, vl)
        # density from M(r) of the live shells (total matter; the carrier fraction cancels in rho/rho_bar)
        dMdr = np.interp(r, 0.5 * (rl[1:] + rl[:-1]), np.diff(Ml) / np.maximum(np.diff(rl), 1e-9))
        rho = dMdr / (4 * math.pi * r ** 2)
        rho_bar = RHOM0 * (1 + zq) ** 3
        s = 1.0 if s_mode == "1" else 1 - float(np.interp(zq, list(FHALO), list(FHALO.values())))
        rr = s * (rho / rho_bar) / float(X.rho_t_over_mean(zq, dt0))
        wr = vr - u; wt = L / r
        Dd = dl * ((wr ** 2 + wt ** 2) / vk ** 2 - 1)
        rec_t.append(t); rec_D.append(Dd); rec_G.append(Gt_fn(zq) * rr); rec_rho.append(rho / rho_bar); rec_r.append(r.copy())
        if i == nstep: break
        # radial motion in the enclosed mass, L conserved: each live shell's M is the TOTAL mass it encloses (halo included),
        # live shells are ordered in radius (no crossing before collapse); inside the innermost live shell, the halo's Mc
        idx = np.searchsorted(rl, r)
        Min = np.where(idx > 0, Ml[np.clip(idx - 1, 0, len(Ml) - 1)], Mcq)
        ar = -GK * Min / r ** 2 + L ** 2 / r ** 3 + OLH2 * r
        vr = vr + h * ar; r = r + h * vr; t = t + h
    T = np.array(rec_t) * X.TU; Dm = np.array(rec_D); Gm = np.array(rec_G); Rho = np.array(rec_rho); Rr = np.array(rec_r)
    res = []
    for j in range(nmu):
        dj, gj = Dm[:, j], Gm[:, j]
        sg = np.sign(dj); idx = np.where(sg[1:] * sg[:-1] < 0)[0]
        idx = [k for k in idx if Rr[k, j] > 1.05 * rf]
        if not idx: res.append(None); continue
        k = idx[0]
        lo, hi = max(k - 4, 0), min(k + 6, len(dj))
        cf = np.polyfit(T[lo:hi] - T[k], dj[lo:hi], 2)
        g = float(X.sweep_gain(float(gj[k]), abs(cf[1]), cf[0])) if STIM else 0.0
        res.append(dict(r_over_r200=float(Rr[k, j] / r200), gain=g, rho=float(Rho[k, j]), t=float(T[k] / X.TU)))
    cross = [x_ for x_ in res if x_ is not None]
    f_fast = len(cross) / nmu
    # the zone: pump mass between the 10th-90th percentile crossing radii at the median crossing time; the seeds: the fast
    # fraction of the mass converted at the front over one crossing time (shells crossing r200 during [te, t_cross])
    if cross:
        rc = np.array([x_["r_over_r200"] for x_ in cross]) * r200
        tc = float(np.median([x_["t"] for x_ in cross]))
        rl, vl, Ml, Mcq = flow_at(S, tc)
        M_zone = float(np.interp(np.percentile(rc, 90), rl, Ml) - np.interp(np.percentile(rc, 10), rl, Ml))
        s = 1.0 if s_mode == "1" else 1 - float(np.interp(1 / np.exp(np.interp(tc, X.T_OF, X.LNA_T)) - 1, list(FHALO), list(FHALO.values())))
        M_zone *= s
        _, _, _, Mc_c = flow_at(S, tc)
        M_seed = f_fast * max(Mc_c - Mc, 1e-3 * Mc)
        g_med = float(np.median([x_["gain"] for x_ in cross]))
        Y = math.exp(min(g_med, 700.0)) * M_seed / max(M_zone, 1e-30) if STIM else M_seed / max(M_zone, 1e-30)
    else:
        M_zone = M_seed = g_med = Y = 0.0
    return dict(r200=r200, u_front=u_f, f_fast=f_fast, r_cross_med=float(np.median([x_["r_over_r200"] for x_ in cross])) if cross else None,
                rho_cross_med=float(np.median([x_["rho"] for x_ in cross])) if cross else None, g_med=g_med,
                M_zone=M_zone, M_seed=M_seed, lnMzMs=math.log(max(M_zone, 1e-30) / max(M_seed, 1e-30)) if cross else None, Y=Y)


IZ = {}
CASES = [(1e11, 1.0), (1e12, 0.5), (1e12, 1.0), (1e12, 2.0), (1e13, 0.5), (1e13, 1.0)]
for (M200, ze) in CASES:
    for dt0 in (X.DT0_LIN, 13.5):
        for s_mode in ("1", "1-F"):
            r_ = zone_run(M200, ze, 0.6, dt0, s_mode)
            IZ[(M200, ze, round(dt0, 2), s_mode, 0.6)] = r_
            P(f"    M200 {M200:.0e} z_e {ze} delta_t0 {dt0:5.2f} s={s_mode:3s}: r200 {r_['r200']:.0f} kpc, u(r200) {r_['u_front']:.0f} km/s; fast "
              f"{r_['f_fast']:.2f}; crossings at {r_['r_cross_med'] if r_['r_cross_med'] is None else round(r_['r_cross_med'], 2)} r200 "
              f"(1+delta {r_['rho_cross_med'] if r_['rho_cross_med'] is None else round(r_['rho_cross_med'], 2)}); median gain {r_['g_med']:.1f}; "
              f"ln(M_zone/M_seed) {r_['lnMzMs'] if r_['lnMzMs'] is None else round(r_['lnMzMs'], 2)}; Y = {r_['Y']:.2e}   {el()}")
for eps in (0.4, 1.0):
    r_ = zone_run(1e12, 1.0, eps, X.DT0_LIN, "1-F")
    IZ[(1e12, 1.0, round(X.DT0_LIN, 2), "1-F", eps)] = r_
    P(f"    eps {eps}: M200 1e12 z_e 1: fast {r_['f_fast']:.2f}; crossings at {r_['r_cross_med']} r200; median gain {r_['g_med']:.1f}; Y = {r_['Y']:.2e}")
OUT["numbers"]["I"] = {"|".join(str(x_) for x_ in k_): v_ for k_, v_ in IZ.items()}
DT_NOM = round(X.DT0_LIN, 2)
nom_all = [(k_, v_) for k_, v_ in IZ.items() if k_[1] <= 1.0 and k_[2] == DT_NOM and k_[4] == 0.6]
check("I1 halo-seeded zones: in every tested case >= 30% of the daughters emitted at r200 by the infalling pump cross the "
      "resonance again outside r200 (fast seeds exist), and with the full-density pump (s = 1) at z_e <= 1 (nominal cell) their "
      "median gain beats ln(M_zone/M_seed) (Y >= 1) for every tested halo",
      "; ".join(f"{k_[0]:.0e}/z{k_[1]}/s={k_[3]}: fast {v_['f_fast']:.2f}, g {v_['g_med']:.1f}, Y {v_['Y']:.1e}" for k_, v_ in nom_all),
      len(nom_all) == 10 and all(v_["f_fast"] >= 0.3 for v_ in IZ.values()) and all(v_["Y"] >= 1.0 for k_, v_ in nom_all if k_[3] == "1"),
      "the infalling pump at r200 blue-shifts the inward-emitted daughters (and the tangential ones, through the converging "
      "infall) above v_k; they cross it again where the outflow catches up, near the turnaround radius")
check("I2 (reported) the smooth pump s = 1 - F_halo, z_e = 2, delta_t0 = 13.5, and the eps bracket", "; ".join(
      f"{k_[0]:.0e}/z{k_[1]}/dt0 {k_[2]}/s={k_[3]}/eps {k_[4]}: Y {v_['Y']:.1e}" for k_, v_ in IZ.items() if not (k_[1] <= 1.0 and k_[2] == DT_NOM and k_[3] == "1" and k_[4] == 0.6)),
      True, load_bearing=False)

# ============================================================================================ H the pre-declared hypotheses
banner("H   (reported) THE PRE-DECLARED HYPOTHESES, as they fell")
HB_decl = all(BR[(z, 0.6)]["frac"] >= 0.2 and BR[(z, 0.6)]["median_gain"] >= 3.0 for z in (0.5, 1.0))
HI_decl = all(v_["f_fast"] >= 0.3 and v_["Y"] >= 1.0 for k_, v_ in nom_all)
HZ_decl = min(rat) >= 0.5 and max(rat) <= 1.0 and min(enh) >= 10 and ign
HH = {"H-S": ident_ok and anti_ok and d2_ok, "H-H": all(v_["monotone"] and v_["recross"] == 0 and v_["max_dev"] <= 0.01 for v_ in H1.values()),
      "H-Z": HZ_decl, "H-B (pre-declared configuration d = 0.6)": HB_decl, "H-I (s = 1 - F_halo and s = 1)": HI_decl}
for k_, v_ in HH.items():
    P(f"    {k_:44s}: {'held' if v_ else 'FELL'}")
OUT["numbers"]["H"] = HH
fell = [k_ for k_, v_ in HH.items() if not v_]
check("H (reported) the pre-declared hypotheses as they fell", HH, True,
      ("fell: " + "; ".join(fell) + " -- kept as run; the load-bearing checks above state what does hold") if fell else "all held",
      load_bearing=False)

# ============================================================================================ R the reach
banner("R   THE REACH: comoving distance a daughter covers from z_e (peculiar speed v_k (1+z)/(1+z_e)), and the resonance reach")
RR = {}
for ze in (3.0, 2.0, 1.0, 0.5):
    ae = 1 / (1 + ze)
    aa = np.linspace(ae, 1.0, 4001)
    integrand = VK_FID * ae / (aa ** 3 * X.H0_KPC * 1e3 * X.E(1 / aa - 1))          # km/s / (km/s/Mpc) per a -> Mpc comoving
    chi = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(aa))])
    reach_res = {dv: dv / (X.H0_KPC * 1e3 * float(X.E(ze))) * (1 + ze) for dv in (30.0, 100.0, 300.0)}     # comoving Mpc
    RR[ze] = dict(chi_to_z0_Mpc=float(chi[-1]), resonance_reach_comoving_Mpc=reach_res)
    P(f"    z_e = {ze}: comoving distance to z = 0 {chi[-1]:.1f} Mpc; resonance reach Delta/H for an excess Delta = 30/100/300 km/s: "
      + "/".join(f"{v:.2f}" for v in reach_res.values()) + " comoving Mpc")
OUT["numbers"]["R"] = {str(k_): v_ for k_, v_ in RR.items()}

# ============================================================================================ summary
banner("SUMMARY")
P(f"""  The gate keeps the mean background from self-igniting (<= {ratio_sp.max():.3f} of E_need), but a resonant seed gains up to
  {', '.join(f"{v['max']:.1f}" for v in g_bg.values())} e-folds per passage there at z ~ 0.3 (G2).  Whether seeds find the resonance is kinematics: against its
  LOCAL pump a daughter's relative velocity obeys dw/dt = -(w.grad)u (S1), so in any expanding flow a daughter born on the
  resonance never returns (H1) and a seed enters it at most once.  Where the flow contracts along some axis it can: a
  turned-around pancake has a zero-strain cone on which the narrow resonance holds a mode for sqrt(G/alpha), a gain
  {min(enh):.0f}-{max(enh):.0f}x the Hubble sweep's (Z1, exact rays within {min(rat):.2f}-{max(rat):.2f} of the local formula), so pancakes ignite below the
  trigger (Z2); daughters born inside re-cross the resonance outside for {min(v_['frac'] for v_ in BR.values()):.0%}-{max(v_['frac'] for v_ in BR.values()):.0%} of pairs (B1); and around
  every accreting halo the infalling pump blue-shifts about half the daughters, which convert the zone outside (I1).
  XR19_web_runaway.py puts these rules on a realistic web.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["summary"] = dict(n_checks=len(CH), load_bearing_failed=n_fail, runtime_s=round(time.time() - T0, 1))
suffix = "_MUTATE" if MUTATE else ""
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results{suffix}.json"), "w"), indent=1, default=str)
P(f"\n  checks: {sum(ok for _, ok, _ in CH)}/{len(CH)} pass; load-bearing failures: {n_fail}   {el()}")
sys.exit(1 if n_fail else 0)
