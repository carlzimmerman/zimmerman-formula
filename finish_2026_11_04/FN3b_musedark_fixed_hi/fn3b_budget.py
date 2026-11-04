"""FN3b budget (criteria s2), before any data: FN3's levers recomputed with Sigma_HI fixed at 6.0, plus L_HI.

Per z-third and footing, a synthetic galaxy at the third's medians carries the law at the band with Sigma_HI 6.0; its
v_perp at 0.5-2.5 R_e is refitted for log M* with a0 x 10^0.05 (L_band), mu x 10^0.1 (L_H2) and Sigma_HI x 10^0.1
(L_HI). sigma_cm = sqrt(0.20^2 + (L_H2 0.10)^2 + (L_band sigma_band)^2 + (L_HI 0.25)^2); slope sys adds (L_HI 0.10).
kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import sys

import numpy as np
from scipy import optimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "FN3_musedark_law_refit"))
import fn3_common as C  # noqa: E402
import fn3_cube as F  # noqa: E402
from fn3_budget import dlogmu_dz_err  # noqa: E402

SIG_HI = 6.0


def vperp(mass, R, Re, n, logM, sig0, sighi):
    vp, _ = F.kinematics(mass.vc2(R, Re, n, logM, sighi), R, Re, n, sig0, 1.0)
    return vp


def refit(tgt, R, Re, n, s0, mass, lm0, sighi):
    f = lambda lm: float(np.sum((vperp(mass, R, Re, n, lm, s0, sighi) - tgt) ** 2))
    return optimize.minimize_scalar(f, bounds=(lm0 - 2, lm0 + 2), method="bounded", options=dict(xatol=1e-7)).x


def main():
    N, P15 = C.Native(), C.planck15()
    phot, _ = C.load_catalogue()
    s = json.load(open(os.path.join(HERE, "..", "FN3_musedark_law_refit", "fn3_sample.json")))
    out = dict(criteria="FN3b FROZEN_CRITERIA.md", sigma_hi=SIG_HI, sed_scale=0.20, mu_scale=0.10, hi_scale=0.25, thirds={})
    lines = ["FN3b budget, frozen before Stage 1 (criteria s2); Sigma_HI fixed at 6.0 Msun/pc^2"]
    zall = []
    for t in ("0", "1", "2"):
        z, lm, Re, nn, s0, ls = [], [], [], [], [], []
        for gid in s["thirds"][t]:
            g, ph = C.load_galaxy(gid), phot[gid]
            zz = ph["z"]
            dl2 = (float(N.DL(zz)) / P15.luminosity_distance(zz).value) ** 2
            z.append(zz); zall.append(zz)
            lm.append(ph["Mstar"] + math.log10(dl2))
            Re.append(g["par"]["radius"] * 0.2 * N.kpc_per_arcsec(zz))
            nn.append(g["par"]["sersic_n"]); s0.append(g["par"]["velocity_dispersion"])
            ls.append(math.log10(ph["SFR"]) + math.log10(dl2) if ph.get("SFR", 0) > 0 else float("nan"))
        zm, lmm, Rem, nm, s0m = (float(np.median(a)) for a in (z, lm, Re, nn, s0))
        mu = C.mu_mol_t20(zm, lmm, float(np.nanmedian(ls)), N.age_gyr(zm), use_dms=True)
        R = np.linspace(0.5, 2.5, 21) * Rem
        sb = N.band_sigma_dex(zm)
        rec = dict(N=len(z), z_med=zm, logM_sed_med=lmm, Re_kpc_med=Rem, n_med=nm, sig0_med=s0m, mu_mol=mu,
                   sigma_band_dex=sb, footings={})
        for foot, af in C.A_FOOT.items():
            a0 = af * float(N.band_ratio(zm))
            base = F.LawMass(mu * 10 ** lmm, a0)
            tgt = vperp(base, R, Rem, nm, lmm, s0m, SIG_HI)
            l0 = refit(tgt, R, Rem, nm, s0m, base, lmm, SIG_HI)
            la = refit(tgt, R, Rem, nm, s0m, F.LawMass(mu * 10 ** lmm, a0 * 10 ** 0.05), lmm, SIG_HI)
            lh = refit(tgt, R, Rem, nm, s0m, F.LawMass(mu * 10 ** 0.1 * 10 ** lmm, a0), lmm, SIG_HI)
            lg = refit(tgt, R, Rem, nm, s0m, base, lmm, SIG_HI * 10 ** 0.1)
            Lb, Lh, Lg = (la - l0) / 0.05, (lh - l0) / 0.1, (lg - l0) / 0.1
            scm = math.sqrt(0.20 ** 2 + (Lh * 0.10) ** 2 + (Lb * sb) ** 2 + (Lg * 0.25) ** 2)
            rec["footings"][foot] = dict(a0=a0, identity=float(l0 - lmm), L_band=Lb, L_H2=Lh, L_HI=Lg, sigma_cm=scm)
            lines.append(f"third {t} {foot:9s}: z {zm:.3f} logM {lmm:.2f} | L_band {Lb:+.3f} L_H2 {Lh:+.3f} L_HI {Lg:+.3f} "
                         f"sigma_band {sb:.3f} -> sigma_cm {scm:.4f}")
        out["thirds"][t] = rec
    zmed = float(np.median(zall))
    e = dlogmu_dz_err(zmed)
    for foot in C.A_FOOT:
        Lh = float(np.median([out["thirds"][t]["footings"][foot]["L_H2"] for t in "012"]))
        Lg = float(np.median([out["thirds"][t]["footings"][foot]["L_HI"] for t in "012"]))
        ss = math.sqrt(0.10 ** 2 + (Lh * e) ** 2 + (Lg * 0.10) ** 2)
        out.setdefault("slope", {})[foot] = dict(z_med=zmed, L_H2_med=Lh, L_HI_med=Lg, sigma_s_sys=ss)
        lines.append(f"slope budget {foot}: L_H2 {Lh:+.3f}, L_HI {Lg:+.3f} -> sigma_s,sys {ss:.4f} dex per unit z")
    lines.append("kappa = 1/2 FITTED; not theory closed.")
    print("\n".join(lines))
    open(os.path.join(HERE, "fn3b_budget.out"), "w").write("\n".join(lines) + "\n")
    json.dump(out, open(os.path.join(HERE, "budget_fn3b.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
