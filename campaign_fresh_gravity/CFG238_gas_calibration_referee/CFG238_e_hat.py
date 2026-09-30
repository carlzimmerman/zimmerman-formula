#!/usr/bin/env python3
"""CFG238 attack e: three-cornered hat on NOEMA3D (N = 5), pair-type confound, reconstruction sensitivities (frozen D14, section 6e). Exit 0."""
import sys
from scipy import stats
from CFG238_common import *


def hat_from_idx(cc, cd, idu, idx):
    """cc = CO-CI, cd = CO-dust, idu = CI-dust for the galaxy rows idx (with repeats)."""
    return hat(cc[idx], cd[idx], idu[idx])


def noema_rebuild(cosmo_name="Planck18", Td=25.0, beta=1.8, dust_nu_scale=1.0):
    from astropy.cosmology import FlatLambdaCDM, Planck18
    import astropy.units as u
    cosmo = Planck18 if cosmo_name == "Planck18" else FlatLambdaCDM(H0=70, Om0=0.3)
    G = readcsv(os.path.join(NO, "noema3d_per_galaxy.csv"))
    OBS = {r["id"]: r for r in readcsv(os.path.join(NO, "noema3d_observations.csv")) if r["weighting"] != "Ro5"}
    out = {}
    for g in G:
        z = float(g["z"]); DL = cosmo.luminosity_distance(z).to(u.Mpc).value
        nu_co = float(OBS[g["id"]]["freq_GHz"])
        group1 = "CO4-3" in OBS[g["id"]]["line"]; R1J = 2.4 if group1 else 1.8
        Lp = lambda S, nu: 3.25e7 * S * nu ** -2 * DL ** 2 * (1 + z) ** -3
        d = {}
        S = fl(g["S_CO_P2_Jykms"]); d["CO"] = 4.36 * R1J * Lp(S, nu_co) if S else None
        Sci = fl(g["S_CI_Jykms"]); d["CI"] = 18.7 * Lp(Sci, 492.161 / (1 + z)) if Sci else None
        Sd = fl(g["S_dust_mJy"])
        if Sd:
            nu_rest = nu_co * dust_nu_scale * (1 + z)
            K = (353.0 / nu_rest) ** (3 + beta) * ((math.exp(0.04799 * nu_rest / Td) - 1) / (math.exp(16.956 / Td) - 1))
            DLm = DL * 3.0857e22
            d["dust"] = 4 * math.pi * Sd * 1e-29 * K * DLm ** 2 / (1 + z) / 6.7e12
        d["CO_t1"] = 10 ** float(g["logMmol_CO_P2"])
        out[g["id"]] = d
    return out


