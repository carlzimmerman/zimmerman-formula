#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
P34d -- RESOLUTION OR REALISATION?  GP4's cosmic-shear window cells in one realisation at two resolutions, across
realisations, and the mock's cluster content.

WHY.  P34c re-scored GP4's two window cells in a 200 Mpc box at 512^3 and found both above the gate on the alternative
footing (1.207 and 1.251, against GP4's 1.145 and 1.190 at 256^3).  But GP3's builder draws its white noise and its halo
counts cell by cell, so a 512^3 box with GP4's seed is a DIFFERENT realisation, not GP4's box resolved better.  P34b's
100 Mpc box, at the same fine cell size, moved the kernel-alone ratio by at most 0.6%, against P34c's 2-4%.  How much of
P34c's rise is resolution and how much is the realisation has not been measured.  Every box also holds fewer cells with
a >= 1e14 Msun halo's bound baryons than the Sheth-Tormen expectation (P34c: 36 and 43 against 59).  Whether halos are
missing or share cells has not been measured either.  This lane measures all three.

MACHINERY (loaded unedited, as GP4, P34b and P34c load it): GP3's source up to its M1 banner -- phantom(), spectra(),
ratios(), PNL_of, GP0, and the 200 Mpc / 256^3 mock MK (seed 20260925, GP4's box), whose grid the coarse boxes use;
GP4's shear formula R(k) = T^2 + 2 r_x T s + s^2 with T from L364's committed values; the gate R <= 1.2 on k = 0.1-1,
both footings; MS3's census.  Written out below, each with a control:
  * build_counted(): GP3's build_mock() verbatim, plus tallies of the halos it draws (it deposits them and keeps no list).
  * THE PAIRED COARSE BOX: a 512^3 box's matter and bound-baryon densities averaged over 2x2x2 cells onto the 256^3 grid.
    This is the same realisation at GP4's resolution: mass is conserved, and each halo sits in the coarse cell that
    contains it, which is how GP3's builder deposits halos.
  * COMMON k BINS: GP3's spectra() bins k in 24 log bins from 2 pi/L to the box's own Nyquist, so a 512^3 box is binned
    differently from a 256^3 one.  The paired comparison bins both boxes with GP4's (the 256^3 grid's) edges.

PRE-DECLARED (before the run):
  C1  CONTROL: build_counted() reproduces GP3's own 200 Mpc / 256^3 mock MK bit for bit (rho_m and rhoB).
  C2  CONTROL: GP4's box (seed 20260925, 256^3) reproduces GP4's committed scores for its two window cells (1e-9).
  C3  CONTROL: the 512^3 box at seed 20260925, with its own bins, reproduces P34c's committed 512^3 scores (1e-9).
  C4  CONTROL: the paired coarse boxes conserve the fine boxes' matter and bound-baryon mass (1e-12, relative), and on
      every 256^3 box the common-bin spectra equal GP3's spectra() exactly.
  H1  RESOLUTION: at fixed realisation and common bins, going from 256^3 to 512^3 raises the worst R on the alternative
      footing by at least half of P34c's raise for that cell, for both cells, in both realisations (seeds 20260925 and
      20260931).  Recorded either way; if H1 fails, at least half of P34c's raise is the realisation or the binning.
  H2  REALISATIONS: both window cells pass (both footings) in each of eight 200 Mpc / 256^3 realisations of GP3's
      builder (GP4's seed and 20260932-20260938).  Recorded either way.
  H3  THE ENSEMBLE ESTIMATE: R(k) averaged over the eight realisations, plus the paired resolution shift averaged over
      the two realisations, passes for both cells on both footings.  Recorded either way.
  D1  (reported) for seed 20260925, P34c's rise split exactly into binning (the fine box's own bins against GP4's),
      resolution (fine against its paired coarse box) and realisation (the paired coarse box against GP4's box).
  D2  (reported) the mock's cluster content: halos drawn above 1e13.5 / 1e14 / 1e14.5 Msun against the builder's own
      expectation, the cells holding them, and the cells holding two or more; the spread of the worst R over the
      realisations.
  D3  (reported) the kernel-alone ratio's change from 256^3 to 512^3 at fixed realisation and common bins.
MUTATE=1: no free streaming (T = 1), GP4's own control -- H2 and H3 must then fail (rc = 1).  The controls always
score with T on.

Run from anywhere:  python3 real_research/paper34_audit_2026/P34d_resolution_or_realisation.py   (needs ~20 GB of memory)
"""
import os, sys, io, gc, json, math, time, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
GPD = os.path.join(REPO, "real_research", "generated_phantom_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "P34d", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, ok, measured, load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")


def banner(t):
    P("\n" + "=" * 118 + f"\n{t}\n" + "=" * 118)


def load(path, split, name):
    """exec a committed lane's machinery (everything before `split`), unedited, with its MUTATE forced off (GP4's loader)."""
    src = open(path).read().split(split)[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
    ns = {"__name__": name, "__file__": path}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src, ns)
    return ns


P(__doc__.strip().split("\n\n")[0])
if MUTATE:
    P("  *** MUTATE=1: no free streaming (T = 1); H2 and H3 must FAIL ***")

G3 = load(os.path.join(GPD, "GP3_lensing_power_and_growth.py"),
          "# ============================================================================================ M1 control", "gp3")
GP0, ZS, MK = G3["GP0"], G3["ZS"], G3["MK"]
GP4J = json.load(open(os.path.join(GPD, "GP4_generated_phantom_plus_kicked_carrier_results.json")))["numbers"]
L364 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L364_replacement_carrier_cosmic_shear_results.json")))["numbers"]
P34C = json.load(open(os.path.join(HERE, "P34c_gp4_window_fixed_volume_results.json")))["numbers"]
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
KG = (0.1, 0.2, 0.3, 0.5, 0.7, 1.0)
WINDOW = [(0.95, 1200.0), (0.9, 1400.0)]
CELLS = [f"{fd}|{vk:.0f}" for fd, vk in WINDOW]
T05 = {f"{r['fd']}|{r['vk']:.0f}": r["T05"] for r in L364["scan"]}
LMH = np.arange(10.0, 15.51, 0.05)
KB = np.geomspace(2 * np.pi / MK["L"] * 1.01, np.pi / MK["dx"], 24)      # GP4's bins: GP3's spectra() on the 256^3 grid
SEEDS256 = [20260925] + list(range(20260932, 20260939))
SEEDS512 = [20260925, 20260931]
LCUT = (13.5, 14.0, 14.5)


def build_counted(L, N, seed, reading="observed", RS=1.5):
    """GP3's build_mock(), verbatim (its module's dn, bh, DZ, ZS), plus tallies of the halos it draws above LCUT."""
    dn, bh, DZ = G3["dn"], G3["bh"], G3["DZ"]
    dx = L / N; rng = np.random.default_rng(seed)
    k1 = np.fft.fftfreq(N, d=dx) * 2 * np.pi; kz = np.fft.rfftfreq(N, d=dx) * 2 * np.pi
    KX, KY, KZ = np.meshgrid(k1, k1, kz, indexing="ij"); K2 = KX ** 2 + KY ** 2 + KZ ** 2
    Pk = GP0.Pk0(np.sqrt(K2)) * DZ ** 2; Pk[0, 0, 0] = 0
    dk = np.fft.rfftn(rng.standard_normal((N, N, N))) * np.sqrt(Pk / dx ** 3)
    dS = np.fft.irfftn(dk * np.exp(-K2 * RS ** 2 / 2), s=(N, N, N)); sS = dS.std()
    rho_m = GP0.RHO_M0 * np.exp(dS - sS ** 2 / 2)
    edges = np.arange(10.0, 15.6, 0.1); cen = 0.5 * (edges[1:] + edges[:-1]); Vc = dx ** 3
    rhoB = np.zeros((N, N, N))
    # ---- the tallies (no draws from rng; the builder's draw sequence is untouched)
    del dk; gc.collect()
    tally = {str(c): {"drawn": 0, "expected": 0.0} for c in LCUT}
    per_cell = {str(c): np.zeros((N, N, N), dtype=np.int32) for c in (14.0, 14.5)}
    for lc in cen:
        n = np.interp(lc, GP0.LM, dn) * 0.1 * math.log(10); b = np.interp(lc, GP0.LM, bh)
        cnt = rng.poisson(n * Vc * np.exp(b * dS - (b * sS) ** 2 / 2))
        rhoB += cnt * float(GP0.M_bound(10 ** lc, ZS, reading)) / Vc
        for c in LCUT:                                                   # bins lie wholly above c (centres 0.05 off)
            if lc > c:
                tally[str(c)]["drawn"] += int(cnt.sum()); tally[str(c)]["expected"] += float(n * L ** 3)
        for c in (14.0, 14.5):
            if lc > c:
                per_cell[str(c)] += cnt.astype(np.int32)
    for c in (14.0, 14.5):
        pc = per_cell[str(c)]
        tally[str(c)].update(cells_holding=int((pc >= 1).sum()), cells_holding_2plus=int((pc >= 2).sum()), max_in_one_cell=int(pc.max()))
    del per_cell, dS; gc.collect()
    return {"L": L, "N": N, "dx": dx, "KX": KX, "KY": KY, "KZ": KZ, "K2": K2, "rho_m": rho_m, "rhoB": rhoB, "sS": sS}, tally


def census(mk, L):
    """MS3's census, as P34c runs it: cells holding at least the bound baryons of a 1e{lM} halo, against Sheth-Tormen."""
    dn = G3["dn"]
    Vc = mk["dx"] ** 3; Vbox = L ** 3; out = {}
    for lM in (13.5, 14.0, 14.5):
        thr = float(GP0.M_bound(10 ** lM, ZS, "observed"))
        sel = LMH >= lM
        out[str(lM)] = {"cells_with_bound_baryons_above": int((mk["rhoB"] * Vc >= thr).sum()),
                        "expected_halos_above": float(np.trapz(np.interp(LMH[sel], GP0.LM, dn), LMH[sel] * math.log(10))) * Vbox}
    return out


