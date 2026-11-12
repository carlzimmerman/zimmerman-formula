"""EUC5R instrument checks on the model machinery: J1, J2, K-proj, kernel-vs-direct, J3, J4, K-sanity.
Run from the repo root:  python closure_2026_11_12/EUC5R_blind_dynamical_boost_regrade/euc5r_checks.py
Exit 1 if any gate (J1, J2, K-proj, kernel, J3, K-sanity band) fails."""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from euc5r_model import (G, ARCSEC, A0_ALT, A0_CANON, AUGER_COSMO, JeansKernel, SersicLens, M2D_law,
                         aperture_weight, b_lens, a0_units)

HERE = os.path.dirname(os.path.abspath(__file__))
SLACS = "real_research/data/slacs_auger2009_lenses.tsv"
OUT = {}
FAILS = []


def P(*a):
    print(*a, flush=True)


def ck(name, ok, val):
    OUT[name] = dict(value=val, ok=bool(ok))
    P(f"  {name:28s} {'PASS' if ok else 'FAIL'}  {val}")
    if not ok:
        FAILS.append(name)


def load_slacs():
    lines = open(SLACS, encoding="latin-1").read().splitlines()
    hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
    hdr = lines[hi].split("\t")
    col = {c: i for i, c in enumerate(hdr)}
    out = []
    for l in lines[hi + 3:]:
        if not l.strip() or l.startswith("#"):
            continue
        r = l.split("\t")
        if len(r) < len(hdr):
            continue

        def f(k):
            try:
                return float(r[col[k]].strip())
            except ValueError:
                return float("nan")
        out.append(dict(name=r[col["SDSS"]].strip(), zl=f("zlens"), zs=f("zsrc"), sig=f("sigma"), esig=f("e_sigma"),
                        RE=f("RE"), ReV=f("Re(V)"), logMs=f("logMs")))
    return out


def main():
    P("EUC5R checks")
    # ---------------- J1 Plummer, isotropic, Newtonian
    M, a = 1e11, 1.0
    jk = JeansKernel(lambda r: (1 + r * r / a / a) ** -2.5, 0.0, 1e-4, 1e4, N=1600)
    g = G * M * jk.r / (jk.r ** 2 + a * a) ** 1.5
    R = np.array([0.5, 2.0]) * a
    Sig, SS = jk.moments_point(R, g)
    s2 = SS / Sig
    ex = 3 * math.pi / 64 * G * M / a / np.sqrt(1 + R * R / a / a)
    err = np.abs(s2 / ex - 1)
    ck("J1_plummer", np.all(err < 0.01), [float(x) for x in err])
    # ---------------- J2 nu ~ r^-3, flat curve, beta 0.3
    vc = 200.0
    jk2 = JeansKernel(lambda r: r ** -3.0, 0.3, 1e-6, 1e7, N=2000)
    g2 = vc * vc / jk2.r
    Sig, SS = jk2.moments_point(np.array([1.0]), g2)
    e2 = abs(SS[0] / Sig[0] / (vc * vc / 3) - 1)
    ck("J2_powerlaw_beta0.3", e2 < 0.01, float(e2))
    # ---------------- K-proj: point mass, aperture weight of a central point
    a0n = 1e-30 * 1e8
    Mp = 1e11
    m2 = M2D_law(5.0, Mp, 1.0, 4.0, a0n, "N", m3=lambda r: np.ones_like(r))
    ck("Kproj_pointmass", abs(m2 / Mp - 1) < 1e-6, float(m2 / Mp - 1))
    Rap, s = 3.0, 2.0
    w0 = aperture_weight(np.array([1e-9]), Rap, s)[0]
    ck("Kproj_aperture_centre", abs(w0 - (1 - math.exp(-Rap * Rap / (2 * s * s)))) < 1e-4,
       float(w0 - (1 - math.exp(-Rap * Rap / (2 * s * s)))))
    # ---------------- kernel vs direct (aperture integral done by brute force on point moments)
    L = SersicLens(2.5e11, 6.0, 5.0, beta=0.2)
    a0u = a0_units(A0_ALT)
    Rap, s = 4.0, 3.0
    sk = L.sigma_ap(1.0, a0u, "S", Rap, s)
    gg = L.g_grid(1.0, a0u, "S")
    Rg = np.logspace(-3.5, math.log10(Rap + 8 * s), 1500)
    Sig, SS = L.jk.moments_point(Rg, gg)
    W = aperture_weight(Rg, Rap, s)
    num = np.trapz(W * SS * Rg * Rg, np.log(Rg))
    den = np.trapz(W * Sig * Rg * Rg, np.log(Rg))
    sd = math.sqrt(num / den)
    ck("Kernel_vs_direct", abs(sk / sd - 1) < 2e-3, float(sk / sd - 1))
    # Newtonian scaling: sigma^2 proportional to B
    s1 = L.sigma_ap(1.0, 1e-30, "N", Rap, s)
    s4 = L.sigma_ap(4.0, 1e-30, "N", Rap, s)
    ck("Newton_sigma2_propto_B", abs((s4 / s1) ** 2 / 4 - 1) < 1e-9, float((s4 / s1) ** 2 / 4 - 1))
    # ---------------- J3 / J4 / K-sanity on SLACS
    rows = [d for d in load_slacs() if all(np.isfinite([d["zl"], d["zs"], d["sig"], d["RE"], d["ReV"]]))
            and d["RE"] > 0 and d["ReV"] > 0]
    ratios, j4, ksan, per = [], [], [], []
    for d in rows:
        DA = AUGER_COSMO.DA(d["zl"])
        Re = d["ReV"] * ARCSEC * DA
        Rap = 1.5 * ARCSEC * DA
        s = 1.5 / 2.354820045 * ARCSEC * DA
        sc = AUGER_COSMO.sigcr(d["zl"], d["zs"])
        Mref = 1e11
        lens = SersicLens(Mref, Re, 4.0, beta=0.0)
        bl = b_lens(Mref, Re, 4.0, d["RE"], sc, a0u, "S")
        sp = lens.sigma_ap(10 ** bl, a0u, "S", Rap, s)
        ratios.append(sp / d["sig"])
        bd, flag = lens.b_dyn(d["sig"], a0u, "S", Rap, s, lo=-3, hi=3)
        j4.append(bd - bl)
        row = dict(name=d["name"], pred_over_meas=sp / d["sig"], bdyn_minus_blens=bd - bl)
        if np.isfinite(d["logMs"]):
            sM = lens.sigma_ap(10 ** d["logMs"] / Mref, a0u, "S", Rap, s)
            ksan.append(sM / d["sig"])
            row["salp_pred_over_meas"] = sM / d["sig"]
        per.append(row)
    medr = float(np.median(ratios))
    P(f"  SLACS lenses used in J3: {len(rows)}")
    ck("J3_slacs_median_ratio", abs(medr - 0.977) <= 0.05, medr)
    OUT["J4_median_bdyn_minus_blens"] = float(np.median(j4))
    P(f"  J4 median b_dyn - b_lens(true z_s) = {np.median(j4):+.4f} dex  (N={len(j4)})")
    mk = float(np.median(ksan))
    ck("Ksanity_salpeter_pred", 0.85 <= mk <= 1.00, mk)
    OUT["J3_N"] = len(rows)
    OUT["Ksanity_N"] = len(ksan)
    OUT["slacs_per_lens"] = per
    json.dump(OUT, open(os.path.join(HERE, "euc5r_checks.json"), "w"), indent=1)
    P("FAILS:", FAILS)
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
