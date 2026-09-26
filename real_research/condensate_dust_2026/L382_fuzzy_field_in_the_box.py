#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
L382 -- THE FUZZY WAVE FIELD IN THE PARTICLE-MESH BOX: can the record's box tell a wave field (fuzzy dark matter) from the
collisionless carrier at the boson masses the Lyman-alpha forest still allows?

WHY.  L374: the minimal condensate cannot pass through itself at a stream crossing, while a linear wave field
  (Schroedinger-Poisson; fuzzy dark matter) with the same dispersion tracks the collisionless answer.  The next question is
  what the wave field does in the record's particle-mesh box (L366-L378, L373: 100 Mpc/h, 256^3 mesh, 0.39 Mpc/h cells).
  A wave field differs from collisionless dust in two ways only: (a) its initial power is suppressed below its Jeans scale
  (Hu, Barkana & Gruzinov 2000: T(k) = cos(x^3) / (1 + x^8), x = 1.61 m22^(1/18) k / k_J,eq, k_J,eq = 9 m22^(1/2) Mpc^-1,
  m22 = m / 1e-22 eV); (b) below its de Broglie length it interferes and forms solitonic cores.  Above its de Broglie length
  it moves as collisionless dust (L374's positive control), so on the mesh everything else is the box as it stands.  The
  forest bounds the boson mass from below: m >~ 2e-21 eV (Irsic et al. 2017), m >~ 2e-20 eV (Rogers & Peiris 2021).

METHOD.  On the box's own mesh (its |k| grid, its CLASS linear spectrum at z_i = 49, L362's P_lin): the wave field's change
  to the box's initial conditions -- total density variance, sigma_8, rms displacement, each |k| shell, and the one-
  dimensional power along a mesh axis on the forest gate's k_par = 0.2-2 h/Mpc -- at m22 = 1 (forest-excluded), 20 and 200
  (the two forest bounds).  The box's evolution is the same code from those initial conditions.  Sub-mesh: de Broglie
  lengths at galaxy / group / cluster speeds and solitonic core radii (Schive et al. 2014: r_c ~ 1.6 kpc / m22 x
  (M_h / 1e9 Msun)^(-1/3)) against the mesh cell and Harvey's 100 kpc aperture.
PRE-DECLARED (before any run).  H: at the forest-allowed masses (m22 = 20, 200) the wave field changes the box's initial
  total variance, sigma_8 and rms displacement by < 1% and every mesh shell and the forest-range 1D power by < 2%, and its
  sub-mesh scales (de Broglie length at group/cluster speeds, solitonic cores of 1e14-1e15 Msun halos) are < 1% of
  Harvey's aperture -- so the box and its gates cannot tell the wave field from the carrier, and L373's verdict is the wave
  field's.  Reported: at m22 = 1 the box sees it.
CHECKS
  C1 IDENTITY: the transfer is Hu-Barkana-Gruzinov's -- T(k -> 0) = 1 and the half-mode scale goes as m^(4/9) (fitted exponent
     within 0.002), with k_1/2(m22 = 1) = 4.5-4.7 Mpc^-1.
  C2 CONTROL: P_lin on the unique |k| of the mesh reproduces direct evaluation at 200 random mesh points (1e-12).
  C3 LIMIT: at m22 = 1e6 the box's initial variance changes by < 1e-8 (the collisionless limit).
  R1 = H.   W (reported) the full table and the sub-mesh scales.