def spectra_bins(mk, fields, kb):
    """GP3's spectra() with the bin edges passed in (GP3 derives them from the box's own Nyquist)."""
    N, dx = mk["N"], mk["dx"]
    K = np.sqrt(mk["K2"]).ravel(); wz = np.where(mk["KZ"].ravel() == 0, 1.0, 2.0)
    idx = np.digitize(K, kb)
    F = {n: np.fft.rfftn(d).ravel() for n, d in fields.items()}

    def pk(a, b):
        p = (F[a] * np.conj(F[b])).real * dx ** 3 / N ** 3
        out, kk = [], []
        for i in range(1, len(kb)):
            s = idx == i
            if s.any(): out.append(np.sum(p[s] * wz[s]) / np.sum(wz[s])); kk.append(np.sum(K[s] * wz[s]) / np.sum(wz[s]))
        return np.array(kk) / G3["h"], np.array(out)
    return pk


def pk_shear(pk):
    """P34c's shear_input() on a spectra closure: s^2 = P_ph/P_NL and r_x per bin, and GP3's kernel-alone ratio."""
    kh, Pmm = pk("m", "m"); _, Pxx = pk("m", "ph"); _, Ppp = pk("ph", "ph")
    Pnl = G3["PNL_of"](kh)
    s2 = Ppp / Pnl; rx = Pxx / np.sqrt(np.maximum(Pmm * Ppp, 1e-300))
    _, _, Rc, _ = G3["ratios"]({"kh": kh, "Pmm": Pmm, "Pxx": Pxx, "Ppp": Ppp})
    return {"kh": kh, "s2_bin": s2, "rx_bin": rx, "Rc": {q: float(np.interp(q, kh, Rc)) for q in KG}}


