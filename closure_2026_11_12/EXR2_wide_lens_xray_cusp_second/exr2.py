#!/usr/bin/env python3
"""EXR2 (WIDE-LENS X-RAY CUSP, SECOND MEASUREMENT).  Frozen criteria: FROZEN_CRITERIA.md (commit 512015c599).

Does eRASS1 see the X-rays that ESZ1's r^-2 gas cusp must emit?  Not a blind re-grade of EXR1 (see the criteria).
Reads the answers that exr2_fetch.py stored; sends nothing.

  python3 -I exr2.py --data-dir <ECLIPSE csv dir> --cache-dir <fetch cache> --atomdb <AtomDB 3.1.3 dir>
  EXR2_MUTATE=inject python3 -I exr2.py ...     (must exit 1)
  EXR2_MUTATE=shift  python3 -I exr2.py ...     (must exit 1)
  EXR2_MUTATE=newton python3 -I exr2.py ...     (must exit 1)
"""
import argparse, csv, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "ESZ1_wide_lens_gas_pressure"))
import esz1 as Z
import exr2_fetch as FT
E, L8 = Z.E, Z.L8
MUT = (os.environ.get("EXR2_MUTATE", "") or "").strip()
if MUT == "newton": E.FOOT = {k: 1.0e-30 for k in E.FOOT}
G, MSUN, KPC, MP, KEV, MU, MUE = Z.G, Z.MSUN, Z.KPC, Z.MP, Z.KEV, Z.MU, Z.MUE
XH = 2.0 / MUE - 1.0
SUL = -math.log(1.0 - 0.99865)                 # count limit for zero counts at the one-sided 3 sigma level
APF, TRANS = 0.80, 0.40
KERG = 1.602176634e-9                           # erg per keV
NBOOT, NL = 2000, 400
ZMET = (0.0, 0.3)
K_PRE = {"022": 8.1534e-12, "024": 8.2439e-12}
U = 1.0e-15
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)

# ---------------------------------------------------------------- service answers
def load_ul(cache, name, n):
    lim = json.load(open(os.path.join(cache, name)))["limits"]
    if len(lim) != n: sys.exit("%s: %d answers for %d look-ups" % (name, len(lim), n))
    g = lambda k: np.array([float(x[k]) if x.get(k) is not None else np.nan for x in lim])
    return dict(cnt=g("Count"), bkg=g("Bkg_counts"), exp=g("Exposure"), ulb=g("UL_B"), flag=g("Flag_pos"),
                de=np.array([bool(x.get("de_sky")) for x in lim]), ra=g("ra"), dec=g("dec"))
def usable(d):
    return d["de"] & (d["flag"] == 0) & (d["exp"] > 0) & np.isfinite(d["cnt"]) & np.isfinite(d["bkg"])
def values(d, n):
    """per target: value (rate, target minus the mean of its usable offsets), validity, exposure, the 8 null values."""
    use = usable(d).reshape(n, 9)
    with np.errstate(invalid="ignore", divide="ignore"): r = ((d["cnt"] - d["bkg"]) / d["exp"]).reshape(n, 9)
    T = d["exp"].reshape(n, 9)[:, 0]
    uo = use[:, 1:]; no = uo.sum(1); ro = np.where(uo, r[:, 1:], 0.0); tot = ro.sum(1)
    valid = use[:, 0] & (no >= 6)
    with np.errstate(invalid="ignore", divide="ignore"):
        v = np.where(valid, r[:, 0] - tot / np.maximum(no, 1), np.nan)
        nul = np.full((n, 8), np.nan)
        for k in range(8): nul[:, k] = np.where(valid & uo[:, k], r[:, 1 + k] - (tot - ro[:, k]) / np.maximum(no - 1, 1), np.nan)
        off_mean = np.where(valid, tot / np.maximum(no, 1), np.nan)
    return v, valid, T, nul, off_mean
