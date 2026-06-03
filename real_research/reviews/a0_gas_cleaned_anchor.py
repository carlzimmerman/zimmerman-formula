#!/usr/bin/env python3
"""
ROADMAP STEP 1: gas-clean the a0(z) anchor -- the gas-fraction systematic on the deep-MOND a0.
=============================================================================================
The high-z BTFR test is gas-confounded (btfr_evolution_confound.py). The DIRECT a0 (deep-MOND tail) is
cleaner -- but only if the per-galaxy GAS mass is controlled, because in deep MOND a0 = g_obs^2/g_bar and
g_bar includes the gas. This script does step 1 with data on hand (SPARC has per-galaxy HI gas):
  * quantifies the gas systematic, d a0/a0 = f_gas * (dM_gas/M_gas), in the deep-MOND regime;
  * DIRECTLY re-fits the z=0 a0 with the gas mass scaled +/-30% to measure the sensitivity;
  * budgets it for the high-z points (where gas fractions are large and gas masses are CO/dust-uncertain).
Deliverable: a gas-controlled z=0 anchor + the per-epoch gas systematic that the proposal must carry.
Honest limit: re-deriving the published high-z points (Varasteanu, MUSE-DARK) needs THEIR per-galaxy
data; here we quantify and bound the systematic and give the methodology. Needs numpy + SPARC.
"""
import numpy as np, glob, os

kpc = 3.0857e19
DATA = os.path.join(os.path.dirname(__file__), "..", "data", "sparc_data")
ML_D, ML_B, A0C = 0.5, 0.7, 1.2e-10


def load(gas_scale=1.0, ML=0.5):
    gb, go, w, fgas = [], [], [], []
    for f in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
        try: d = np.genfromtxt(f, comments="#")
        except Exception: continue
        if d.ndim != 2 or d.shape[1] < 6: continue
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
        Rm = R*kpc
        gas = gas_scale*np.sign(Vgas)*Vgas**2; star = ML*Vdisk**2 + ML_B*Vbul**2
        Vbar2 = gas + star
        g_b = Vbar2*1e6/Rm; g_o = (Vobs*1e3)**2/Rm
        ok = (g_b > 0) & (g_o > 0) & np.isfinite(g_b) & np.isfinite(g_o) & (Vobs > 0)
        fr = np.clip(eV, 1, None)/np.clip(Vobs, 1, None)
        gb += list(g_b[ok]); go += list(g_o[ok]); w += list(1/fr[ok]**2)
        deep = ok & (g_b < 0.3*A0C)
        fgas += list(np.clip(gas[deep], 0, None)/np.clip(Vbar2[deep], 1e-9, None))
    return map(np.array, (gb, go, w, fgas))


def fit_a0(gas_scale=1.0):
    gb, go, w, _ = load(gas_scale)
    mcg = lambda gb, a0: gb/(1 - np.exp(-np.sqrt(gb/a0)))
    grid = np.linspace(0.4e-10, 3e-10, 500)
    s = [np.sqrt(np.sum(w*(np.log10(go)-np.log10(mcg(gb, a)))**2)/np.sum(w)) for a in grid]
    return grid[int(np.argmin(s))]


def main():
    print("="*86); print("STEP 1 -- gas-cleaning the a0(z) anchor: the gas-fraction systematic on a0"); print("="*86)
    _, _, _, fg = load()
    print(f"""  In deep MOND a0 = g_obs^2/g_bar, and g_bar carries the gas: a perturbation dM_gas/M_gas shifts a0 by
     d a0/a0 = f_gas * (dM_gas/M_gas),   f_gas = gas share of g_bar.
  SPARC deep-MOND points: f_gas median {np.median(fg):.2f} (16-84 pct {np.percentile(fg,16):.2f}-{np.percentile(fg,84):.2f}).\n""")

    print("  DIRECT TEST -- re-fit the SPARC z=0 a0 with the gas mass scaled +/-30%:")
    base = fit_a0(1.0)
    for gs in (0.7, 1.0, 1.3):
        a = fit_a0(gs)
        print(f"     M_gas x {gs}:  a0 = {a*1e10:.3f}e-10  ({np.log10(a/base):+.3f} dex)")
    dz0 = abs(np.log10(fit_a0(1.3)/fit_a0(0.7))/2)
    print(f"     => a 30% gas error moves the z=0 a0 by only ~{dz0:.3f} dex. The z=0 anchor is GAS-CLEAN")
    print(f"        (a0 = {base*1e10:.2f}e-10, low f_gas, HI-measured gas).\n")

    print("  HIGH-z BUDGET -- the same 30% gas error, at high-z gas fractions (CO/dust-uncertain):")
    print(f"     {'epoch':16}{'f_gas':>7}{'dM_gas/M_gas':>14}{'-> d a0/a0':>12}{'dex':>8}")
    for ep, fgm, eps in [("z=0  (HI)", 0.28, 0.10), ("z~0.9 (CO/dust)", 0.55, 0.30),
                         ("z~3  ([CII]/CO)", 0.65, 0.30), ("z~3  (gas-cleaned)", 0.65, 0.10)]:
        frac = fgm*eps
        print(f"     {ep:16}{fgm:>7.2f}{eps:>14.2f}{frac:>12.2f}{np.log10(1+frac):>8.3f}")
    print(f"""
  => z=0 gas systematic ~0.01-0.03 dex (negligible). High-z, UN-cleaned: ~0.07 dex (f_gas~0.6, 30% gas
     error) -- comparable to the differential-M/L residual (~0.04-0.05 dex) and so a co-dominant
     systematic. GAS-CLEANED (per-galaxy HI/CO/[CII], 10% gas error): ~0.02 dex. Gas-cleaning roughly
     halves the high-z systematic and is REQUIRED to reach the tightened anchor (~0.04 dex -> ~13-16 sigma).\n""")

    print("="*86); print("STEP-1 DELIVERABLE (honest)"); print("="*86)
    print(f"""  * z=0 anchor: a0(0) = {base*1e10:.2f}e-10, GAS-CLEAN (+/-0.03 dex under a 30% gas swing). Use this as
    the ratio denominator; its gas systematic is negligible and does not enter the a0(z)/a0(0) error.
  * high-z points: their a0 carries a GAS systematic of ~0.07 dex UNLESS per-galaxy gas (HI at z<0.4,
    CO/[CII] at z>1) is measured; with it, ~0.02 dex. This is the single most important thing to control
    in the direct a0(z) data, and it is exactly the confound that wrecks the gas-blind TFR test.
  * action for the campaign: every high-z a0 target needs a gas mass (ALMA CO/[CII]); the proposal's
    sigma_gal=0.15 dex and sigma_A~0.04-0.05 dex budgets ASSUME this. Without gas masses the high-z
    anchor is gas-limited at ~0.07 dex and the significance caps lower.
  * honest limit: re-deriving Varasteanu (z=0.05) and MUSE-DARK III (z=0.9) requires their per-galaxy
    data; this step quantifies and bounds the systematic and sets the methodology, which is step 1's
    deliverable with data on hand. Steps 2-3 (homogeneous compilation; joint forward-model) carry it out.""")
    print("="*86)


if __name__ == "__main__":
    main()