def measure_both(mk, a0):
    """GP3's measure() at lambda = 1 Mpc (its body: phantom(), then spectra()), scored with the box's own bins and GP4's."""
    rho_ph, gm, f = G3["phantom"](mk, 1.0, a0)
    del gm, f
    fields = {"m": mk["rho_m"] / GP0.RHO_M0 - 1, "ph": rho_ph / GP0.RHO_M0}
    del rho_ph; gc.collect()
    pk = G3["spectra"](mk, fields); own = pk_shear(pk); del pk; gc.collect()
    pk = spectra_bins(mk, fields, KB); com = pk_shear(pk); del pk, fields; gc.collect()
    return {"own": own, "common": com}


def shear_R(sh, cell, T_on):
    """GP4's formula (as P34b/P34c): R(k) = T^2 + 2 r_x T s + s^2 on the mock's bins, T interpolated in log k."""
    kh = sh["kh"]
    if T_on:
        lk = np.log([float(q) for q in KG]); Tv = np.array([T05[cell][str(q)] for q in KG])
        T = np.interp(np.log(kh), lk, Tv)
    else:
        T = np.ones_like(kh)
    sb = np.sqrt(np.maximum(sh["s2_bin"], 0.0))
    Rb = T * T + 2 * sh["rx_bin"] * T * sb + sb * sb
    return {q: float(np.interp(q, kh, Rb)) for q in KG}