MUTATE=1 sets the "allowed" masses to m22 = 0.01 (1e-24 eV): the box sees the wave field and R1 flips.
Run from the repository root:  python3 real_research/condensate_dust_2026/L382_fuzzy_field_in_the_box.py
"""
import os, sys, json, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "real_research", "dark_sector_2026"))
import L366_triggered_carrier_cluster_retention as L6          # noqa: E402  (the box's constants and L362's Sim / P_lin)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "L382_fuzzy_field_in_the_box" + ("_MUTATE" if MUTATE else "")
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "L382", "mutate": MUTATE, "checks": {}, "numbers": {}}
EXPECT_BLIND = True                                                # H, set before any run
L2, h, ZI, LBOX, NG, NP = L6.L2, L6.h, L6.ZI, L6.LBOX, L6.NG, L6.NP
M_EXCL, M_ALLOWED = 1.0, ((0.01, 0.01) if MUTATE else (20.0, 200.0))
HBAR_EVS, C_KMS, KPC_M, MSUN_EV = 6.582119569e-16, 299792.458, 3.0857e19, 1.115e66
CELL_KPC = LBOX / NG / h * 1e3                                      # physical kpc at z = 0


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 116); P(t); P("=" * 116)


def T_fdm(k_mpc, m22):
    """Hu, Barkana & Gruzinov 2000; k in comoving Mpc^-1."""
    x = 1.61 * m22 ** (1.0 / 18.0) * np.asarray(k_mpc, float) / (9.0 * math.sqrt(m22))
    return np.cos(x ** 3) / (1.0 + x ** 8)


def k_half(m22):
    """the half-mode scale T^2 = 1/2 (Mpc^-1): the first root, by bisection on the monotone low-k branch."""
    lo, hi = 1e-6, 50.0 * m22 ** (4.0 / 9.0)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if T_fdm(mid, m22) ** 2 > 0.5:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: the 'allowed' masses are set to m22 = 0.01 -- the box must see the wave field ***")

    # ------------------------------------------------------------------------------------------ the box's mesh and spectrum
    s = L2.Sim(LBOX, NG, NP)
    K2 = np.asarray(s.K2, float).ravel()
    keep = np.ones(K2.size, bool); keep[0] = False                 # Sim sets K2[0, 0, 0] = 1 (not 0): drop the zero mode
    Kh = np.sqrt(K2[keep])                                          # h/Mpc, every mode of the box's initial conditions
    uq, inv = np.unique(np.round(K2[keep], 12), return_inverse=True)
    Pu = np.array([L2.P_lin(math.sqrt(q), ZI) for q in uq])
    Pk = Pu[inv]
    rng = np.random.default_rng(3); idx = rng.choice(Kh.size, 200, replace=False)
    dev = max(abs(Pk[i] / L2.P_lin(Kh[i], ZI) - 1) for i in idx)
    P(f"  mesh: {NG}^3 over {LBOX:.0f} Mpc/h ({CELL_KPC:.0f} kpc cells at z = 0); |k| from {Kh.min():.3f} to {Kh.max():.2f} h/Mpc "
      f"(Nyquist {math.pi * NG / LBOX:.2f}); {uq.size} distinct |k|   [{time.time() - T0:.0f}s]")

    # ------------------------------------------------------------------------------------------ C1-C3
    banner("C1-C3  THE TRANSFER, THE SPECTRUM ON THE MESH, THE COLLISIONLESS LIMIT")
    ms = np.array([1.0, 20.0, 200.0])
    kh_ = np.array([k_half(m) for m in ms])
    slope = float(np.polyfit(np.log(ms), np.log(kh_), 1)[0])
    check("C1 IDENTITY: the transfer is Hu-Barkana-Gruzinov's -- T(k -> 0) = 1, k_1/2 ~ m^(4/9) (exponent within 0.002), "
          "k_1/2(m22 = 1) in 4.5-4.7 Mpc^-1",
          f"T(1e-6) - 1 = {T_fdm(1e-6, 1.0) - 1:.1e}; exponent {slope:.4f} (4/9 = {4 / 9:.4f}); k_1/2 = "
          + ", ".join(f"{k:.2f} Mpc^-1 ({k / h:.1f} h/Mpc) at m22 = {m:g}" for m, k in zip(ms, kh_)),
          abs(T_fdm(1e-6, 1.0) - 1) < 1e-12 and abs(slope - 4 / 9) < 0.002 and 4.5 <= kh_[0] <= 4.7)
    check("C2 CONTROL: P_lin on the mesh's distinct |k| reproduces direct evaluation at 200 random modes", f"max deviation {dev:.1e}",
          dev < 1e-12)
    W8 = lambda k: 3 * (np.sin(8 * k) - 8 * k * np.cos(8 * k)) / (8 * k) ** 3

    def box_change(m22):
        T2 = T_fdm(Kh * h, m22) ** 2
        var = float(np.sum(Pk * T2) / np.sum(Pk))
        w8 = W8(Kh) ** 2
        s8 = math.sqrt(float(np.sum(Pk * T2 * w8) / np.sum(Pk * w8)))
        disp = math.sqrt(float(np.sum(Pk * T2 / Kh ** 2) / np.sum(Pk / Kh ** 2)))
        edges = np.linspace(Kh.min(), Kh.max() * (1 + 1e-9), 41)
        sh = np.digitize(Kh, edges) - 1
        shell = np.array([np.sum(Pk[sh == b] * T2[sh == b]) / max(np.sum(Pk[sh == b]), 1e-300) for b in range(40)])
        # the 1D power along a mesh axis at the forest gate's k_par: sum over the transverse modes of each k_x
        kx = np.abs(np.asarray(np.meshgrid(*(3 * [np.fft.fftfreq(NG, LBOX / NG) * 2 * np.pi]), indexing="ij")[0]).ravel()[keep])
        kp = np.unique(np.round(kx, 10)); kp = kp[(kp >= 0.2) & (kp <= 2.0)]
        p1 = np.array([np.sum((Pk * T2)[np.abs(kx - q) < 1e-8]) / np.sum(Pk[np.abs(kx - q) < 1e-8]) for q in kp])
        return dict(var=var, s8=s8, disp=disp, shell_min=float(shell.min()), shell_top=float(shell[-1]),
                    p1d_min=float(p1.min()), T2_nyq=float(T_fdm(math.pi * NG / LBOX * h, m22) ** 2),
                    T2_corner=float(T_fdm(Kh.max() * h, m22) ** 2))
    lim = box_change(1e6)
    check("C3 LIMIT: at m22 = 1e6 the box's initial variance changes by < 1e-8 (the collisionless limit)",
          f"1 - variance ratio {1 - lim['var']:.1e}", abs(1 - lim["var"]) < 1e-8)

    # ------------------------------------------------------------------------------------------ the box at each mass
    banner("THE BOX'S INITIAL CONDITIONS WITH THE WAVE FIELD (ratios to the collisionless carrier's)")
    TAB = {}
    for m in (M_EXCL,) + M_ALLOWED:
        r = box_change(m); TAB[f"{m:g}"] = r
        P(f"    m = {m:g}e-22 eV: variance {r['var']:.6f} | sigma_8 {r['s8']:.6f} | rms displacement {r['disp']:.6f} | worst shell "
          f"{r['shell_min']:.4f} | forest-range 1D power >= {r['p1d_min']:.4f} | T^2 at Nyquist {r['T2_nyq']:.4f}, at the corner {r['T2_corner']:.4f}")

    # ------------------------------------------------------------------------------------------ below the mesh
    banner("BELOW THE MESH: de Broglie lengths and solitonic cores (kpc) against the cell and Harvey's 100 kpc aperture")
    SUB = {}
    for m in (M_EXCL,) + M_ALLOWED:
        # lambda = h / (m v) = 2 pi hbar c^2 / (m c^2 v): hbar [eV s] c^2 [km^2/s^2] / (eV km/s) = km -> kpc
        lam = {v: 2 * math.pi * HBAR_EVS * (C_KMS ** 2) / (m * 1e-22 * v) / (KPC_M / 1e3) for v in (200.0, 700.0, 1200.0)}
        core = {Mh: 1.6 / m * (Mh / 1e9) ** (-1.0 / 3.0) for Mh in (1e12, 1e14, 1e15)}
        SUB[f"{m:g}"] = dict(lambda_dB_kpc={str(v): x for v, x in lam.items()}, soliton_core_kpc={f"{k:.0e}": x for k, x in core.items()})
        P(f"    m = {m:g}e-22 eV: de Broglie length {lam[200.0]:.3g} / {lam[700.0]:.3g} / {lam[1200.0]:.3g} kpc at 200 / 700 / 1200 km/s; "
          f"solitonic core {core[1e12]:.3g} / {core[1e14]:.3g} / {core[1e15]:.3g} kpc in 1e12 / 1e14 / 1e15 Msun halos; mesh cell "
          f"{CELL_KPC:.0f} kpc")

    # ------------------------------------------------------------------------------------------ R1
    banner("R1  THE HYPOTHESIS (set before any run)")
    ok = []
    for m in M_ALLOWED:
        r, sb = TAB[f"{m:g}"], SUB[f"{m:g}"]
        ok.append(abs(1 - r["var"]) < 0.01 and abs(1 - r["s8"]) < 0.01 and abs(1 - r["disp"]) < 0.01 and r["shell_min"] > 0.98
                  and r["p1d_min"] > 0.98 and sb["lambda_dB_kpc"]["700.0"] < 1.0 and sb["soliton_core_kpc"]["1e+14"] < 1.0)
    ex = TAB[f"{M_EXCL:g}"]
    check("R1 = H: at the forest-allowed masses the box cannot tell the wave field from the carrier (initial variance, sigma_8, "
          "displacement < 1%; every shell and the forest-range 1D power < 2%; de Broglie length and group cores < 1 kpc)",
          f"m22 {M_ALLOWED}: {ok}; for contrast m22 = 1 (forest-excluded): worst shell {ex['shell_min']:.3f}, T^2 at Nyquist {ex['T2_nyq']:.3f}",
          all(ok) == EXPECT_BLIND)
    check("W (reported) the table and the sub-mesh scales", "see above", True, load_bearing=False)
    OUT["numbers"].update(k_half_mpc={f"{m:g}": float(k) for m, k in zip(ms, kh_)}, box=TAB, sub_mesh=SUB, cell_kpc=CELL_KPC,
                          allowed=M_ALLOWED, excluded=M_EXCL)

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        kk = np.geomspace(0.01, 60, 600)
        fig, ax = plt.subplots(figsize=(7.5, 4.2))
        for m, c in zip((M_EXCL,) + M_ALLOWED, ("C3", "C0", "C2")):
            ax.plot(kk, T_fdm(kk * h, m) ** 2, color=c, label=f"m = {m:g} x 1e-22 eV" + (" (forest-excluded)" if m == M_EXCL else ""))
        ax.axvspan(Kh.min(), Kh.max(), color="0.9", zorder=0, label="the box's mesh")
        ax.axvspan(0.2, 2.0, color="C1", alpha=0.15, zorder=0, label="forest gate k_par")
        ax.set_xscale("log"); ax.set_ylim(-0.05, 1.08); ax.set_xlabel("k [h/Mpc]"); ax.set_ylabel("T^2 (wave field / carrier)")
        ax.set_title("the wave field's initial-power suppression on the box's mesh", fontsize=9); ax.legend(fontsize=7)
        fig.tight_layout(); fig.savefig(os.path.join(HERE, SLUG + ".png"), dpi=110); P(f"  figure: {SLUG}.png")
    except Exception as e_:
        P(f"  figure skipped: {e_}")

    banner("VERDICT")
    n_fail = sum(1 for _, ok_, lb in CH if lb and not ok_)
    OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
    json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1,
              default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"  {sum(1 for _, ok_, _ in CH if ok_)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {SLUG}_results.json   [{time.time() - T0:.0f}s]")
    P(f"rc={0 if n_fail == 0 else 1}")
    sys.exit(0 if n_fail == 0 else 1)
