"""CFG88 POST-COMPARISON (written AFTER my frozen main/MUTATE/sensitivity runs and AFTER opening CFG42's script; labelled as such, changes no frozen number).
Tests the two differences found by reading CFG42's script: (D1) 'expectation' = max(current gas, E[neighbour ratio]) (my A2), and Upsilon_V variation moves ONLY the stellar
mass (their halo mass and infall gas stay at Upsilon = 2); (D2) error of a non-KM median = 1.2533 rms/sqrt(n) (not my bootstrap).  Run: python3 cfg88_post.py"""
import math, numpy as np
import cfg88 as C
from cfg88 import Cfg, load, load_collins, calib_set, mstar_from_MV, mcoll_from_mstar, edge_phantom, nfw_enclosed, conc_DM, KERNELS, A0, FB, G, MSUN, KPC, gas_ratio, med, boot_stat
ufd, cls, lvd, lf = load(); col = load_collins(); CAL = calib_set(lf)
FLOORS = (1e8, 3e8, 1e9, 3e9, 1e10)
def predict_post(s, cfg, CAL_, want_detail=False):
    a0 = A0[cfg.foot]; nu = KERNELS[cfg.kernel]; conc = C.CONC[cfg.conc]
    Mst = mstar_from_MV(s["MV"], cfg.ups); Mst2 = mstar_from_MV(s["MV"], 2.0)
    rg = gas_ratio(s, cfg.copy(ups=2.0), CAL_)            # gas fixed at the Upsilon = 2 value (absolute)
    Mb = Mst + rg * Mst2
    r = 4 / 3 * s["Re_pc"] * 1e-3 * KPC
    gN = G * (Mb * MSUN / 2) / r ** 2; g = nu(gN / a0) * gN; dark = 0.0; fex = 0.0
    if cfg.phi != 0.0:
        Mc = mcoll_from_mstar(Mst2, clamp=cfg.clamp, unclamped=cfg.unclamped)     # halo mass at Upsilon = 2
        if cfg.small_mcoll is not None and Mst2 < 1e5: Mc = cfg.small_mcoll
        if cfg.fixed_mcoll is not None: Mc = cfg.fixed_mcoll
        Mc /= cfg.mcoll_div
        Mph, _ = edge_phantom(Mb, a0, nu); fex = max(0.0, 1 - Mph / ((1 - FB) * Mc))
        dark = cfg.phi * G * fex * (1 - FB) * nfw_enclosed(Mc, r / KPC, conc) * MSUN / r ** 2
    sg = math.sqrt((g + dark) * r / 3) / 1e3
    return (sg, dict(fex=fex)) if want_detail else sg
C.predict = predict_post
def offs(P, cfg): return C.offsets(P, cfg, CAL)
def cfg42_row(P, foot, rule, ulmode=False):
    base = Cfg(foot=foot, phi=1.0 if rule else 0.0, gas="A2")
    cens = np.array([s["ul"] for s in P]); x = offs(P, base); m = med(x, cens)
    if ulmode: err = boot_stat(x, cens, nb=1000, seed=42)
    else: err = 1.2533 * float(np.std(x)) / math.sqrt(len(x))
    ms = [med(offs(P, base.copy(ups=u)), cens) for u in (1.0, 4.0)]; fU = 0.5 * abs(ms[1] - ms[0])
    if rule:
        fl = [med(offs(P, base.copy(small_mcoll=v)), cens) for v in FLOORS]; fC = 0.5 * (max(fl) - min(fl))
    else: fC = 0.0
    tot = math.sqrt(err ** 2 + fU ** 2 + fC ** 2)
    return m, err, fU, fC, tot, m / tot
print("CFG42-style recipe re-implemented in my code (gas A2, halo mass and gas fixed at Upsilon=2 under the Upsilon scan, error 1.2533 rms/sqrt n; KM bootstrap for UFD)")
targets = {("ufd", "canonical", 0): "+0.325 (3.77s)", ("ufd", "alt", 0): "+0.304 (3.55s)", ("ufd", "canonical", 1): "-0.059 +-0.143 (-0.41s)", ("ufd", "alt", 1): "-0.059 (-0.41s)",
           ("cls", "canonical", 0): "+0.027", ("cls", "alt", 0): "+0.008", ("cls", "canonical", 1): "-0.118 (-1.78s)", ("cls", "alt", 1): "-0.123 (-1.90s)",
           ("col", "canonical", 0): "+0.064", ("col", "alt", 0): "+0.045", ("col", "canonical", 1): "-0.024 (-0.22s)", ("col", "alt", 1): "-0.016",
           ("m31", "canonical", 0): "+0.044 (0.6s)", ("m31", "alt", 0): "+0.031", ("m31", "canonical", 1): "-0.107 (-2.67s, e 0.040)", ("m31", "alt", 1): "-0.109 (-2.66s)"}
PP = {"ufd": ufd, "cls": cls, "col": col, "m31": lvd}
for (k, foot, rule), t in targets.items():
    m, e, fU, fC, tot, z = cfg42_row(PP[k], foot, rule, ulmode=(k == "ufd"))
    print(f"{k:4s} {foot:9s} {'rule' if rule else 'law '}: {m:+.4f} +- {tot:.3f} ({z:+.2f}s) [err {e:.3f} U {fU:.3f} C {fC:.3f}]   CFG42 README: {t}")
# R1 scan at their grid values
print("\nR1 scan at CFG42's logspace(7.5,12,19)[::3] grid (small satellites only), canonical, CFG42-style predictor:")
cens = np.array([s["ul"] for s in ufd])
for v in np.logspace(7.5, 12, 19)[::3]:
    print(f"   {v:.2e}: {med(offs(ufd, Cfg(small_mcoll=v, gas='A2')), cens):+.3f}")