SH = {}                                                  # (box, footing, bins) -> shear input
TAL, CEN = {}, {}
worst = lambda box, cell, f, bins="own", T_on=not MUTATE: max(shear_R(SH[(box, f, bins)], cell, T_on).values())

banner("C1  build_counted() AGAINST GP3's OWN MOCK")
mk0, TAL["s20260925"] = build_counted(200.0, 256, 20260925)
eq_m, eq_b = bool(np.array_equal(mk0["rho_m"], MK["rho_m"])), bool(np.array_equal(mk0["rhoB"], MK["rhoB"]))
del mk0; gc.collect()
check("C1 CONTROL: build_counted() reproduces GP3's own 200 Mpc / 256^3 mock MK bit for bit (rho_m and rhoB)", eq_m and eq_b,
      f"rho_m identical {eq_m}; rhoB identical {eq_b}")

banner("R  EIGHT REALISATIONS AT GP4's RESOLUTION (GP3's builder, 200 Mpc / 256^3, lambda = 1 Mpc)")
for sd in SEEDS256:
    box = f"s{sd}"
    if sd == 20260925:
        mk = MK
    else:
        mk, TAL[box] = build_counted(200.0, 256, sd)
    CEN[box] = census(mk, 200.0)
    for f in A0:
        m = measure_both(mk, A0[f]); SH[(box, f, "own")], SH[(box, f, "common")] = m["own"], m["common"]
    if mk is not MK:
        del mk
    gc.collect()
    t = TAL[box]["14.0"]
    P(f"    seed {sd}: " + "; ".join(f"({c}) worst R {worst(box, c, 'canonical'):.3f} / {worst(box, c, 'alt'):.3f}" for c in CELLS) +
      f"; halos >= 1e14 drawn {t['drawn']} (expected {t['expected']:.1f}) in {t['cells_holding']} cells   [{time.time() - T0:.0f}s]")

banner("P  ONE REALISATION AT TWO RESOLUTIONS: 512^3 boxes and their 2x2x2-averaged 256^3 twins on GP4's grid")
cons, n = 0.0, MK["N"]
for sd in SEEDS512:
    fb, cb = f"f{sd}", f"c{sd}"
    mkf, TAL[fb] = build_counted(200.0, 512, sd)
    mkc = {k: MK[k] for k in ("L", "N", "dx", "KX", "KY", "KZ", "K2")}
    for key in ("rho_m", "rhoB"):
        mkc[key] = mkf[key].reshape(n, 2, n, 2, n, 2).mean(axis=(1, 3, 5))
        cons = max(cons, abs(8.0 * mkc[key].sum() / mkf[key].sum() - 1))
    mkc["sS"] = float("nan")
    CEN[fb], CEN[cb] = census(mkf, 200.0), census(mkc, 200.0)
    for f in A0:
        m = measure_both(mkf, A0[f]); SH[(fb, f, "own")], SH[(fb, f, "common")] = m["own"], m["common"]
        P(f"    seed {sd}, 512^3, {f} measured   [{time.time() - T0:.0f}s]")
    del mkf; gc.collect()
    for f in A0:
        m = measure_both(mkc, A0[f]); SH[(cb, f, "own")], SH[(cb, f, "common")] = m["own"], m["common"]
    del mkc; gc.collect()
    t = TAL[fb]["14.0"]
    for c in CELLS:
        P(f"    seed {sd} ({c}), alt: 512^3 own bins {worst(fb, c, 'alt'):.3f}, 512^3 GP4's bins {worst(fb, c, 'alt', 'common'):.3f}, "
          f"paired 256^3 {worst(cb, c, 'alt'):.3f}; canonical {worst(fb, c, 'canonical'):.3f} / {worst(fb, c, 'canonical', 'common'):.3f} / "
          f"{worst(cb, c, 'canonical'):.3f}")
    P(f"    seed {sd}: halos >= 1e14 drawn {t['drawn']} (expected {t['expected']:.1f}); cells holding them 512^3 {t['cells_holding']}, "
      f"census 512^3 {CEN[fb]['14.0']['cells_with_bound_baryons_above']}, paired 256^3 {CEN[cb]['14.0']['cells_with_bound_baryons_above']}   [{time.time() - T0:.0f}s]")

