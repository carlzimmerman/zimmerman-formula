#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR12 (4/4) -- DOES HALO SPIN, FED BY FILAMENTS, CHANGE RETENTION?  ("swirling down between the bands", question B)

WHY.  If the dark fluid spirals into halos along filaments, the halo's inner fluid rotates.  Three ways that could move
the construction's clearing and retention numbers: (1) centrifugal support lowers the inner density, and FK1's
conversion rate goes as n^2; (2) a superfluid can rotate only through quantised vortices, whose cores are empty; (3)
the kicked daughters leave a rotating pump, so a prograde daughter starts faster than a retrograde one.  This lane
sizes all three and compares them with the gates' tolerances: the flagship's S <= 0.059 at r_F (MS2), and the X-COP
window, where L388's pooled retention (0.374-0.607 over 575-650 km/s) sits 0.088 above the floor (0.286) and 0.161
below the ceiling (0.768).

MODEL.  NFW hosts (Dutton & Maccio 2014 c(M, z)).  Rotation v_phi(r, theta) = eta v_c(r) sin(theta), with eta fixed by the
Bullock spin lambda' = J/(sqrt(2) M_200 V_200 r_200) (J = (2/3) eta int r v_c dM), lambda' = 0.03-0.05 (0.035 the median).
Escape: XR7's static model (an NFW halo with isotropic Jeans velocities, every carrier element converting at once, a
daughter kept iff its energy stays bound), re-implemented, with the rotation added to each pump element's velocity --
either on top of the Jeans dispersion ('added') or at fixed kinetic energy ('energy-conserving': sigma^2 -> sigma^2 -
(2/9) eta^2 v_c^2).  Each converting pair leaves back to back in the pump's frame, so one daughter is prograde and one
retrograde: the pair average removes the first order in v_rot/v_k.
CHECKS
  B0 CONTROL: the re-implementation reproduces XR7's committed static-model 50% retention v_200 at 575/600/625/650 km/s,
     both potential references, EXACTLY (same random numbers).
  B1 [load-bearing claim] centrifugal support: for lambda' <= 0.05 the rotation's share of the support is <= 5%, the density
     at r_F falls by <= 10% (isothermal-slope estimate), so the n^2 rate there falls by <= 20% -- far inside the flagship's
     trigger margin (rho(r_F) = 12.7-44x the nominal threshold, XR12_forest_halo_model W) -- and the conversion edge moves
     by <= 4% in radius, inside FK1's 6% density sharpness.  (The drop at 0.1 r_200 is reported: no gate sits there.)
  B2 [load-bearing claim] the vortex lattice (Feynman: n_v = m Omega/(pi hbar)): spacing >= 10 pc for m <= 1e-17 eV in
     the flagship host and in a cluster; the cores' filling fraction is < 1e-5, and the lattice is < 1e-3 of the random
     vortex tangle that multistreaming already carries (one node per de Broglie cell, XR8/FL2 V6).
  B3 [load-bearing claim] escape: with lambda' = 0.05 the prograde-minus-retrograde escape asymmetry is first order, but
     the pair-averaged retention moves by < 0.0088 (a tenth of the X-COP margin) at every host mass, and the 50%
     transition moves by < 5% in v_200, for both rotation variants and every kick.
  B4 [load-bearing claim] the flagship: rotation changes the escape fraction of daughters born at r_F by < 0.0059 (a
     tenth of S's tolerance).
MUTATE=1: eta = 1 (a dark fluid rotating at the circular speed, a rotation-supported disc): B3 must FAIL (rc = 1).

A0 FOOTINGS.  Nothing here reads a0 except r_F (canonical 38.6 kpc, alt 35.2 kpc); both are evaluated in B4.

SCOPE.  Static halos (no assembly, as XR7's static model; the committed PM retention with assembly is 1.8-3.3x higher in
transition mass, XR7); a smooth rotation law; the vortex-core size taken as the local de Broglie scale lambda_dB/(2 pi)
(FL1's nearly free field has no smaller healing length).  Read-only on every other file.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR12_spin_retention.py
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, json, math, time
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR12_spin_retention"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR12", "part": "4/4 spin", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split(" ")[0]] = {"ok": ok, "claim": name, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 112); P(t); P("=" * 112)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: eta = 1 (rotation at the circular speed); B3 must FAIL ***")

# ============================================================================================ XR7's static model, re-implemented
G = 4.30091e-9                                   # Mpc (km/s)^2 / Msun (XR7)
h = 0.6736
OM_PM = 0.3138
RHOC0 = 2.775e11 * h ** 2                        # Msun / Mpc^3
mfun = lambda x: np.log1p(x) - x / (1 + x)


def c_dm14(M200, z=0.0):
    a = 0.520 + (0.905 - 0.520) * math.exp(-0.617 * z ** 1.21); b = -0.101 + 0.026 * z
    return 10 ** (a + b * math.log10(M200 / (1e12 / h)))


def rho_c(z, om=OM_PM):
    return RHOC0 * (om * (1 + z) ** 3 + 1 - om)


class NFW:
    def __init__(self, M200, z=0.0, om=OM_PM):
        self.M200, self.z = M200, z; self.c = c_dm14(M200, z)
        self.r200 = (3 * M200 / (4 * math.pi * 200 * rho_c(z, om))) ** (1 / 3); self.rs = self.r200 / self.c
        self.v200 = math.sqrt(G * M200 / self.r200); self.mc = float(mfun(self.c))


YG = np.geomspace(1e-5, 1e5, 40000); FY = mfun(YG) / (YG ** 3 * (1 + YG) ** 2)
TAILY = np.concatenate([np.cumsum((0.5 * (FY[1:] + FY[:-1]) * np.diff(YG))[::-1])[::-1], [0.0]])
rng_s = np.random.default_rng(20260926); NS_ = 40000
U_ = rng_s.random(NS_); GV = rng_s.normal(size=(NS_, 3)); NK = rng_s.normal(size=(NS_, 3)); NK /= np.linalg.norm(NK, axis=1)[:, None]
MU_ = np.random.default_rng(1729).uniform(-1, 1, NS_)          # position cos(theta) for the rotation (a separate stream)
SINT = np.sqrt(1 - MU_ ** 2)


def crossing(x, y, L, extrapolate=False):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if y[0] >= L:
        return float("nan"), "below"
    for i in range(len(x) - 1):
        if y[i] < L <= y[i + 1]:
            return float(x[i] + (L - y[i]) * (x[i + 1] - x[i]) / (y[i + 1] - y[i])), "in"
    return float("nan"), "above"


def static_retained(M200, vk, ref, eta=0.0, mode="added", z=0.0, split=False):
    """XR7's static_retained(); eta > 0 adds the rotation eta v_c(r) sin(theta) phi_hat to each pump element."""
    Hh = NFW(M200, z); c = Hh.c; xg = np.geomspace(1e-4, c, 4000); x = np.interp(U_ * float(mfun(c)), mfun(xg), xg)
    s2 = (c / float(mfun(c))) * x * (1 + x) ** 2 * np.interp(np.log(x), np.log(YG), TAILY)
    v = GV * np.sqrt(s2)[:, None] * Hh.v200
    if eta > 0:
        vc = Hh.v200 * np.sqrt(c * mfun(x) / (x * float(mfun(c))))
        u = eta * vc * SINT
        if mode == "energy":
            scale = np.sqrt(np.clip(1 - (2.0 / 9.0) * (eta * vc) ** 2 / (s2 * Hh.v200 ** 2), 0.0, None))
            v = v * scale[:, None]
        v = v.copy(); v[:, 0] += u                                                  # phi_hat = x_hat in the local frame
    phi = -(Hh.v200 ** 2 * c / float(mfun(c))) * np.log1p(x) / x
    pref = 0.0 if ref == "inf" else -(Hh.v200 ** 2 * c / float(mfun(c))) * math.log1p(2 * c) / (2 * c)
    b0 = 0.5 * np.sum(v ** 2, 1) + phi < pref
    b_p = 0.5 * np.sum((v + vk * NK) ** 2, 1) + phi < pref                          # the daughter kicked along n
    if not split:
        return float(b_p.sum() / max(b0.sum(), 1))
    b_m = 0.5 * np.sum((v - vk * NK) ** 2, 1) + phi < pref                          # its back-to-back partner
    pro = NK[:, 0] > 0
    kept_pro = np.where(pro, b_p, b_m); kept_ret = np.where(pro, b_m, b_p)
    return dict(pair=float((b_p.sum() + b_m.sum()) / (2 * max(b0.sum(), 1))),
                prograde=float(kept_pro.sum() / max(b0.sum(), 1)), retrograde=float(kept_ret.sum() / max(b0.sum(), 1)))


LMG = np.arange(11.5, 15.01, 0.05)
VK = (575.0, 600.0, 625.0, 650.0)

# ============================================================================================ B0 XR7 reproduced
banner("B0  CONTROL: XR7's committed static-model 50% retention v_200 reproduced exactly")
X7 = json.load(open(os.path.join(HERE, "XR7_kick_escape_vs_cap_results.json")))["numbers"]["static_model"]
B0 = {}; dev = 0.0
for vk in VK:
    for ref in ("inf", "2r200"):
        ret = np.array([static_retained(10 ** lm, vk, ref) for lm in LMG])
        x_, fl = crossing(LMG, ret, 0.5)
        v200 = NFW(10 ** x_).v200
        B0[f"{int(vk)}/{ref}"] = v200
        dev = max(dev, abs(v200 - X7[f"{int(vk)}/{ref}"]["50%"]["v200"]))
P("    50% retention v_200: " + ", ".join(f"{k_} {v:.4f} (XR7 {X7[k_]['50%']['v200']:.4f})" for k_, v in B0.items()))
OUT["numbers"]["B0"] = dict(v200_50=B0, max_dev=dev)
check("B0 CONTROL: XR7's static-model 50% transition reproduced exactly (8 cells)", f"max |dv_200| = {dev:.2e} km/s", dev < 1e-6)

# ============================================================================================ eta from lambda'
banner("SPIN  eta(lambda') for the rotation law v_phi = eta v_c(r) sin(theta)")


def eta_of_lambda(lam, c):
    mc = float(mfun(c))
    I = quad(lambda x: (x / (1 + x) ** 2 / mc) * (x / c) * math.sqrt(c * float(mfun(x)) / (x * mc)), 0, c)[0]
    return 1.5 * math.sqrt(2) * lam / I


LAMS = (0.03, 0.035, 0.05)
ETA = {}
for lam in LAMS:
    ETA[str(lam)] = {f"c={c:g}": eta_of_lambda(lam, c) for c in (4.0, 7.0, 10.0)}
    P(f"    lambda' = {lam}: eta = " + ", ".join(f"{k_} {v:.3f}" for k_, v in ETA[str(lam)].items())
      + f"  -> rotational share of the support (2/3) eta^2 = " + ", ".join(f"{(2 / 3) * v ** 2:.4f}" for v in ETA[str(lam)].values()))
ETA_MAX = 1.0 if MUTATE else max(max(v.values()) for v in ETA.values())
OUT["numbers"]["eta"] = dict(table=ETA, eta_used_max=ETA_MAX)

# ============================================================================================ B1 centrifugal support
banner("B1  CENTRIFUGAL SUPPORT: the inner density, the n^2 rate, and where the conversion edge sits")
f_rot = (2.0 / 3.0) * ETA_MAX ** 2
B1 = {}
for lab, r_over_rvir in (("r_F in the flagship host (~0.44 r_200)", 0.44), ("0.1 r_200", 0.1), ("conversion edge ~1-3 r_200", 1.0)):
    drho = 1 - r_over_rvir ** (2 * f_rot)                                         # isothermal-slope estimate, normalised at r_vir
    B1[lab] = dict(delta_rho=drho, delta_rate=1 - (1 - drho) ** 2)
    P(f"    {lab:40s}: support share {f_rot:.4f} -> density lower by {drho:.3%}, n^2 rate lower by {B1[lab]['delta_rate']:.3%}")
edge_shift = f_rot / 2.0                                                          # rho ~ r^-2 near the edge: dlnr = dlnrho/2
P(f"    the conversion edge (n = n_t, where rho ~ r^-2 to r^-3) moves inward by <= {edge_shift:.2%}; FK1's threshold is sharp to 6% in "
  f"density (N1: negligible below 0.942 n_t)")
P("    the flagship: rho(r_F) = 12.7-44x the nominal threshold (XR12_forest_halo_model W) -> a <= 10% drop cannot un-trigger r_F")
OUT["numbers"]["B1"] = dict(support_share=f_rot, radii=B1, edge_shift=edge_shift)
worst_rho = B1["r_F in the flagship host (~0.44 r_200)"]["delta_rho"]
check("B1 centrifugal support at lambda' <= 0.05 is <= 5% of the support, lowers the density at r_F by <= 10% and the n^2 "
      "rate there by <= 20%, and moves the conversion edge by <= 4% -- inside the flagship's trigger margin (>= 12.7x) and "
      "FK1's 6% sharpness (0.1 r_200 is reported, not gated: no gate sits there)",
      f"support {f_rot:.4f}; density drop at r_F {worst_rho:.3%} (rate {B1['r_F in the flagship host (~0.44 r_200)']['delta_rate']:.3%}); "
      f"at 0.1 r_200 {B1['0.1 r_200']['delta_rho']:.3%}; edge shift {edge_shift:.2%}",
      f_rot <= 0.05 and worst_rho <= 0.10 and B1["r_F in the flagship host (~0.44 r_200)"]["delta_rate"] <= 0.20 and edge_shift <= 0.04,
      "spin cannot switch the trigger off where it matters: r_F sits an order of magnitude above threshold")

# ============================================================================================ B2 the vortex lattice
banner("B2  THE VORTEX LATTICE a rotating superfluid halo must carry (Feynman: n_v = m Omega / (pi hbar))")
HBAR_SI, EV_KG, KPC_M, PC_M = 1.054571817e-34, 1.78266192e-36, 3.0857e19, 3.0857e16
B2 = {}
hosts = {"flagship r_F (1e12, z=2.5)": dict(M=1e12, z=2.5, r_kpc=38.6), "cluster R_500 (8e14, z=0)": dict(M=8e14, z=0.0, r_kpc=1000.0)}
for hn, hp in hosts.items():
    Hh = NFW(hp["M"], hp["z"]); x = hp["r_kpc"] / 1e3 / Hh.rs
    vc = Hh.v200 * math.sqrt(Hh.c * float(mfun(x)) / (x * Hh.mc)); sig = vc / math.sqrt(2)
    eta_h = 1.0 if MUTATE else eta_of_lambda(0.05, Hh.c)
    Om_ = eta_h * vc * 1e3 / (hp["r_kpc"] * KPC_M)                                # s^-1
    for mev in (2e-19, 5e-19, 1e-17):
        m_ = mev * EV_KG
        n_v = m_ * Om_ / (math.pi * HBAR_SI)                                      # per m^2 (solid-body 2 Omega: an upper bound)
        ell = n_v ** -0.5 / PC_M                                                  # pc
        lam_dB = 2 * math.pi * HBAR_SI / (m_ * sig * 1e3) / PC_M                  # pc
        core = lam_dB / (2 * math.pi)
        fill = math.pi * core ** 2 / ell ** 2
        tangle = ell ** 2 / lam_dB ** 2                                           # random nodes per lattice cell
        N_v = 2 * math.pi * hp["r_kpc"] * KPC_M * eta_h * vc * 1e3 * m_ / (2 * math.pi * HBAR_SI)
        B2[f"{hn}/{mev:g}"] = dict(v_rot=eta_h * vc, spacing_pc=ell, lambda_dB_pc=lam_dB, core_pc=core, filling=fill,
                                   lattice_over_tangle=1 / tangle, N_vortices=N_v)
        P(f"    {hn:28s} m = {mev:.0e} eV: v_rot {eta_h * vc:5.1f} km/s -> spacing {ell:8.2f} pc, {N_v:.1e} vortices; core ~ "
          f"lambda_dB/2pi = {core:.4f} pc, filling {fill:.1e}; lattice / random tangle {1 / tangle:.1e}")
OUT["numbers"]["B2"] = B2
check("B2 the rotation's vortex lattice is sparse (spacing >= 10 pc for m <= 1e-17 eV), its cores fill < 1e-5 of the volume, "
      "and it is < 1e-3 of the random vortex tangle the multistreaming field already carries",
      f"min spacing {min(v['spacing_pc'] for v in B2.values()):.1f} pc; max filling {max(v['filling'] for v in B2.values()):.1e}; "
      f"max lattice/tangle {max(v['lattice_over_tangle'] for v in B2.values()):.1e}",
      min(v["spacing_pc"] for v in B2.values()) >= 10 and max(v["filling"] for v in B2.values()) < 1e-5
      and max(v["lattice_over_tangle"] for v in B2.values()) < 1e-3,
      "the superfluid carries its spin as a vanishing polarisation of nodes it already has: no effect on n^2")

# ============================================================================================ B3 escape with a rotating pump
banner(f"B3  ESCAPE FROM A ROTATING PUMP: pair-averaged retention and the prograde/retrograde split (eta = {ETA_MAX:.3f})")
B3 = {}
worst_d, worst_shift, asym_max = 0.0, 0.0, 0.0
for vk in VK:
    for ref in ("inf", "2r200"):
        base_pair = np.array([static_retained(10 ** lm, vk, ref, split=True)["pair"] for lm in LMG])
        for mode in ("added", "energy"):
            rot = [static_retained(10 ** lm, vk, ref, eta=ETA_MAX, mode=mode, split=True) for lm in LMG]
            pair = np.array([r_["pair"] for r_ in rot])
            d = float(np.max(np.abs(pair - base_pair)))
            x1, _ = crossing(LMG, pair, 0.5); x1b, _ = crossing(LMG, base_pair, 0.5)
            sh = abs(NFW(10 ** x1).v200 / NFW(10 ** x1b).v200 - 1) if np.isfinite(x1) and np.isfinite(x1b) else float("inf")
            asym = float(np.max(np.abs(np.array([r_["prograde"] - r_["retrograde"] for r_ in rot]))))
            B3[f"{int(vk)}/{ref}/{mode}"] = dict(max_delta_retention=d, v200_50_shift=sh, max_pro_minus_retro=asym,
                                                 v200_50_base=NFW(10 ** x1b).v200 if np.isfinite(x1b) else None)
            worst_d = max(worst_d, d); worst_shift = max(worst_shift, sh); asym_max = max(asym_max, asym)
    P(f"    v_k {vk:.0f}: " + "; ".join(f"{k_.split('/', 1)[1]}: dR {v['max_delta_retention']:.4f}, d v50 {v['v200_50_shift']:.2%}, "
                                     f"pro-retro {v['max_pro_minus_retro']:+.3f}" for k_, v in B3.items() if k_.startswith(f"{int(vk)}/")))
xc = {}
for mode in ("added", "energy"):
    r0_ = static_retained(8e14, 600.0, "inf", split=True)["pair"]; r1_ = static_retained(8e14, 600.0, "inf", eta=ETA_MAX, mode=mode, split=True)["pair"]
    xc[mode] = (r0_, r1_)
P("    an X-COP-like host (8e14, 600 km/s, Phi(inf)): retention " + ", ".join(f"{m_}: {a:.4f} -> {b:.4f}" for m_, (a, b) in xc.items()))
OUT["numbers"]["B3"] = dict(cells=B3, worst_delta=worst_d, worst_v50_shift=worst_shift, max_asymmetry=asym_max, xcop_host=xc)
check("B3 with lambda' = 0.05 the pair-averaged retention moves by < 0.0088 (a tenth of the X-COP margin) at every host mass "
      "and the 50% transition by < 5% in v_200, both rotation variants and every kick -- although single daughters show a "
      "first-order prograde/retrograde asymmetry", f"max |dR| = {worst_d:.4f}; max v50 shift {worst_shift:.2%}; "
      f"max prograde - retrograde {asym_max:+.3f}",
      worst_d < 0.0088 and worst_shift < 0.05,
      "back-to-back pairs cancel the first order in v_rot/v_k; what is left is second order, (v_rot/v_k)^2 against a "
      "Jeans dispersion that already dwarfs v_rot")

# ============================================================================================ B4 the flagship's r_F
banner("B4  THE FLAGSHIP: escape of daughters born at r_F, with and without the rotation (both footings)")
B4 = {}
Hf = NFW(1e12, 2.5)
rng4 = np.random.default_rng(4242); g4 = rng4.normal(size=(200000, 3)); n4 = rng4.normal(size=(200000, 3))
n4 /= np.linalg.norm(n4, axis=1)[:, None]; st4 = np.sqrt(1 - rng4.uniform(-1, 1, 200000) ** 2)
for f_, rF in (("canonical", 38.6), ("alt", 35.2)):
    x = rF / 1e3 / Hf.rs
    vc = Hf.v200 * math.sqrt(Hf.c * float(mfun(x)) / (x * Hf.mc))
    s = Hf.v200 * math.sqrt((Hf.c / Hf.mc) * x * (1 + x) ** 2 * float(np.interp(math.log(x), np.log(YG), TAILY)))
    phi = -(Hf.v200 ** 2 * Hf.c / Hf.mc) * math.log1p(x) / x
    eta_f = 1.0 if MUTATE else eta_of_lambda(0.05, Hf.c)
    out_ = {}
    for vk in VK:
        esc = {}
        for et in (0.0, eta_f):
            v = g4 * s; v = v.copy(); v[:, 0] += et * vc * st4
            ep = 0.5 * np.sum((v + vk * n4) ** 2, 1) + phi > 0; em = 0.5 * np.sum((v - vk * n4) ** 2, 1) + phi > 0
            esc[et] = float((ep.sum() + em.sum()) / (2 * len(ep)))
        out_[f"{int(vk)}"] = dict(escape_norot=esc[0.0], escape_rot=esc[eta_f], delta=abs(esc[eta_f] - esc[0.0]))
    B4[f_] = dict(r_F=rF, v_c=vc, sigma=s, v_esc=math.sqrt(-2 * phi), eta=eta_f, by_kick=out_)
    P(f"    {f_:9s} r_F = {rF} kpc: v_c {vc:.0f}, sigma {s:.0f}, v_esc (full LCDM halo) {math.sqrt(-2 * phi):.0f} km/s; escape "
      + ", ".join(f"{k_}: {v['escape_norot']:.4f} -> {v['escape_rot']:.4f}" for k_, v in out_.items()))
d4 = max(v["delta"] for b in B4.values() for v in b["by_kick"].values())
OUT["numbers"]["B4"] = B4
check("B4 at the flagship radius the rotation changes the daughters' escape fraction by < 0.0059 (a tenth of S's tolerance), "
      "both footings, every kick -- even in the full, uncleared LCDM potential", f"max |d escape| = {d4:.4f}", d4 < 0.0059,
      "spin cannot bring S(r_F) near 0.059")

# ============================================================================================ summary
banner("SUMMARY")
P(f"""  Question (B): does filament-fed spin change retention?  No, not at any level the gates can see.
  - Centrifugal support at lambda' <= 0.05: {f_rot:.1%} of the support; the density at r_F drops <= {worst_rho:.1%}; r_F stays 12.7-44x
    above threshold; the conversion edge moves <= {edge_shift:.1%} (B1).
  - The vortex lattice: spacing >= {min(v['spacing_pc'] for v in B2.values()):.0f} pc, filling <= {max(v['filling'] for v in B2.values()):.0e}, a
    <= {max(v['lattice_over_tangle'] for v in B2.values()):.0e} polarisation of the random node tangle (B2).
  - Escape: single daughters split prograde/retrograde by up to {asym_max:+.3f}, but each pair has one of each, and the pair-averaged
    retention moves by <= {worst_d:.4f} (X-COP margin 0.088), the 50% transition by <= {worst_shift:.1%} (B3); at r_F by <= {d4:.4f} (B4).""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["summary"] = dict(load_bearing_failed=n_fail, n_checks=len(CH), runtime_s=round(time.time() - T0, 1))
suffix = "_MUTATE" if MUTATE else ""
json.dump(OUT, open(os.path.join(HERE, f"{SLUG}_results{suffix}.json"), "w"), indent=1, default=str)
P(f"\n  checks: {sum(ok for _, ok, _ in CH)}/{len(CH)} pass; load-bearing failures: {n_fail}   [{time.time() - T0:.0f}s]")
sys.exit(1 if n_fail else 0)
