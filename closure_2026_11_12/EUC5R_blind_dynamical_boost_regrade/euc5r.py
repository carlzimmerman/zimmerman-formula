"""EUC5R graded reading under A1 (DESI dispersions), both footings, law S headline, law B reported.
Run from the repo root after euc5r_checks.py and euc5r_fit.py (f1, desi, slacs).
EUC5R_MUTATE=newton: a0 -> 1e-30 on both footings; b_med must rise; exits 1; separate outputs."""
import json, math, os, sys
import numpy as np
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from euc5r_model import (ARCSEC, A0_ALT, A0_CANON, ECLIPSE_COSMO as CO, SersicLens, b_lens, a0_units)
import euc5r_data as D
from euc5r_fit import chosen_desi

MUT = os.environ.get("EUC5R_MUTATE", "")
TAG = "_MUTATE_newton" if MUT == "newton" else ""
SEED = 20261112
FOOT = {"canonical": A0_CANON, "alt": A0_ALT}
if MUT == "newton":
    FOOT = {k: 1e-30 for k in FOOT}
BETAS = (-0.2, 0.0, 0.2)
SEEING = (0.9, 1.1, 1.3)
RAP_ARC = 0.75
LINES = []


def P(s=""):
    print(s, flush=True)
    LINES.append(s)