banner("CONTROLS")
dev2 = 0.0
for fd, vk in WINDOW:
    c = f"{fd}|{vk:.0f}"
    row = [r for r in GP4J["scan"] if r["lam"] == 1.0 and r["fd"] == fd and r["vk"] == vk][0]
    for f in A0:
        dev2 = max(dev2, abs(worst("s20260925", c, f, T_on=True) - row["shear"][f]))
check("C2 CONTROL: GP4's box (seed 20260925, 256^3) reproduces GP4's committed scores for its two window cells (1e-9)", dev2 < 1e-9, f"max |diff| = {dev2:.1e}")
dev3 = max(abs(worst("f20260925", c, f, T_on=True) - P34C["window"][f"{c}|200/512"][f]) for c in CELLS for f in A0)
check("C3 CONTROL: the 512^3 box at seed 20260925, with its own bins, reproduces P34c's committed 512^3 scores (1e-9)", dev3 < 1e-9, f"max |diff| = {dev3:.1e}")
b256 = [b for b in {k[0] for k in SH} if not b.startswith("f")]
dev4 = max(float(np.max(np.abs(SH[(b, f, "own")][q] - SH[(b, f, "common")][q]))) if SH[(b, f, "own")][q].shape == SH[(b, f, "common")][q].shape else np.inf
           for b in b256 for f in A0 for q in ("kh", "s2_bin", "rx_bin"))
check("C4 CONTROL: the paired coarse boxes conserve mass (1e-12, relative); on every 256^3 box GP4's-bin spectra equal GP3's spectra()",
      cons < 1e-12 and dev4 == 0.0, f"mass: max relative {cons:.1e}; spectra: max |diff| {dev4:.1e} over {len(b256)} boxes")

banner("H1  RESOLUTION AT FIXED REALISATION (GP4's bins, alternative footing)")
H1 = {}
for sd in SEEDS512:
    for c in CELLS:
        need = 0.5 * (P34C["window"][f"{c}|200/512"]["alt"] - P34C["window"][f"{c}|200/256"]["alt"])
        got = worst(f"f{sd}", c, "alt", "common") - worst(f"c{sd}", c, "alt")
        H1[f"{sd}|{c}"] = {"shift": got, "half_P34c": need}
        P(f"    seed {sd} ({c}): 512^3 - paired 256^3 = {got:+.4f}   (half of P34c's raise: {need:.4f})")
OUT["numbers"]["H1"] = H1
check("H1 RESOLUTION: at fixed realisation and common bins, 256^3 -> 512^3 raises the worst R (alt) by at least half of "
      "P34c's raise, both cells, both realisations", all(v["shift"] >= v["half_P34c"] for v in H1.values()),
      {k: round(v["shift"], 4) for k, v in H1.items()})

banner("H2  THE WINDOW ACROSS EIGHT REALISATIONS AT GP4's RESOLUTION")
W = {c: {f: [worst(f"s{sd}", c, f) for sd in SEEDS256] for f in A0} for c in CELLS}
npass = sum(all(W[c][f][i] <= 1.2 for c in CELLS for f in A0) for i in range(len(SEEDS256)))
for c in CELLS:
    for f in A0:
        v = np.array(W[c][f])
        P(f"    ({c}) {f:9s}: worst R over seeds mean {v.mean():.3f}, sd {v.std(ddof=1):.3f}, range {v.min():.3f}-{v.max():.3f}; "
          f"passes in {(v <= 1.2).sum()}/{len(v)}")
OUT["numbers"]["H2"] = {"worst": W, "seeds": SEEDS256, "realisations_passing_everything": int(npass)}
check("H2 REALISATIONS: both window cells pass (both footings) in each of the eight 256^3 realisations", npass == len(SEEDS256),
      f"{npass}/{len(SEEDS256)} realisations pass for both cells on both footings")

banner("H3  THE ENSEMBLE ESTIMATE: the eight-realisation mean R(k) plus the paired resolution shift")
H3 = {}
for c in CELLS:
    for f in A0:
        mean = {q: float(np.mean([shear_R(SH[(f"s{sd}", f, "own")], c, not MUTATE)[q] for sd in SEEDS256])) for q in KG}
        dres = {q: float(np.mean([shear_R(SH[(f"f{sd}", f, "common")], c, not MUTATE)[q] - shear_R(SH[(f"c{sd}", f, "own")], c, not MUTATE)[q]
                                  for sd in SEEDS512])) for q in KG}
        est = {q: mean[q] + dres[q] for q in KG}
        H3[f"{c}|{f}"] = {"mean_256": mean, "resolution_shift": dres, "estimate": est, "worst_estimate": max(est.values()),
                          "worst_mean_256": max(mean.values())}
        P(f"    ({c}) {f:9s}: worst of the mean {max(mean.values()):.3f}; with the resolution shift {max(est.values()):.3f} "
          f"(shift at k = 1: {dres[1.0]:+.3f})")