def wstack(v, T, nul, weighted=True):
    v = np.asarray(v, float); keep = np.isfinite(v); v = v[keep]; nul = np.asarray(nul, float)[keep]
    T = np.asarray(T, float)[keep] if weighted else np.ones(len(v)); N = len(v)
    if N == 0: return dict(N=0, mean=float("nan"), sigma=float("nan"), sig_boot=float("nan"), sig_null=float("nan"), nulls=[])
    rng = np.random.default_rng(E.SEED); idx = rng.integers(0, N, (NBOOT, N))
    bs = (T[idx] * v[idx]).sum(1) / T[idx].sum(1); ns = []
    for k in range(nul.shape[1]):
        ok = np.isfinite(nul[:, k]); ns.append(float((T[ok] * nul[ok, k]).sum() / T[ok].sum()) if ok.any() else float("nan"))
    sb, sn = float(bs.std()), float(np.sqrt(np.nanmean(np.array(ns) ** 2)))
    return dict(N=N, mean=float((T * v).sum() / T.sum()), sigma=max(sb, sn), sig_boot=sb, sig_null=sn, nulls=ns)
def wmean(x, T, keep, weighted=True):
    x, T = np.asarray(x, float)[keep], (np.asarray(T, float)[keep] if weighted else np.ones(int(np.sum(keep))))
    return float((T * x).sum() / T.sum()) if len(x) else float("nan")

# ---------------------------------------------------------------- plasma
def apec(atomdb_dir):
    os.environ["ATOMDB"] = os.path.abspath(atomdb_dir)
    import pyatomdb
    sess = pyatomdb.spectrum.CIESession(); eb = np.geomspace(0.05, 20.0, 3001); sess.set_response(eb, raw=True)
    emid = np.sqrt(eb[1:] * eb[:-1]); KT = np.geomspace(0.03, 5.0, 60); S = np.zeros((len(ZMET), len(KT), len(emid)))
    def spec(kT, Zm):
        sess.set_abund(list(range(3, 31)), Zm); return np.asarray(sess.return_spectrum(kT), float) * emid * KERG   # erg cm^3/s per bin
    for iz, Zm in enumerate(ZMET):
        for j, kT in enumerate(KT): S[iz, j] = spec(float(kT), Zm)
    return dict(eb=eb, KT=KT, S=S, spec=spec, version=pyatomdb.__version__)
def band_w(eb, lo, hi):
    return np.clip((np.minimum(eb[1:], hi) - np.maximum(eb[:-1], lo)) / (eb[1:] - eb[:-1]), 0.0, 1.0)
def lam_of(A, z):
    """band emissivity table (metallicity x temperature) for the rest band of a lens at redshift z."""
    return A["S"] @ band_w(A["eb"], 0.6 * (1.0 + z), 2.3 * (1.0 + z))
def lam_interp(kT, KT, tab):
    out = np.exp(np.interp(np.log(np.maximum(kT, 1e-12)), np.log(KT), np.log(np.maximum(tab, 1e-300))))
    return np.where(kT < KT[0], 0.0, out)

# ---------------------------------------------------------------- the cusp
class Cusp:
    def __init__(self, rows):
        _, self.z, self.RE, self.Re, self.n, lm = E.build(rows); self.Ms = 10.0 ** lm * MSUN; self.N = len(rows)
        self.DA, self.DL = E.EUCLID.DA(self.z), E.EUCLID.DL(self.z)
        self.eng = Z.engines(self.RE, self.Re, self.n, self.Ms); self.r = Z.grid(300.0)[0]
        self.gs0 = G * self.Ms[:, None] * E.M3D_frac(self.r[None, :], self.Re[:, None], self.n[:, None]) / self.r[None, :] ** 2
    def solve(self, a0, case, bs):
        """gas mass (kg), kT(r) in keV on the grid, electron density at R_E (cm^-3)."""
        Mt = math.pi * self.RE ** 2 * E.EUCLID.sigcr(self.z, L8.zs_case(self.z, case))
        Mg = Z.solve_gas("G2", self.RE, self.Re, self.n, self.Ms, Mt, 10.0 ** bs, a0, self.eng)
        Menc, rho = Z.gas_body("G2", Mg, self.r)
        Pr = Z.pressure(self.r, rho, E.g_law(10.0 ** bs * self.gs0 + G * Menc / self.r[None, :] ** 2, a0, "S"))
        with np.errstate(invalid="ignore", divide="ignore"): kT = np.where(rho > 0, MU * MP * Pr / np.maximum(rho, 1e-300), 0.0) / KEV
        return Mg, kT, Z.gas_density_at("G2", Mg, self.RE) / (MUE * MP) * 1.0e-6
    def lum(self, Mg, kT, lamfun, rin_fac=1.0):
        """band luminosity (erg/s) of the gas between rin_fac R_E and min(300 kpc, 15 arcsec), per lens."""
        rin = rin_fac * self.RE; rout = np.minimum(Z.RT, 15.0 * E.ARCSEC * self.DA); L = np.zeros(self.N); u = np.linspace(0.0, 1.0, NL)
        for i in range(self.N):
            if Mg[i] <= 0 or rout[i] <= rin[i]: continue
            rl = rin[i] * (rout[i] / rin[i]) ** u
            ne = Mg[i] / (4.0 * math.pi * Z.RT * rl ** 2) / (MUE * MP) * 1.0e-6
            kTl = np.exp(np.interp(np.log(rl), np.log(self.r), np.log(np.maximum(kT[i], 1e-12))))
            f = XH * MUE * ne ** 2 * lamfun(i, kTl) * 4.0 * math.pi * (rl * 100.0) ** 3
            L[i] = Z.TRAPZ(f, np.log(rl))
        return L
    def flux(self, L):
        return APF * TRANS * L / (4.0 * math.pi * (self.DL * 100.0) ** 2)

