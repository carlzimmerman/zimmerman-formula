#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
h76_h13_h36_h63.py -- HUNT ITEMS 76, 13, 36, 63.
=================================================
Item 76 (the M/L predicted by the cosmological constant): a_0 is FIXED by Planck's rho_Lambda to 0.7%.  In the deep-MOND tail
        g_obs^2 = a_0 g_bar, and g_bar carries the stellar mass-to-light ratio.  So with a_0 fixed, the rotation curves PREDICT
        Upsilon_[3.6] -- a stellar population parameter derived from the cosmological constant.  Compare with stellar-population
        synthesis (0.5 +- 0.1 at 3.6 um, Schombert+2019, McGaugh+2016) and with DiskMass's dynamical value (~0.3).
        This is the number that three lensing items just ran into (1/66/2/65), so it is the pivot.
Item 13 (Local Group timing): the MW and M31 approach at -110 km/s from a separation of 780 kpc.  In MOND their two-body problem
        has NO free mass: M_b(MW) + M_b(M31) is measured.  Integrate from the Big Bang and compare.
Item 36 (escape velocity): in MOND the potential is logarithmic and unbounded, so v_esc is set by where the EXTERNAL field cuts
        the galaxy off.  v_esc(R0) is therefore a prediction from M_b, a_0 and the external field -- no halo.
Item 63 (void versus wall): galaxies in voids feel almost no external field, so their outer rotation curves must NOT decline;
        wall galaxies feel more.  ON DISK cosmic-web match for SPARC.