OUT["numbers"]["H3"] = H3
check("H3 THE ENSEMBLE ESTIMATE passes for both cells on both footings", all(v["worst_estimate"] <= 1.2 for v in H3.values()),
      {k: round(v["worst_estimate"], 3) for k, v in H3.items()})

banner("D1-D3  (reported) P34c's RISE SPLIT, THE CLUSTER CONTENT, THE KERNEL-ALONE RATIO")
D1 = {}
for c in CELLS:
    for f in A0:
        a, b_, cc, d = (worst("s20260925", c, f), worst("c20260925", c, f), worst("f20260925", c, f, "common"), worst("f20260925", c, f))
        D1[f"{c}|{f}"] = {"GP4_box": a, "paired_coarse": b_, "fine_common": cc, "fine_own": d,
                          "realisation": b_ - a, "resolution": cc - b_, "binning": d - cc, "total": d - a}
        P(f"    seed 20260925 ({c}) {f:9s}: total {d - a:+.4f} = realisation {b_ - a:+.4f} + resolution {cc - b_:+.4f} + binning {d - cc:+.4f}")
OUT["numbers"]["D1"] = D1
check("D1 (reported) P34c's rise split into realisation, resolution and binning (seed 20260925)", True,
      {k: (round(v["realisation"], 4), round(v["resolution"], 4), round(v["binning"], 4)) for k, v in D1.items() if k.endswith("alt")}, load_bearing=False)
for box in sorted(TAL):
    t = TAL[box]
    P(f"    {box:10s}: " + "; ".join(f">= 1e{c}: drawn {t[c]['drawn']} vs expected {t[c]['expected']:.1f}" +
                                   (f", in {t[c]['cells_holding']} cells ({t[c]['cells_holding_2plus']} with 2+, max {t[c]['max_in_one_cell']})" if "cells_holding" in t[c] else "")
                                   for c in ("13.5", "14.0", "14.5")))
OUT["numbers"]["tally"] = TAL
OUT["numbers"]["census"] = CEN
dr14 = [TAL[b]["14.0"]["drawn"] / TAL[b]["14.0"]["expected"] for b in TAL]
sh14 = [1 - TAL[b]["14.0"]["cells_holding"] / max(TAL[b]["14.0"]["drawn"], 1) for b in TAL]
check("D2 (reported) the mock's >= 1e14 halos: drawn / expected, and the share of drawn halos lost to shared cells", True,
      f"drawn/expected {min(dr14):.2f}-{max(dr14):.2f}; shared-cell loss {min(sh14):.2f}-{max(sh14):.2f} over {len(TAL)} boxes", load_bearing=False)
D3 = {}
for sd in SEEDS512:
    for f in A0:
        D3[f"{sd}|{f}"] = {q: SH[(f"f{sd}", f, "common")]["Rc"][q] / SH[(f"c{sd}", f, "own")]["Rc"][q] - 1 for q in (0.3, 0.5, 0.7, 1.0)}
        P(f"    seed {sd} {f:9s}: kernel-alone ratio 512^3 / paired 256^3 - 1 at k 0.3/0.5/0.7/1: " +
          " / ".join(f"{D3[f'{sd}|{f}'][q]:+.3f}" for q in (0.3, 0.5, 0.7, 1.0)))
OUT["numbers"]["D3"] = D3
check("D3 (reported) the kernel-alone ratio's change 256^3 -> 512^3 at fixed realisation, common bins, k = 0.5-1", True,
      f"{min(v[q] for v in D3.values() for q in (0.5, 0.7, 1.0)):+.3f} to {max(v[q] for v in D3.values() for q in (0.5, 0.7, 1.0)):+.3f}", load_bearing=False)

banner("VERDICT")
nlb = sum(1 for _, ok, lb in CH if lb and not ok)
P(f"  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {nlb}   [{time.time() - T0:.0f}s]")
fn = os.path.join(HERE, "P34d_resolution_or_realisation_results" + ("_MUTATE" if MUTATE else "") + ".json")
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"  wrote {os.path.basename(fn)}")
sys.exit(1 if nlb else 0)