def boot_median(x, n=2000, seed=SEED):
    x = np.asarray(x, float)
    rng = np.random.default_rng(seed)
    bs = np.median(x[rng.integers(0, len(x), (n, len(x)))], axis=1)
    return float(np.median(x)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def word(lo, hi):
    if hi <= 0.15:
        return "DYNAMICAL GATE HOLDS"
    if lo >= 0.25:
        return "DYNAMICAL GATE FAILS"
    return "NO VERDICT"


def main():
    checks = json.load(open(f"{HERE}/euc5r_checks.json"))
    f1 = json.load(open(f"{HERE}/euc5r_f1.json"))
    scale = json.load(open(f"{HERE}/euc5r_slacs_scale.json"))
    j_ok = all(checks[k]["ok"] for k in ("J1_plummer", "J2_powerlaw_beta0.3", "J3_slacs_median_ratio"))
    f1_ok = bool(f1["F1_gate_pass"])
    P(f"EUC5R graded reading under A1  {'[MUTATE newton]' if MUT else ''}")
    P(f"J1-J3 {'PASS' if j_ok else 'FAIL'}; F1 {'PASS' if f1_ok else 'FAIL'}; F2 NOT RUN (blind; READING 2.2)")
    for k, v in f1["runs"].items():
        if k.startswith("gate"):
            P(f"  F1 {k}: median/sigma_in = {v['ratio_to_sigma_in']:.4f}")
    cat = D.samples().set_index("unique_identifier")
    df = pd.read_csv(f"{HERE}/euc5r_desi_fits.csv")
    ch = chosen_desi(df)
    ch["quality"] = ch.quality.astype(bool)
    P(f"A1.1 spectra of S lenses: {len(df)} spectra, {ch.unique_identifier.nunique()} lenses "
      f"({int(ch.in_P.sum())} in P); kinds {df.kind.value_counts().to_dict()}")
    P(f"quality-passing chosen spectra: S {int(ch.quality.sum())}, P {int((ch.quality & ch.in_P).sum())}")
    # error-definition sensitivity (propagated vs unpropagated error in the err/sigma cut)
    alt_q = ch.apply(lambda r: (r.status == "ok") and 70 <= r.sigma <= 500 and r.err_fit / r.sigma <= 0.25
                     and abs(r.V) <= 300 and r.npix >= 800, axis=1)
    P(f"  lenses whose quality changes if err_fit (unpropagated) is used: {int((alt_q != ch.quality).sum())}")
    # F3 repeatability
    P("F3 repeat spectra (sigma, err):")
    for u, g in df.groupby("unique_identifier"):
        if len(g) > 1:
            P("  " + u + ": " + "; ".join(f"{'prim' if r.specprimary else 'sec '} {r.sigma:.1f}+-{r.err:.1f} S/N {r.snr_pix:.2f}"
                                          for _, r in g.iterrows()))
    g = ch[ch.quality].copy()
    rows = []
    for _, r in g.iterrows():
        c = cat.loc[r.unique_identifier]
        z = float(r.z_def)
        zp = float(c.eclipse_median_phz)
        Ms = 10 ** float(c.eclipse_log_survived_mass_med) * (CO.DL(z) / CO.DL(zp)) ** 2
        DA = CO.DA(z)
        Re = float(c.eclipse_effective_radius) * ARCSEC * DA
        RE = float(c.eclipse_effective_einstein_radius) * ARCSEC * DA
        n = float(c.eclipse_sersic_index)
        Rap = RAP_ARC * ARCSEC * DA
        lenses = {b: SersicLens(Ms, Re, n, beta=b) for b in BETAS}
        row = dict(uid=r.unique_identifier, in_P=bool(r.in_P), z=z, zphot=zp,
                   in_window=bool(c.eclipse_min70_phz - 0.1 <= z <= c.eclipse_max70_phz + 0.1),
                   logMs=math.log10(Ms), Re_kpc=Re, RE_kpc=RE, n=n, thetaE=float(c.eclipse_effective_einstein_radius),
                   sigma=float(r.sigma), err=float(r.err))
        sc_inf = CO.sigcr(z, 1100.0)
        for fn, a0 in FOOT.items():
            a0u = a0_units(a0)
            for law in ("S", "B"):
                for b in BETAS:
                    for fw in SEEING:
                        if law == "B" and not (b == 0.0 and fw == 1.1):
                            continue
                        s = fw / 2.354820045 * ARCSEC * DA
                        bd, fl = lenses[b].b_dyn(r.sigma, a0u, law, Rap, s)
                        row[f"b_{fn}_{law}_{b:+.1f}_{fw}"] = bd
                        row[f"edge_{fn}_{law}_{b:+.1f}_{fw}"] = fl
                # READING R: sigma / s at s, lo, hi (law S, beta 0, 1.1")
                if law == "S":
                    s11 = 1.1 / 2.354820045 * ARCSEC * DA
                    for lab in ("s", "lo", "hi"):
                        sv = scale["degraded"][lab]
                        row[f"bR_{fn}_{lab}"] = lenses[0.0].b_dyn(r.sigma / sv, a0u, "S", Rap, s11)[0]
                binf = b_lens(Ms, Re, n, RE, sc_inf, a0u, law)
                row[f"binf_{fn}_{law}"] = binf
            # conditional source redshift (law S, beta 0, 1.1"): b_lens(z_s) = b_dyn
            bd = row[f"b_{fn}_S_+0.0_1.1"]
            a0u = a0_units(a0)
            if bd < row[f"binf_{fn}_S"]:
                row[f"zs_cond_{fn}"] = float("nan")
            else:
                f = lambda lx: b_lens(Ms, Re, n, RE, CO.sigcr(z, z + math.exp(lx)), a0u, "S") - bd
                lo, hi = math.log(1e-3), math.log(1100.0 - z)
                if f(lo) < 0:
                    row[f"zs_cond_{fn}"] = z + 1e-3
                else:
                    from scipy.optimize import brentq
                    row[f"zs_cond_{fn}"] = z + math.exp(brentq(f, lo, hi, xtol=1e-6))
        rows.append(row)
    T = pd.DataFrame(rows)
    T.to_csv(f"{HERE}/euc5r_per_lens{TAG}.csv", index=False, float_format="%.5f")
    res = dict(F1_pass=f1_ok, J_pass=j_ok, F2="not run (blind)", footings={})
    for samp in ("P", "S"):
        U = T[T.in_P] if samp == "P" else T
        P(f"\n=== sample {samp}: N = {len(U)} lenses with a qualifying DESI dispersion ===")
        for fn in FOOT:
            P(f"-- footing {fn} (a0 = {FOOT[fn]:.4e})")
            words = {}
            for law in ("S", "B"):
                for b in BETAS:
                    for fw in SEEING:
                        key = f"b_{fn}_{law}_{b:+.1f}_{fw}"
                        if key not in U:
                            continue
                        if not (b == 0.0 or fw == 1.1):
                            continue
                        m, lo, hi = boot_median(U[key])
                        ne = int((U[key.replace("b_", "edge_", 1)] != "ok").sum())
                        w = word(lo, hi)
                        if law == "S":
                            words[(b, fw)] = w
                        P(f"   law {law} beta {b:+.1f} seeing {fw}\": b_med {m:+.4f} [{lo:+.4f}, {hi:+.4f}]  "
                          f"at search end {ne}  -> {w if law == 'S' else '(reported)'}")
                        res["footings"].setdefault(samp, {}).setdefault(fn, {})[key] = dict(med=m, lo=lo, hi=hi, edge=ne, word=w)
            head = words[(0.0, 1.1)]
            stable = len(set(words.values())) == 1
            final = head if stable else "NO VERDICT"
            if len(U) < 30:
                final = "NOT EVALUABLE (N < 30)"
            if not (f1_ok and j_ok):
                lab = f"NOT EVALUABLE (F1 {'pass' if f1_ok else 'FAIL'}, J {'pass' if j_ok else 'FAIL'}); would-be word on the numbers: {final}"
            else:
                lab = final + " (under A1; conditional on F2, not run blind)"
            P(f"   WORD {samp} {fn}: {lab}; variant words {sorted(set(words.values()))}")
            res["footings"][samp][fn]["word"] = lab
            # reported items
            key = f"b_{fn}_S_+0.0_1.1"
            dd = U[key] - U[f"binf_{fn}_S"]
            P(f"   b_dyn - b_inf (law S): median {dd.median():+.4f}, fraction < -0.25: {(dd < -0.25).mean():.3f}; "
              f"b_inf median {U[f'binf_{fn}_S'].median():+.4f}")
            zc = U[f"zs_cond_{fn}"]
            P(f"   CONDITIONAL source z where b_lens = b_dyn: median {np.nanmedian(zc) if zc.notna().any() else float('nan'):.3f} "
              f"(over solvable), fraction with no solution {zc.isna().mean():.3f}")
            for lab2, sel in (("thetaE<1.0", U.thetaE < 1.0), ("1.0-1.3", (U.thetaE >= 1.0) & (U.thetaE < 1.3)),
                              ("1.3-1.7", (U.thetaE >= 1.3) & (U.thetaE < 1.7)), (">1.7", U.thetaE >= 1.7),
                              (">1.3", U.thetaE >= 1.3)):
                V = U[sel]
                if len(V) >= 3:
                    m, lo, hi = boot_median(V[key])
                    P(f"   class {lab2:10s} N={len(V):2d}: b_med {m:+.4f} [{lo:+.4f}, {hi:+.4f}]")
                else:
                    P(f"   class {lab2:10s} N={len(V):2d}: " + ", ".join(f"{x:+.3f}" for x in V[key]))
            # window sensitivity
            V = U[U.in_window]
            m, lo, hi = boot_median(V[key])
            P(f"   photo-z window kept only (N={len(V)}): b_med {m:+.4f} [{lo:+.4f}, {hi:+.4f}]")
            # READING R
            ms, los, his = boot_median(U[f"bR_{fn}_s"])
            m1, lo1, hi1 = boot_median(U[f"bR_{fn}_lo"])
            m2, lo2, hi2 = boot_median(U[f"bR_{fn}_hi"])
            env = (min(los, lo1, lo2), max(his, hi1, hi2))
            P(f"   READING R (sigma / s, s = {scale['degraded']['s']:.4f} [{scale['degraded']['lo']:.4f}, "
              f"{scale['degraded']['hi']:.4f}]): b_med {ms:+.4f}, envelope [{env[0]:+.4f}, {env[1]:+.4f}] "
              f"-> READING R would-be {word(*env)} (not a frozen word)")
            res["footings"][samp][fn]["readingR"] = dict(med=ms, lo=env[0], hi=env[1], word=word(*env))
    json.dump(res, open(f"{HERE}/euc5r_results{TAG}.json", "w"), indent=1)
    open(f"{HERE}/euc5r{TAG}.out", "w").write("\n".join(LINES) + "\n")
    if MUT == "newton":
        base = json.load(open(f"{HERE}/euc5r_results.json"))
        rise = all(res["footings"]["P"][fn]["b_" + fn + "_S_+0.0_1.1"]["med"] >
                   base["footings"]["P"][fn]["b_" + fn + "_S_+0.0_1.1"]["med"] for fn in FOOT)
        P(f"MUTATE newton: b_med on P rises on both footings: {rise}")
        open(f"{HERE}/euc5r{TAG}.out", "w").write("\n".join(LINES) + "\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