if __name__ == "__main__":
    outp, jp = out_paths("CFG238_e_hat")
    T = Tee(outp)
    banner(T, "CFG238 attack e (three-cornered hat N=5, exact bootstrap, mocks, pair-type confound, NOEMA3D sensitivities)")
    R = {}
    LINES = []

    def line(lid, ok, msg):
        LINES.append((lid, ok))
        T(f"  [{'PASS' if ok else 'MISS'}] {lid} {msg}")

    NO_ = load_noema()
    ok5 = [r for r in NO_ if r["ok"] == 1]
    ids5 = [r["id"] for r in ok5]
    cd = np.array([r["CO_t1"] - r["dust"] for r in ok5]); cc = np.array([r["CO_t1"] - r["CI"] for r in ok5]); idu = np.array([r["CI"] - r["dust"] for r in ok5])
    T(f"N validated = {len(ok5)} of {len(NO_)}: {ids5}; z {[r['z'] for r in ok5]}; groups {sorted(set(r['group'] for r in ok5))} (all group 1, CO(4-3), R_14 = 2.4)")
    for r, a, b, c in zip(ok5, cd, cc, idu):
        T(f"  {r['id']}: CO-dust {a:+.3f}  CO-CI {b:+.3f}  CI-dust {c:+.3f}")
    T(f"  means: CO-dust {cd.mean():+.4f} CO-CI {cc.mean():+.4f} CI-dust {idu.mean():+.4f}; SD {cd.std(ddof=1):.4f} {cc.std(ddof=1):.4f} {idu.std(ddof=1):.4f}")
    # t interval and N needed
    sd_ = cd.std(ddof=1); se_ = sd_ / math.sqrt(5)
    tt = stats.t.ppf(0.975, 4)
    T(f"  95% t-interval (4 dof) of the mean CO-dust: {cd.mean():+.3f} +- {tt * se_:.3f}  -> [{cd.mean() - tt * se_:+.3f}, {cd.mean() + tt * se_:+.3f}]")
    Nn = {}
    for hw in (0.10, 0.05, 0.03):
        nn = 5
        while stats.t.ppf(0.975, nn - 1) * sd_ / math.sqrt(nn) > hw:
            nn += 1
        Nn[hw] = nn
    T(f"  N needed (t-based, SD {sd_:.3f}) for a 95% half-width of 0.10 / 0.05 / 0.03 dex: {Nn}")
    R["tint"] = dict(half=tt * se_, N_needed=Nn)
    # hat point estimates
    vCO, vCI, vdu = hat(cc, cd, idu)
    T(f"  hat variances: CO {vCO:.5f}  CI {vCI:.5f}  dust {vdu:.5f}  (sigma: {sgn_sqrt(vCO):.3f}, {sgn_sqrt(vCI):.3f}, {sgn_sqrt(vdu):.3f})")
    R["hat"] = dict(vCO=vCO, vCI=vCI, vdust=vdu)
    # jackknife
    jk = []
    for i in range(5):
        m = np.arange(5) != i
        jk.append(hat(cc[m], cd[m], idu[m]))
    jk = np.array(jk)
    jse = np.sqrt((4 / 5) * ((jk - jk.mean(0)) ** 2).sum(0))
    T(f"  jackknife SE of the variances: CO {jse[0]:.5f} CI {jse[1]:.5f} dust {jse[2]:.5f}  -> relative to |estimate|: {np.round(jse / np.abs([vCO, vCI, vdu]), 2).tolist()}")
    R["jackknife_se"] = jse.tolist()
    # exact enumeration of the bootstrap
    seqs = list(itertools.product(range(5), repeat=5))
    ex = np.array([hat(cc[list(s)], cd[list(s)], idu[list(s)]) if len(set(s)) > 1 else (0.0, 0.0, 0.0) for s in seqs])
    # hat() on a resample with all-equal galaxies has zero variance -> (0,0,0)
    nmulti = len({tuple(sorted(s)) for s in seqs})
    T(f"  exact bootstrap: {len(seqs)} equally likely sequences, {nmulti} distinct multisets (degenerate all-same: {sum(1 for s in seqs if len(set(s)) == 1)} sequences, variances 0)")
    names = ("sigma_CO^2", "sigma_CI^2", "sigma_dust^2")
    exr = {}
    for j, nm in enumerate(names):
        v = ex[:, j]
        exr[nm] = dict(median=float(np.median(v)), p16=float(np.percentile(v, 16)), p84=float(np.percentile(v, 84)), p2_5=float(np.percentile(v, 2.5)), p97_5=float(np.percentile(v, 97.5)), fneg=float((v < 0).mean()))
        T(f"   {nm}: point {[vCO, vCI, vdu][j]:+.5f}  exact-bootstrap median {exr[nm]['median']:+.5f}; 68% [{exr[nm]['p16']:+.5f}, {exr[nm]['p84']:+.5f}]; 95% [{exr[nm]['p2_5']:+.5f}, {exr[nm]['p97_5']:+.5f}]; fraction negative {exr[nm]['fneg']:.3f}")
    anyneg = float(((ex < 0).any(1)).mean())
    T(f"   fraction of exact-bootstrap resamples with at least one negative variance {anyneg:.3f}")
    # sigma (std) intervals for the README-style quote
    for j, nm in enumerate(("sigma_CO", "sigma_CI", "sigma_dust")):
        sv = np.sign(ex[:, j]) * np.sqrt(np.abs(ex[:, j]))
        T(f"   {nm} (signed sqrt): 95% bootstrap interval [{np.percentile(sv, 2.5):+.3f}, {np.percentile(sv, 97.5):+.3f}], 68% [{np.percentile(sv, 16):+.3f}, {np.percentile(sv, 84):+.3f}]")
        exr[nm] = dict(p2_5=float(np.percentile(sv, 2.5)), p97_5=float(np.percentile(sv, 97.5)))
    R["exact"] = exr
    R["exact_anyneg"] = anyneg
    rng = np.random.default_rng(238)
    rb = np.array([hat(cc[i], cd[i], idu[i]) for i in rng.integers(0, 5, (20000, 5))])
    T(f"  random bootstrap check (20000, seed 238): fraction negative CO {float((rb[:, 0] < 0).mean()):.3f} CI {float((rb[:, 1] < 0).mean()):.3f} dust {float((rb[:, 2] < 0).mean()):.3f}")
    line("H-C19a", exr["sigma_CI^2"]["fneg"] > 0.5, f"fraction with sigma_CI^2 < 0 in the exact bootstrap {exr['sigma_CI^2']['fneg']:.3f} (estimate > 0.5)")
    line("H-C19b", exr["sigma_CO^2"]["p2_5"] <= 0, f"95% interval of sigma_CO^2 [{exr['sigma_CO^2']['p2_5']:+.5f}, {exr['sigma_CO^2']['p97_5']:+.5f}] includes 0 (estimate: yes)")
    line("H-C19c", exr["sigma_dust^2"]["p2_5"] <= 0, f"95% interval of sigma_dust^2 [{exr['sigma_dust^2']['p2_5']:+.5f}, {exr['sigma_dust^2']['p97_5']:+.5f}] includes 0 (estimate: yes, P 0.5)")
    # mocks
    T("\n== mocks (seed 2385, K = 20000): estimator behaviour at N = 5 and 10")
    rng = np.random.default_rng(2385)
    mock = {}
    for truth in ((0.084, 0.05, 0.105), (0.084, 0.084, 0.105), (0.10, 0.10, 0.10)):
        for N in (5, 10):
            e = rng.normal(0, 1, (20000, N, 3)) * np.array(truth)
            A_, B_, C_ = e[:, :, 0], e[:, :, 1], e[:, :, 2]   # CO, CI, dust errors
            v_ab = np.var(A_ - B_, axis=1, ddof=1); v_ac = np.var(A_ - C_, axis=1, ddof=1); v_bc = np.var(B_ - C_, axis=1, ddof=1)
            sA = (v_ab + v_ac - v_bc) / 2; sB = (v_ab + v_bc - v_ac) / 2; sC = (v_ac + v_bc - v_ab) / 2
            fn = [float((s < 0).mean()) for s in (sA, sB, sC)]
            fa = float(((sA < 0) | (sB < 0) | (sC < 0)).mean())
            rel = [float(np.median(s) / t_ ** 2) for s, t_ in zip((sA, sB, sC), truth)]
            mock[f"{truth}|N={N}"] = dict(fneg=fn, fany=fa, med_over_true=rel)
            T(f"  truth {truth} N {N}: negative fraction CO/CI/dust {np.round(fn, 3).tolist()}; any negative {fa:.3f}; median(sigma^2-hat)/sigma^2 {np.round(rel, 2).tolist()}")
    R["mock"] = mock
    f55 = mock["(0.1, 0.1, 0.1)|N=5"]["fany"]
    line("H-A5", abs(f55 - 0.55) <= 0.05, f"N=5 equal-sigma mock, at least one negative variance {f55:.3f} (estimate 0.55 +- 0.05; README '54%')")
    # correlated errors
    T("  correlated-error mocks (shared component between CO and dust; truth sigma (0.10, 0.15, 0.20)):")
    corr = {}
    sg = np.array([0.10, 0.15, 0.20])
    for rho in (-0.3, 0.0, 0.3, 0.5):
        C = np.diag(sg ** 2); C[0, 2] = C[2, 0] = rho * sg[0] * sg[2]
        L_ = np.linalg.cholesky(C)
        for N in (300, 5):
            e = rng.normal(0, 1, (4000 if N == 300 else 20000, N, 3)) @ L_.T
            A_, B_, C_ = e[:, :, 0], e[:, :, 1], e[:, :, 2]
            v_ab = np.var(A_ - B_, axis=1, ddof=1); v_ac = np.var(A_ - C_, axis=1, ddof=1); v_bc = np.var(B_ - C_, axis=1, ddof=1)
            sA = (v_ab + v_ac - v_bc) / 2; sB = (v_ab + v_bc - v_ac) / 2; sC = (v_ac + v_bc - v_ab) / 2
            rel = [float(np.sqrt(np.abs(np.median(s))) * np.sign(np.median(s)) / t_) for s, t_ in zip((sA, sB, sC), sg)]
            corr[f"rho={rho}|N={N}"] = dict(sigma_over_true=rel, fany=float(((sA < 0) | (sB < 0) | (sC < 0)).mean()))
            T(f"   rho {rho:+.1f} N {N}: median sigma-hat / true (CO, CI, dust) {np.round(rel, 3).tolist()}; any negative {corr[f'rho={rho}|N={N}']['fany']:.3f}")
    R["corr"] = corr
    # independence audit: distance / cosmology
    T("\n== independence audit: distances, cosmology, dust frequency (transcription of the recipes read in the data chat script)")
    RB = {}
    for cn in ("Planck18", "H070"):
        B = noema_rebuild(cn)
        RB[cn] = B
    chat = {r["id"]: r for r in NO_}
    mx = {}
    for k in ("CO", "CI", "dust"):
        dd = [math.log10(RB["Planck18"][i][k]) - {"CO": chat[i]["CO_rec"], "CI": chat[i]["CI"], "dust": chat[i]["dust"]}[k] for i in chat if RB["Planck18"][i].get(k) and {"CO": chat[i]["CO_rec"], "CI": chat[i]["CI"], "dust": chat[i]["dust"]}[k] is not None]
        mx[k] = float(np.max(np.abs(dd)))
        T(f"  transcription rebuild (Planck18) vs data chat CSV: {k}: N {len(dd)} max |diff| {mx[k]:.4f} dex (CSV rounding 0.001)")
    R["rebuild_maxdiff"] = mx
    line("T-rebuild", max(mx.values()) < 0.01, f"transcription rebuild reproduces the CSV masses to {max(mx.values()):.4f} dex (recipe shared, NOT independent)")
    # CO control of the rebuild against Table 1
    res = {i: math.log10(RB["Planck18"][i]["CO"] / RB["Planck18"][i]["CO_t1"]) for i in chat}
    T(f"  CO control (rebuild - Table 1): " + ", ".join(f"{i}:{v:+.3f}" for i, v in res.items()))
    # cosmology effect on pair differences
    def five(B, co="CO_t1"):
        a = np.array([math.log10(B[i][co] / B[i]["dust"]) for i in ids5]); b = np.array([math.log10(B[i]["CI"] / B[i]["dust"]) for i in ids5])
        return a.mean(), b.mean()
    T(f"  five validated: CO(Table1)-dust {five(RB['Planck18'])[0]:+.3f} [Planck18], {five(RB['H070'])[0]:+.3f} [H0=70]; CI-dust {five(RB['Planck18'])[1]:+.3f} / {five(RB['H070'])[1]:+.3f}  (distance is common-mode: CO rebuild uses the same D_L^2)")
    sens = {}
    for Td in (20.0, 25.0, 30.0, 35.0):
        for beta in (1.6, 1.8, 2.0):
            for fs in (0.9, 1.0, 1.1):
                B = noema_rebuild("Planck18", Td, beta, fs)
                a, b = five(B)
                sens[(Td, beta, fs)] = (a, b)
    arr = np.array(list(sens.values()))
    T(f"  dust-recipe sensitivity over T_d 20-35 K x beta 1.6-2.0 x dust frequency +-10% (36 cells): CO-dust mean spans {arr[:, 0].min():+.3f} to {arr[:, 0].max():+.3f} (span {np.ptp(arr[:, 0]):.3f}); CI-dust spans {arr[:, 1].min():+.3f} to {arr[:, 1].max():+.3f}")
    sub = {k: v for k, v in sens.items() if k[2] == 1.0}
    a2 = np.array(list(sub.values()))
    T(f"    at the nominal dust frequency only (12 cells): CO-dust {a2[:, 0].min():+.3f} to {a2[:, 0].max():+.3f} (span {np.ptp(a2[:, 0]):.3f}); frequency +-10% alone at T 25 K, beta 1.8: {sens[(25.0, 1.8, 0.9)][0]:+.3f} / {sens[(25.0, 1.8, 1.1)][0]:+.3f} vs nominal {sens[(25.0, 1.8, 1.0)][0]:+.3f}")
    R["dust_sens"] = dict(span_CO_dust=float(np.ptp(arr[:, 0])), span_CI_dust=float(np.ptp(arr[:, 1])), span_nominal_freq=float(np.ptp(a2[:, 0])))
    line("H-C22", np.ptp(arr[:, 0]) >= 0.15, f"CO-dust span over the dust-recipe grid {np.ptp(arr[:, 0]):.3f} (estimate >= 0.15)")

    # pair-type confound
    T("\n== pair-type confound: K by pair type, source and bin")
    d82, _ = s82_d()
    s82 = msd(d82)
    B9 = load_bourne(); dB = np.array([r["logCI"] - r["logDust"] for r in B9]); sB = msd(dB)
    sN = msd(idu); sNc = msd(cd)
    rows_ = [("B1 z<0.2", "CO-dust", "Stripe82", s82), ("B2 z~1", "[CI]-dust", "Bourne+19", sB), ("B2 z~1.2", "[CI]-dust", "NOEMA3D five", sN), ("B2 z~1.2", "CO-dust", "NOEMA3D five", sNc)]
    for b_, pt, src, st in rows_:
        T(f"  {b_:10s} {pt:10s} {src:14s}: N {st['N']:3d} mean {st['mean']:+.3f} SE {st['se']:.3f} K {Kfun(st['mean'], st['se']):.3f}")
    dco = sNc["mean"] - s82["mean"]; seco = math.sqrt(sNc["se"] ** 2 + s82["se"] ** 2)
    dci = sN["mean"] - sB["mean"]; seci = math.sqrt(sN["se"] ** 2 + sB["se"] ** 2)
    T(f"  like-for-like CO-dust, NOEMA3D five minus Stripe82: {dco:+.3f} +- {seco:.3f} ({dco / seco:+.2f} sigma)")
    T(f"  [CI]-dust, NOEMA3D five minus Bourne+19: {dci:+.3f} +- {seci:.3f} ({dci / seci:+.2f} sigma)")
    line("H-C20", abs(dco - 0.051) <= 0.01 and abs(seco - 0.063) <= 0.01, f"CO-dust like-for-like {dco:+.3f} +- {seco:.3f} (hand +0.051 +- 0.063)")
    line("H-C21", abs(dci - 0.152) <= 0.01 and abs(seci - 0.072) <= 0.01, f"[CI]-dust source difference {dci:+.3f} +- {seci:.3f} (hand 0.152 +- 0.072)")
    # helium sensitivity on Bourne
    he = math.log10(1.36)
    for lab, sh in (("Bourne continuum mass + He (x1.36)", -he), ("Bourne [CI] mass without He", -he), ("Bourne continuum without He", +he)):
        pooled = np.concatenate([dB + sh, idu])
        sp = msd(pooled)
        T(f"  labelled He sensitivity ({lab}: Bourne offset shifted by {sh:+.3f}): Bourne mean {sB['mean'] + sh:+.3f}; pooled N {sp['N']} mean {sp['mean']:+.3f} SE {sp['se']:.3f} K {Kfun(sp['mean'], sp['se']):.3f}")
    T("  He treatment of Bourne's continuum mass is not stated on disk; [CI] is H2 + He per the repo HTML of 1810.01640.")
    R["pairtype"] = dict(dco=dco, seco=seco, dci=dci, seci=seci)
    R["lines"] = LINES
    dump(jp, R)
    T.close()
    sys.exit(0)