def fam_word(meas, sig, pred):
    if not (np.isfinite(meas) and np.isfinite(sig) and np.isfinite(pred)) or pred < 3.0 * sig: return "NO POWER"
    return "EXCLUDED" if meas + 2.0 * sig < pred else "ALLOWED"
def lane_word(w0, w3, N, ok):
    if not ok or N < 100: return "NOT EVALUABLE"
    if w0 == "EXCLUDED": return "CUSP EXCLUDED"
    if w3 == "EXCLUDED": return "CUSP EXCLUDED UNLESS METAL-FREE"
    if w3 == "ALLOWED": return "CUSP NOT EXCLUDED"
    return "NO VERDICT"

# ================================================================== main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True); ap.add_argument("--cache-dir", required=True); ap.add_argument("--atomdb", required=True)
    a = ap.parse_args(); tag = "exr2" + ("_MUTATE_" + MUT if MUT else "")
    P("EXR2 (WIDE-LENS X-RAY CUSP, SECOND MEASUREMENT)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    RES = dict(lane="EXR2", criteria_commit="512015c599", mutate=MUT, footings=E.FOOT, not_blind=True); CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok)); P("  %s %-3s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))

    # ---------------------------------------------------------------- samples and answers
    P("\n[data]")
    rows, _ = E.load(a.data_dir); OUT.extend(E.OUT); E.OUT.clear()
    S, _ = E.select(rows, ("A", "B")); byid = {r["id"]: r for r in S}
    T = FT.targets(a.data_dir); POS = FT.positions(T); nT = len(T)
    iW = np.array([i for i, t in enumerate(T) if t["cls"] == "W"]); iC = np.array([i for i, t in enumerate(T) if t["cls"] == "C"])
    Wrows = [byid[T[i]["id"]] for i in iW]; NW = len(iW)
    P("  targets: W %d (ESZ1's wide lenses), C %d (ESZ1's controls); positions %d" % (NW, len(iC), len(POS)))
    D = {b: load_ul(a.cache_dir, "ul_dr1_%s.json" % b, len(POS)) for b in ("022", "024")}
    for b in D:
        if not (np.allclose(D[b]["ra"], [p["ra"] for p in POS], atol=1e-7) and np.allclose(D[b]["dec"], [p["dec"] for p in POS], atol=1e-7)):
            sys.exit("answers of band %s do not match the positions" % b)
    D2 = load_ul(a.cache_dir, "ul_dr2_024.json", NW)
    K2S = json.load(open(os.path.join(a.cache_dir, "k2_sources.json"))); DK = load_ul(a.cache_dir, "ul_k2_024.json", 2 * len(K2S))

    # ---------------------------------------------------------------- instrument checks
    P("\n[instrument checks]")
    KB = {}; k1 = []
    for b in ("022", "024"):
        pools = [D[b]] + ([DK] if b == "024" else [])
        x = np.concatenate([(d["ulb"] * d["exp"])[usable(d) & (d["cnt"] == 0)] for d in pools]); KB[b] = float(np.median(x))
        k1.append((len(x), float(np.max(np.abs(x / KB[b] - 1.0))), abs(KB[b] / K_PRE[b] - 1.0)))
    ecf = SUL / KB["024"] / 0.75
    ck("K1", "UL_B x Exposure at zero counts constant to 0.5 % (N >= 50 per band), equal to the values met before freezing, ECF(024) within 3 % of 1.074e12",
       "022: N %d, spread %.1e, K %.4e; 024: N %d, spread %.1e, K %.4e; ECF(024) %.4e" % (k1[0][0], k1[0][1], KB["022"], k1[1][0], k1[1][1], KB["024"], ecf),
       all(c[0] >= 50 and c[1] < 0.005 and c[2] < 0.005 for c in k1) and abs(ecf / 1.074e12 - 1.0) < 0.03)
    Q = {b: SUL / KB[b] for b in KB}                       # counts/s per (erg/s/cm^2), EEF included
    nk = len(K2S); cf = np.array([s["ml_flux_1"] for s in K2S])
    def k2ratio(sl):
        d = {k: v[sl] for k, v in DK.items()}; ok = usable(d)
        return np.where(ok, (d["cnt"] - d["bkg"]) / d["exp"] / Q["024"] / cf, np.nan)
    rt, rs = k2ratio(slice(0, nk)), k2ratio(slice(nk, 2 * nk))
    if MUT == "shift": rt = rs
    mt, ms_ = float(np.nanmedian(rt)) if nk else float("nan"), float(np.nanmedian(rs)) if nk else float("nan")
    ck("K2", "catalogued point sources (ml_flux_1 1e-13 to 1e-12): median aperture flux / catalogue flux in 0.75-1.25 (N >= 20); below 0.2 when moved 0.1 deg",
       "N = %d, median ratio %.3f; moved: %.3f" % (int(np.isfinite(rt).sum()), mt, ms_), np.isfinite(rt).sum() >= 20 and 0.75 <= mt <= 1.25 and ms_ < 0.2)
    A = apec(a.atomdb)
    s1 = A["spec"](1.0, 0.0); ff = 1.4e-27 * math.sqrt(1.0 * KERG / 1.380649e-16) * 1.2 * 1.4
    bw = band_w(A["eb"], 0.87, 3.34); r43 = float((A["spec"](0.45, 0.3) @ bw) / (A["spec"](0.45, 0.0) @ bw))
    ck("K4", "pyatomdb %s: Lambda(1 keV, Z = 0) within 30 %% of the free-free estimate; rest 0.87-3.34 keV at 0.45 keV, Z 0.3 / Z 0 > 2" % A["version"],
       "%.3e against %.3e; ratio %.2f" % (s1.sum(), ff, r43), abs(s1.sum() / ff - 1.0) < 0.30 and r43 > 2.0)
    CU = Cusp(Wrows); SOL = {}
    for nm, a0 in E.FOOT.items():
        for key, case, bs in (("least", "far", 0.10), ("salpeter", "far", 0.0), ("central", "central", 0.0)): SOL[(nm, key)] = CU.solve(a0, case, bs)
    if not MUT:
        ref = json.load(open(os.path.join(HERE, "..", "ESZ1_wide_lens_gas_pressure", "esz1_results.json")))["model"]; e5 = []
        for nm in E.FOOT:
            Mg, _, ne = SOL[(nm, "least")]; rr = ref["%s|G2|far|+0.10" % nm]
            e5 += [abs(float(np.median(Mg / MSUN)) / rr["Mg_med"] - 1.0), abs(float(np.nanmedian(np.where(Mg > 0, ne, np.nan))) / rr["ne_med"] - 1.0)]
        ck("K5", "ESZ1 reproduced: median r^-2 gas mass and n_e at R_E, least setting, both footings (1e-6)", "largest deviation %.1e" % max(e5), max(e5) < 1.0e-6)
    Mg6 = SOL[(list(E.FOOT)[0], "least")][0]; L6 = CU.lum(Mg6, np.full((CU.N, len(CU.r)), 1.0), lambda i, kT: np.full(kT.shape, 1.0e-23))
    rout = np.minimum(Z.RT, 15.0 * E.ARCSEC * CU.DA) * 100.0; REc = CU.RE * 100.0; nE = Mg6 / (4.0 * math.pi * Z.RT * CU.RE ** 2) / (MUE * MP) * 1.0e-6
    ana = np.where((Mg6 > 0) & (rout > REc), 1.0e-23 * XH * MUE * nE ** 2 * 4.0 * math.pi * REc ** 4 * (1.0 / REc - 1.0 / rout), 0.0)
    e6 = float(np.max(np.abs(L6[ana > 0] / ana[ana > 0] - 1.0)))
    ck("K6", "luminosity integral for a constant emissivity against the closed form (1e-3)", "%.1e" % e6, e6 < 1.0e-3)

    # ---------------------------------------------------------------- predictions
    P("\n[model: ESZ1's r^-2 gas, least hydrostatic temperature, APEC, gas outside R_E and inside 15 arcsec, x %.2f x %.2f]" % (APF, TRANS))
    LAM = [lam_of(A, z) for z in CU.z]
    def lamfun(iz): return lambda i, kT: lam_interp(kT, A["KT"], LAM[i][iz])
    F, INFO = {}, {}
    for nm in E.FOOT:
        for key in ("least", "salpeter", "central"):
            Mg, kT, ne = SOL[(nm, key)]
            for iz, Zm in enumerate(ZMET):
                L = CU.lum(Mg, kT, lamfun(iz)); F[(nm, key, Zm)] = CU.flux(L)
                if key == "least":
                    F[(nm, "rin2", Zm)] = CU.flux(CU.lum(Mg, kT, lamfun(iz), 2.0))
                    j = np.array([int(np.argmin(np.abs(CU.r - x))) for x in CU.RE])
                    INFO[(nm, Zm)] = dict(Mg_med=float(np.median(Mg / MSUN)), frac_zero=float(np.mean(Mg <= 0)), ne_med=float(np.nanmedian(np.where(Mg > 0, ne, np.nan))),
                                          kT_RE_med=float(np.nanmedian(np.where(Mg > 0, kT[np.arange(CU.N), j], np.nan))), L_med=float(np.median(L)), L_mean=float(np.mean(L)),
                                          F_med=float(np.median(F[(nm, key, Zm)])), F_mean=float(np.mean(F[(nm, key, Zm)])))
    for nm in E.FOOT:
        i0 = INFO[(nm, 0.0)]
        P("  %-9s least setting: median gas mass %.2e Msun (%.0f %% of lenses need none), n_e(R_E) %.2f cm^-3, kT(R_E) %.2f keV" % (nm, i0["Mg_med"], 100 * i0["frac_zero"], i0["ne_med"], i0["kT_RE_med"]))
        for Zm in ZMET:
            i = INFO[(nm, Zm)]
            P("            Z = %.1f: band luminosity outside R_E median %.2e, mean %.2e erg/s; predicted flux median %.1f, mean %.1f (1e-15 erg/s/cm^2)" % (Zm, i["L_med"], i["L_mean"], i["F_med"] / U, i["F_mean"] / U))
    RES["model"] = {"%s|Z%.1f" % k: v for k, v in INFO.items()}

    # ---------------------------------------------------------------- measurement
    P("\n[measurement: net rate at the target minus the mean of its usable offsets; flux = rate x K / %.4f; 1e-15 erg/s/cm^2]" % SUL)
    V = {}
    for b in ("022", "024"):
        v, valid, Tx, nul, off = values(D[b], nT); V[b] = dict(f=v / Q[b], valid=valid, T=Tx, nul=nul / Q[b], off=off / Q[b])
    if MUT == "inject":
        inj = F[("canonical", "least", 0.0)]
        for b in V: V[b]["f"][iW] = V[b]["f"][iW] + inj
        P("  [MUTATE inject] each W lens's Z = 0 canonical prediction added to its value, both bands")
    for b in ("022", "024"):
        d = D[b]; t9 = lambda x: x.reshape(nT, 9)
        P("  band %s: valid W %d of %d, valid C %d of %d; W medians: exposure %.0f s, background %.2f counts; total counts at W targets %d"
          % (b, V[b]["valid"][iW].sum(), NW, V[b]["valid"][iC].sum(), len(iC), np.median(V[b]["T"][iW]), np.nanmedian(t9(d["bkg"])[iW, 0]), int(np.nansum(t9(d["cnt"])[iW, 0]))))
    def st(b, sel, weighted=True): return wstack(V[b]["f"][sel], V[b]["T"][sel], V[b]["nul"][sel], weighted)
    sW = st("022", iW)
    P("  W, band 022: N = %d, stack %+.3f, sigma %.3f (bootstrap %.3f, null stacks %.3f)" % (sW["N"], sW["mean"] / U, sW["sigma"] / U, sW["sig_boot"] / U, sW["sig_null"] / U))
    ns = np.array(sW["nulls"]); k3 = bool(np.nanmax(np.abs(ns)) <= 3.5 * sW["sigma"])
    ck("K3", "none of the 8 null stacks of W beyond 3.5 sigma", "largest %.3f against sigma %.3f (1e-15)" % (np.nanmax(np.abs(ns)) / U, sW["sigma"] / U), k3)
    RES["checks"] = CK; need = ["K1", "K2", "K3", "K4", "K6"] + ([] if MUT else ["K5"])
    allok = all(k in CK and CK[k]["ok"] for k in need)

    # ---------------------------------------------------------------- Part G
    P("\n[Part G: least demanding setting (far source, stars +0.10 dex); 1e-15 erg/s/cm^2]")
    def part_g(b, sub, key="least", scale=1.0, weighted=True, show=False):
        """sub: boolean mask over the W lenses."""
        sel = iW[sub]; s = st(b, sel, weighted); keep = np.isfinite(V[b]["f"][sel]); out = dict(N=s["N"], meas=s["mean"], sigma=s["sigma"], fam={}, word={})
        for nm in E.FOOT:
            w = {}
            for Zm in ZMET:
                pr = scale * wmean(F[(nm, key, Zm)][sub], V[b]["T"][sel], keep, weighted); w[Zm] = fam_word(s["mean"], s["sigma"], pr)
                frac = (s["mean"] + 2.0 * s["sigma"]) / pr if pr > 0 else float("nan")
                out["fam"]["%s|Z%.1f" % (nm, Zm)] = dict(pred=pr, word=w[Zm], upper_over_pred=frac, mass_share=math.sqrt(frac) if frac > 0 else 0.0,
                                                         z_excl=(pr - s["mean"]) / s["sigma"] if s["sigma"] > 0 else float("nan"))
                if show: P("    %-9s Z = %.1f  pred %8.2f   measured %+6.2f +- %.2f   (pred - meas) / sigma = %6.1f   (meas + 2 sigma) / pred = %.3f   gas share allowed %.0f %%   -> %s"
                           % (nm, Zm, pr / U, s["mean"] / U, s["sigma"] / U, out["fam"]["%s|Z%.1f" % (nm, Zm)]["z_excl"], frac, 100 * out["fam"]["%s|Z%.1f" % (nm, Zm)]["mass_share"], w[Zm]))
            out["word"][nm] = lane_word(w[0.0], w[0.3], s["N"], allok)
        return out
    allW = np.ones(NW, bool); gA = np.array([r["grade"] == "A" for r in Wrows]); zlo = CU.z <= 0.6
    G0 = part_g("022", allW, show=True)
    BR = {"band 024 (0.2-2.3 keV)": part_g("024", allW, scale=KB["024"] / KB["022"]), "inner radius 2 R_E": part_g("022", allW, key="rin2"),
          "transmission 0.25": part_g("022", allW, scale=0.25 / TRANS), "unweighted mean": part_g("022", allW, weighted=False),
          "grade A only": part_g("022", gA), "z_l <= 0.6 only": part_g("022", zlo)}
    P("  brackets (measured +- sigma; pred Z = 0 and Z = 0.3, canonical; lane word per footing):")
    for k, bkt in BR.items():
        P("    %-24s N = %3d  %+6.2f +- %.2f   %8.2f / %8.2f   %s / %s" % (k, bkt["N"], bkt["meas"] / U, bkt["sigma"] / U, bkt["fam"]["canonical|Z0.0"]["pred"] / U,
          bkt["fam"]["canonical|Z0.3"]["pred"] / U, bkt["word"]["canonical"], bkt["word"]["alt"]))
    WORD = {}
    for nm in E.FOOT:
        moved = [k for k, bkt in BR.items() if bkt["word"][nm] != G0["word"][nm]]
        WORD[nm] = G0["word"][nm] + (" [BRACKET-DEPENDENT: %s]" % ", ".join(moved) if moved and G0["word"][nm] != "NOT EVALUABLE" else "")
    P("  LANE WORD (Part G): %s / %s" % (WORD["canonical"], WORD["alt"]))
    RES["partG"] = dict(primary=G0, brackets=BR, word=WORD)
    rep = {}
    for key in ("salpeter", "central"):
        keep = np.isfinite(V["022"]["f"][iW]); rep[key] = {"%s|Z%.1f" % (nm, Zm): wmean(F[(nm, key, Zm)], V["022"]["T"][iW], keep) for nm in E.FOOT for Zm in ZMET}
    P("  reported, same weights: Salpeter stars Z 0 %.1f / %.1f, Z 0.3 %.1f / %.1f; sources near z 2 Z 0 %.1f / %.1f, Z 0.3 %.1f / %.1f (canonical / alt)"
      % tuple(rep[k]["%s|Z%.1f" % (nm, Zm)] / U for k in ("salpeter", "central") for Zm in ZMET for nm in ("canonical", "alt")))
    RES["reported_predictions"] = rep

    # ---------------------------------------------------------------- Part C
    P("\n[Part C: wide lenses against ESZ1's matched controls]")
    posC = {T[i]["pair"]: i for i in iC}; pr_ = np.array([(i, posC[T[i]["id"]]) for i in iW if T[i]["id"] in posC], int)
    def part_c(b):
        Dd = V[b]["f"][pr_[:, 0]] - V[b]["f"][pr_[:, 1]]; Dd = Dd[np.isfinite(Dd)]; N = len(Dd)
        if N < 100: return dict(N=N, word="NOT EVALUABLE", mean=float("nan"), lo=float("nan"), hi=float("nan"))
        rng = np.random.default_rng(E.SEED); bs = Dd[rng.integers(0, N, (NBOOT, N))].mean(1); lo, hi = float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
        return dict(N=N, mean=float(Dd.mean()), lo=lo, hi=hi, word="WIDE LENSES ARE BRIGHTER IN X-RAYS" if lo > 0 else "NO EXCESS DETECTED")
    C0, C1 = part_c("022"), part_c("024")
    wc = "NOT EVALUABLE" if not allok else C0["word"] + (" [BRACKET-DEPENDENT: band 024]" if C1["word"] != C0["word"] and C0["word"] != "NOT EVALUABLE" else "")
    for b, c in (("022", C0), ("024", C1)):
        P("  band %s: N = %d pairs, mean difference %+.3f [%+.3f, %+.3f] -> %s" % (b, c["N"], c["mean"] / U, c["lo"] / U, c["hi"] / U, c["word"]))
    P("  LANE WORD (Part C): %s" % wc)
    RES["partC"] = dict(band022=C0, band024=C1, word=wc)

    # ---------------------------------------------------------------- Part D
    P("\n[Part D (no word); 1e-15 erg/s/cm^2]")
    PD = {}
    for b in ("022", "024"):
        for cn, sel in (("W", iW), ("C", iC)):
            s = st(b, sel); su = st(b, sel, False); keep = np.isfinite(V[b]["f"][sel]); off = wmean(V[b]["off"][sel], V[b]["T"][sel], keep)
            zz = np.array([byid[T[i]["id"]]["z"] for i in sel]); lum = 4.0 * math.pi * (E.EUCLID.DL(zz) * 100.0) ** 2 * V[b]["f"][sel]
            PD["%s|%s" % (cn, b)] = dict(N=s["N"], stack=s["mean"], sigma=s["sigma"], unweighted=su["mean"], unweighted_sigma=su["sigma"], offsets_mean=off, mean_luminosity=float(np.nanmean(lum)))
            P("  %s band %s: N %d, stack %+.3f +- %.3f (unweighted %+.3f +- %.3f); its offsets alone average %+.3f; mean luminosity %.2e erg/s"
              % (cn, b, s["N"], s["mean"] / U, s["sigma"] / U, su["mean"] / U, su["sigma"] / U, off / U, np.nanmean(lum)))
    ulW = D["022"]["ulb"].reshape(nT, 9)[iW, 0]; vW = V["022"]["valid"][iW]; u2 = D2["ulb"]; ok2 = D2["de"] & np.isfinite(u2) & (D2["flag"] == 0)
    PL = {}
    for nm in E.FOOT:
        for Zm in ZMET:
            f = F[(nm, "least", Zm)]; PL["%s|Z%.1f" % (nm, Zm)] = dict(below_eRASS1_022=int(np.sum(vW & (ulW < f))), n_eRASS1=int(vW.sum()),
                                                                     below_DR2_024=int(np.sum(ok2 & (u2 < f * KB["024"] / KB["022"]))), n_DR2=int(ok2.sum()))
    P("  per lens: the service's own 3 sigma limit lies below the lens's least prediction for (Z 0 / Z 0.3): eRASS1 band 022 %d / %d of %d (canonical), %d / %d (alt); DR2 three-survey band 024 %d / %d of %d (canonical), %d / %d (alt)"
      % (PL["canonical|Z0.0"]["below_eRASS1_022"], PL["canonical|Z0.3"]["below_eRASS1_022"], PL["canonical|Z0.0"]["n_eRASS1"], PL["alt|Z0.0"]["below_eRASS1_022"], PL["alt|Z0.3"]["below_eRASS1_022"],
         PL["canonical|Z0.0"]["below_DR2_024"], PL["canonical|Z0.3"]["below_DR2_024"], PL["canonical|Z0.0"]["n_DR2"], PL["alt|Z0.0"]["below_DR2_024"], PL["alt|Z0.3"]["below_DR2_024"]))
    RES["partD"] = dict(stacks=PD, per_lens=PL, K=KB)
    RES["samples"] = dict(W=NW, C=int(len(iC)), W_valid_022=int(V["022"]["valid"][iW].sum()), pairs=int(len(pr_)), k2_sources=nk)
    RES["stack_W_022"] = sW; RES["checks_all_pass"] = bool(allok)

    # ---------------------------------------------------------------- twins
    if MUT:
        if MUT == "inject":
            ok = all(G0["fam"]["%s|Z0.0" % nm]["word"] == "ALLOWED" for nm in E.FOOT); msg = "Z = 0 reads %s / %s" % tuple(G0["fam"]["%s|Z0.0" % nm]["word"] for nm in E.FOOT)
        elif MUT == "shift":
            ok = not CK["K2"]["ok"]; msg = "K2 %s" % ("FAILS" if ok else "still passes")
        elif MUT == "newton":
            ref = json.load(open(os.path.join(HERE, "exr2_results.json")))["partG"]["primary"]["fam"]
            now = [G0["fam"]["%s|Z0.0" % nm]["pred"] for nm in ("canonical", "alt")]; was = [ref["%s|Z0.0" % nm]["pred"] for nm in ("canonical", "alt")]
            ok = all(x > y for x, y in zip(now, was)); msg = "pred(Z = 0) %.3e / %.3e against %.3e / %.3e erg/s/cm^2" % (now[0], now[1], was[0], was[1])
        else: ok, msg = False, "unknown twin"
        P("\n[MUTATE %s] %s -> %s" % (MUT, msg, "BITES (exit 1)" if ok else "DOES NOT BITE (exit 2)")); RES["mutate_bites"] = bool(ok)
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1, default=float)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if ok else 2)

    with open(os.path.join(HERE, "exr2_per_lens.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["unique_identifier", "class", "pair", "z_l", "theta_E_arcsec", "valid_022", "exposure_s_022", "counts_022", "background_022", "flux_022", "flux_024",
                    "service_limit_022", "pred_Z0_canonical", "pred_Z0.3_canonical", "pred_Z0_alt", "pred_Z0.3_alt"])
        loc = {int(i): k for k, i in enumerate(iW)}; c9 = D["022"]["cnt"].reshape(nT, 9); b9 = D["022"]["bkg"].reshape(nT, 9); u9 = D["022"]["ulb"].reshape(nT, 9)
        fm = lambda x: "%.4e" % x if np.isfinite(x) else ""
        for i, t in enumerate(T):
            r = byid[t["id"]]; pr = [fm(F[(nm, "least", Zm)][loc[i]]) if i in loc else "" for nm in ("canonical", "alt") for Zm in ZMET]
            w.writerow([t["id"], t["cls"], t["pair"], "%.4f" % r["z"], "%.4f" % r["tE"], int(V["022"]["valid"][i]), "%.1f" % V["022"]["T"][i] if np.isfinite(V["022"]["T"][i]) else "",
                        fm(c9[i, 0]), fm(b9[i, 0]), fm(V["022"]["f"][i]), fm(V["024"]["f"][i]), fm(u9[i, 0])] + pr)
    P("\nchecks all pass: %s" % allok)
    json.dump(RES, open(os.path.join(HERE, "exr2_results.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "exr2.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if allok else 3)

if __name__ == "__main__":
    main()