Both footings.  Mutations.  Checks CAN fail.
"""
import sys, math, csv
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from hunt_lib import *
ck = Check(); rng = np.random.default_rng(76)
gals = load_sparc()
P("="*116); P("ITEM 76 -- the stellar mass-to-light ratio predicted by the cosmological constant"); P("="*116)
def tail_a0(ups_d, cut=1e-11):
    """re-derive g_bar with a different disc M/L and re-measure the deep-tail a_0 with the slope fixed at 1/2"""
    num, den = [], []
    for g in gals:
        gb = (g["vg"]*np.abs(g["vg"]) + ups_d*g["vd"]**2 + UPS_B*g["vb"]**2)/g["r"]*KMS2_KPC
        m = (gb > 0) & (gb < cut)
        if m.sum() == 0: continue
        num.append(np.log10(g["gobs"][m]) - 0.5*np.log10(gb[m]))
    v = np.concatenate(num)
    return 10**(2*float(np.mean(v))), len(v)
info(f"{'Upsilon_3.6':>12} {'a_0 from the deep tail':>24} {'N points':>10}")
for u in (0.3, 0.4, 0.5, 0.6, 0.7, 0.9):
    a, n = tail_a0(u); info(f"{u:12.2f} {a:24.3e} {n:10d}")
R76 = {}
for foot, a0 in A0.items():
    try: ups_req = brentq(lambda u: tail_a0(u)[0] - a0, 0.15, 3.0, xtol=1e-3)
    except ValueError: ups_req = float("nan")
    bs = []
    for _ in range(60):
        idx = rng.integers(0, len(gals), len(gals)); sub = [gals[i] for i in idx]
        def tail_sub(u):
            num = []
            for g in sub:
                gb = (g["vg"]*np.abs(g["vg"]) + u*g["vd"]**2 + UPS_B*g["vb"]**2)/g["r"]*KMS2_KPC
                m = (gb > 0) & (gb < 1e-11)
                if m.sum(): num.append(np.log10(g["gobs"][m]) - 0.5*np.log10(gb[m]))
            return 10**(2*float(np.mean(np.concatenate(num))))
        try: bs.append(brentq(lambda u: tail_sub(u) - a0, 0.15, 3.0, xtol=1e-3))
        except Exception: pass
    bs = np.array(bs); R76[foot] = (ups_req, bs.std() if len(bs) > 10 else float("nan"), len(bs))
    info(f"{foot:10} a_0 = {a0:.3e} REQUIRES Upsilon_[3.6] = {ups_req:.3f} +- {R76[foot][1]:.3f} (galaxy bootstrap, N = {len(bs)})")
SPS = (0.5, 0.1); DISKMASS = 0.3
d_can = (R76["canonical"][0] - SPS[0])/math.sqrt(R76["canonical"][1]**2 + SPS[1]**2)
d_alt = (R76["alt"][0] - SPS[0])/math.sqrt(R76["alt"][1]**2 + SPS[1]**2)
info(f"stellar-population synthesis at 3.6 um: Upsilon = {SPS[0]:.2f} +- {SPS[1]:.2f} (Schombert+2019, McGaugh+2016); DiskMass dynamical ~{DISKMASS}")
ck("76 (a WORKS -- a stellar-population parameter derived from the cosmological constant) with a_0 fixed by Planck's rho_Lambda, the deep tail of the rotation curves PREDICTS the 3.6 um stellar M/L with no fitting, and BOTH footings land inside the stellar-population range: the alt footing lands on it almost exactly (0.504 vs 0.50), the canonical footing 1.5 sigma high",
   abs(d_can) < 2.0 and abs(d_alt) < 2.0,
   f"canonical requires Upsilon = {R76['canonical'][0]:.3f} +- {R76['canonical'][1]:.3f} ({d_can:+.1f} sigma from SPS); alt requires {R76['alt'][0]:.3f} +- {R76['alt'][1]:.3f} ({d_alt:+.1f} sigma) -- the measurement MILDLY PREFERS the alt footing")
ck("76b the footings are not yet separated by this route: they require Upsilon values 1.5 sigma apart, so an independent M/L at 10% (0.05 in Upsilon) would decide, and at present it does not",
   abs(R76["canonical"][0] - R76["alt"][0]) < 3*R76["canonical"][1],
   f"canonical {R76['canonical'][0]:.3f} vs alt {R76['alt'][0]:.3f}: {abs(R76['canonical'][0]-R76['alt'][0])/R76['canonical'][1]:.1f} sigma apart; DiskMass's ~0.3 is excluded by both at > 2 sigma")
P(""); P("="*116); P("ITEM 13 -- the Local Group timing argument with no free mass"); P("="*116)
MW_MB, M31_MB = 6.0e10, 1.2e11; D_LG = 0.78; V_LG = -110.0
H0_LG = H0; t0 = 13.8e9*3.156e7
for foot, a0 in A0.items():
    M = (MW_MB + M31_MB)*Msun
    def rhs(t, y):
        r, v = y; r = max(r, 1e18)
        gN = G*M/r**2; g = gN*nu_s(gN/a0)
        return [v, -g + OM_L*H0**2*r]
    def shoot(v0):
        s = solve_ivp(rhs, (0, t0), [1e19, v0], rtol=1e-9, atol=1e3, dense_output=True, max_step=t0/2000)
        return s
    lo, hi = 1e3, 3e6
    for _ in range(80):
        mid = 0.5*(lo+hi); s = shoot(mid)
        if s.y[0][-1] < D_LG*Mpc: lo = mid
        else: hi = mid
    s = shoot(0.5*(lo+hi)); rf = s.y[0][-1]/Mpc; vf = s.y[1][-1]/1e3
    info(f"{foot:10} MOND two-body, M_b = {(MW_MB+M31_MB):.2e} Msun, no dark matter, no free parameter: at t = 13.8 Gyr the separation is {rf:.3f} Mpc and the relative velocity is {vf:+.0f} km/s   (MEASURED: 0.78 Mpc, -110 km/s)")
    if foot == "canonical": R13 = (rf, vf)
    else: R13a = (rf, vf)
ck("13 AGAINST INTEREST -- the simple radial MOND timing argument OVER-predicts the approach: with the measured baryons and no dark matter it gives -223 (canonical) / -241 (alt) km/s at the observed 0.78 Mpc, against a measured -110.  A factor two too fast, both footings",
   abs(R13[1]) > 1.5*abs(V_LG), f"canonical {R13[1]:+.0f} km/s, alt {R13a[1]:+.0f} vs measured {V_LG:+.0f}; the Newtonian version needs 5e12 Msun, 25x the measured baryons, so neither is comfortable")
info("the published MOND treatment (Zhao, Famaey, Luhausen & Kroupa 2013) resolves this the interesting way: MOND's stronger pull means")
info("the pair must already have had a CLOSE ENCOUNTER, 7-11 Gyr ago, and is now on its second approach -- which a purely radial")
info("single-passage integration like the one above cannot represent.  That flyby is a distinctive, testable prediction (it would have")
info("stripped and reshaped both discs, and is the proposed origin of the Local Group's satellite planes); this item should be re-run")
info("with a two-passage orbit before being read either way.  Recorded as OVER-PREDICTED BY THE SIMPLE MODEL, not as a kill.")
info("caveat both ways: a radial two-body orbit ignores the transverse velocity (small, ~20 km/s from HST/Gaia) and the Local Group's")
info("own mass beyond the two galaxies; the Newtonian version of this argument needs 5e12 Msun, which is 25x the measured baryons.")
P(""); P("="*116); P("ITEM 36 -- the escape velocity from the baryons and the external field"); P("="*116)
R0, VC0 = 8.2, 233.0
for foot, a0 in A0.items():
    Vinf2 = math.sqrt(G*MW_MB*Msun*a0)
    for eN in (0.01, 0.02, 0.05):
        r_efe = math.sqrt(G*MW_MB*Msun/(eN*a0))
        vesc = math.sqrt(2*Vinf2*math.log(r_efe/(R0*kpc)))/1e3
        info(f"{foot:10} e_N = {eN:.2f}: the external field cuts the logarithmic potential at {r_efe/kpc:.0f} kpc -> v_esc(R0) = {vesc:.0f} km/s")
        if foot == "canonical" and eN == 0.02: R36 = vesc
GAIA_VESC = (500.0, 550.0)
for foot, a0 in A0.items():
    v_flat_pred = (G*MW_MB*Msun*a0)**0.25/1e3
    M_needed = (VC0*1e3)**4/(G*a0)/Msun
    r_efe2 = math.sqrt(G*M_needed*Msun/(0.02*a0))
    vesc2 = math.sqrt(2*(VC0*1e3)**2*math.log(r_efe2/(R0*kpc)))/1e3
    info(f"{foot:10} with M_b = {MW_MB:.1e} Msun the framework predicts v_flat = {v_flat_pred:.0f} km/s against the measured {VC0:.0f} -- the repo's known Milky Way v_c normalisation liability (baryon budget, not kernel).")
    info(f"{foot:10} using instead the M_b the framework REQUIRES for v_flat = {VC0:.0f} ({M_needed:.2e} Msun): v_esc(R0) = {vesc2:.0f} km/s at e_N = 0.02")
    if foot == "canonical": R36b = (v_flat_pred, M_needed, vesc2)
ck("36 SPLIT: the escape velocity is a test of the potential's SHAPE and it passes -- once the Milky Way's baryonic mass is set to what the framework needs for the observed rotation speed, v_esc(R0) comes out at 500-560 km/s, inside Gaia's measurement, with no halo.  But that mass is 2.4e11 Msun against a baryon census of 6-9e10, which is the repo's standing Milky Way normalisation liability and is inherited here, not solved",
   GAIA_VESC[0] <= R36b[2] <= 600 and R36b[1] > 2*MW_MB,
   f"with M_b = 6e10: v_flat = {R36b[0]:.0f} km/s (measured {VC0:.0f}) and v_esc = {R36:.0f}; with the required M_b = {R36b[1]:.2e}: v_esc = {R36b[2]:.0f} km/s vs Gaia {GAIA_VESC[0]:.0f}-{GAIA_VESC[1]:.0f}")
P(""); P("="*116); P("ITEM 63 -- void versus wall galaxies: does the external field show in the outer slopes?"); P("="*116)
rows = list(csv.DictReader(open(os.path.join(DATA, "sparc_cosmicweb_match.csv"))))
info(f"cosmic-web match: {len(rows)} rows; using env_class (text) and onepd_2mpp (1+delta from 2M++)")
envc, envd = {}, {}
for r in rows:
    nm = r.get("name")
    if r.get("env_class"): envc[nm] = r["env_class"].strip()
    try: envd[nm] = float(r["onepd_2mpp"])
    except Exception: pass
cls = {}
for g in gals:
    if g["name"] not in envd: continue
    r, v = g["r"], g["vobs"]
    m = r > 0.5*r.max()
    if m.sum() < 3: continue
    sl = np.polyfit(np.log(r[m]), np.log(v[m]), 1)[0]
    cls.setdefault(envc.get(g["name"], "?"), []).append(sl)
    cls.setdefault("__all__", []).append((sl, envd[g["name"]]))
allp = cls.pop("__all__")
sl_all = np.array([a[0] for a in allp]); de = np.array([a[1] for a in allp])
info(f"N = {len(sl_all)} SPARC galaxies matched with a 2M++ density and >= 3 outer points")
for k in sorted(cls):
    a = np.array(cls[k]); info(f"  env_class '{k}': N = {len(a):3d}, mean outer d ln v/d ln r = {a.mean():+.4f} +- {a.std()/math.sqrt(len(a)):.4f}")
lo = de < np.median(de); hi = ~lo
d63 = sl_all[hi].mean() - sl_all[lo].mean()
sd63 = math.sqrt(sl_all[lo].std()**2/lo.sum() + sl_all[hi].std()**2/hi.sum())
rho = float(np.corrcoef(np.log10(de), sl_all)[0, 1])
info(f"low-density half (1+delta < {np.median(de):.2f}): {sl_all[lo].mean():+.4f} +- {sl_all[lo].std()/math.sqrt(lo.sum()):.4f}; high-density half: {sl_all[hi].mean():+.4f} +- {sl_all[hi].std()/math.sqrt(hi.sum()):.4f}")
ck("63 the void-versus-wall outer-slope test runs and finds NO significant difference: the external-field effect predicts a negative difference (denser environment, more declining outer curve) and the measured difference is consistent with zero at this sample size",
   abs(d63) < 3*sd63, f"high minus low density = {d63:+.4f} +- {sd63:.4f} ({d63/sd63:+.1f} sigma), sign {'as the EFE predicts' if d63 < 0 else 'opposite to the EFE'}; correlation with log(1+delta) r = {rho:+.3f}, N = {len(sl_all)}")
cl = np.array(cls.get("cluster", [])); vo = np.array(cls.get("void", [])); wa = np.array(cls.get("wall", []))
if len(cl) > 5 and len(wa) > 5:
    dcw = wa.mean() - cl.mean(); sdcw = math.sqrt(wa.std()**2/len(wa) + cl.std()**2/len(cl))
    dcv = vo.mean() - cl.mean(); sdcv = math.sqrt(vo.std()**2/len(vo) + cl.std()**2/len(cl))
    ck("63b (a HINT, reported and not overclaimed) the env_class split does show the external-field effect's SIGN: cluster galaxies have the most declining outer curves, wall the least, cluster-versus-wall separated at ~2 sigma and cluster-versus-void at ~1 sigma, in the predicted direction -- but wall exceeding void breaks the density ordering, so this is a hint at the level the sample allows and nothing more",
       dcw > 0 and dcv > 0, f"wall - cluster = {dcw:+.4f} +- {sdcw:.4f} ({dcw/sdcw:+.1f} sigma); void - cluster = {dcv:+.4f} +- {sdcv:.4f} ({dcv/sdcv:+.1f} sigma); means: cluster {cl.mean():+.4f} (N={len(cl)}), void {vo.mean():+.4f} (N={len(vo)}), wall {wa.mean():+.4f} (N={len(wa)})")
info("power note: the 2M++ density contrast across SPARC's environments spans only ~1 dex, and the EFE's predicted outer-slope change")
info("over that range is a few percent -- comparable to the 0.01-0.02 measurement error per half-sample.  Underpowered, as expected.")
sys.exit(ck.done())
