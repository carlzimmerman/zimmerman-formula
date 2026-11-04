"""FN3 budget (criteria s6), written before Stage 1: levers and the common-mode error per z-third and footing.

For each third, a synthetic galaxy at the third's median z, SED M* (native D_L), R_e, Sersic n, sigma_0 and SFR carries
the law at the band (Delta = 0, Sigma_HI 5). Its v_perp at 0.5-2.5 R_e is refitted for log M* (Sigma_HI held) with
a0 x 10^0.05 (L_band = dDelta/dlog a0) and with mu_mol x 10^0.1 (L_H2 = dDelta/dlog mu). Then
sigma_cm = sqrt(0.20^2 + (L_H2 x 0.10)^2 + (L_band x sigma_band)^2), sigma_band from CFG689 at the nearest node.
Slope budget: sigma_s,sys = sqrt(0.10^2 + (L_H2 x e_slope)^2), e_slope the error of dlog mu/dz from the relation's
B (-3.33 +- 0.2) and F (0.65 +- 0.05), at the sample's median z. kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os

import numpy as np
from scipy import optimize

import fn3_common as C
import fn3_cube as F


def vperp(mass, R, Re, n, logM, sig0, sighi=5.0):
    vc2 = mass.vc2(R, Re, n, logM, sighi)
    vp, _ = F.kinematics(vc2, R, Re, n, sig0, 1.0)
    return vp


def refit(target, R, Re, n, sig0, mass, logM0):
    f = lambda lm: float(np.sum((vperp(mass, R, Re, n, lm, sig0) - target) ** 2))
    r = optimize.minimize_scalar(f, bounds=(logM0 - 2, logM0 + 2), method="bounded", options=dict(xatol=1e-7))
    return r.x


def dlogmu_dz_err(z):
    x = math.log10(1 + z) - 0.65
    dB = -2 * x / ((1 + z) * math.log(10))
    dF = 2 * (-3.33) / ((1 + z) * math.log(10))
    return math.hypot(dB * 0.2, dF * 0.05)


def main():
    N = C.Native()
    P15 = C.planck15()
    phot, _ = C.load_catalogue()
    s = json.load(open(os.path.join(C.HERE, "fn3_sample.json")))
    out = dict(criteria="c6640225c2", amendment="A1", sed_scale=0.20, sed_slope=0.10, mu_scale=0.10, thirds={})
    lines = ["FN3 budget, frozen before Stage 1 (criteria s6)"]
    zall = []
    for t in ("0", "1", "2"):
        gids = s["thirds"][t]
        z, lm, Re, nn, s0, lsfr = [], [], [], [], [], []
        for gid in gids:
            g = C.load_galaxy(gid)
            ph = phot[gid]
            zz = ph["z"]
            dl2 = (float(N.DL(zz)) / P15.luminosity_distance(zz).value) ** 2
            z.append(zz)
            zall.append(zz)
            lm.append(ph["Mstar"] + math.log10(dl2))
            Re.append(g["par"]["radius"] * 0.2 * N.kpc_per_arcsec(zz))
            nn.append(g["par"]["sersic_n"])
            s0.append(g["par"]["velocity_dispersion"])
            lsfr.append(math.log10(ph["SFR"]) + math.log10(dl2) if ph.get("SFR", 0) > 0 else float("nan"))
        zm, lmm, Rem, nm, s0m = (float(np.median(a)) for a in (z, lm, Re, nn, s0))
        lsm = float(np.nanmedian(lsfr))
        mu = C.mu_mol_t20(zm, lmm, lsm, N.age_gyr(zm), use_dms=True)
        R = np.linspace(0.5, 2.5, 21) * Rem
        sb = N.band_sigma_dex(zm)
        rec = dict(N=len(gids), z_med=zm, logM_sed_med=lmm, Re_kpc_med=Rem, n_med=nm, sig0_med=s0m, logSFR_med=lsm,
                   mu_mol=mu, sigma_band_dex=sb, footings={})
        for foot, af in C.A_FOOT.items():
            a0 = af * float(N.band_ratio(zm))
            base = F.LawMass(mu * 10 ** lmm, a0)
            tgt = vperp(base, R, Rem, nm, lmm, s0m)
            l0 = refit(tgt, R, Rem, nm, s0m, base, lmm)
            la = refit(tgt, R, Rem, nm, s0m, F.LawMass(mu * 10 ** lmm, a0 * 10 ** 0.05), lmm)
            lh = refit(tgt, R, Rem, nm, s0m, F.LawMass(mu * 10 ** 0.1 * 10 ** lmm, a0), lmm)
            Lb, Lh = (la - l0) / 0.05, (lh - l0) / 0.1
            scm = math.sqrt(0.20 ** 2 + (Lh * 0.10) ** 2 + (Lb * sb) ** 2)
            gN = float(np.median((F.disc_v2(R, 10 ** lmm * (1 + mu), Rem, nm) + C.sgas_vc2(R, 5.0, math.pi)) / R)) * C.ACC_UNIT
            rec["footings"][foot] = dict(a0=a0, recovered_identity=float(l0 - lmm), L_band=Lb, L_H2=Lh, sigma_cm=scm,
                                         median_gN_over_a0=gN / a0)
            lines.append(f"third {t} {foot:9s}: z {zm:.3f} logM {lmm:.2f} Re {Rem:.2f} kpc n {nm:.2f} sig0 {s0m:.1f} mu {mu:.3f} | "
                         f"identity {l0 - lmm:+.1e} L_band {Lb:+.3f} L_H2 {Lh:+.3f} sigma_band {sb:.3f} -> sigma_cm {scm:.4f} "
                         f"(median gN/a0 {gN / a0:.2f})")
        out["thirds"][t] = rec
    zmed = float(np.median(zall))
    e = dlogmu_dz_err(zmed)
    for foot in C.A_FOOT:
        Lh = float(np.median([out["thirds"][t]["footings"][foot]["L_H2"] for t in "012"]))
        out.setdefault("slope", {})[foot] = dict(z_med=zmed, dlogmu_dz_err=e, L_H2_med=Lh,
                                                  sigma_s_sys=math.hypot(0.10, Lh * e))
        lines.append(f"slope budget {foot}: dlog mu/dz error {e:.4f} at z {zmed:.3f}, L_H2 {Lh:+.3f} -> sigma_s,sys {math.hypot(0.10, Lh * e):.4f} dex per unit z")
    lines.append("kappa = 1/2 FITTED; not theory closed.")
    print("\n".join(lines))
    open(os.path.join(C.HERE, "fn3_budget.out"), "w").write("\n".join(lines) + "\n")
    json.dump(out, open(os.path.join(C.HERE, "budget.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
