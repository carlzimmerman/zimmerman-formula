#!/usr/bin/env python3
"""EXR1 (WIDE-LENS X-RAY CUSP).  Frozen criteria: FROZEN_CRITERIA.md (commit 0cc195b7f6).  Offline grading.

Does eRASS1 see the X-rays that ESZ1's remaining gas body (G2: rho ~ r^-2 cut at 300 kpc, hydrostatic in law S's own
field, zero edge pressure) must emit from Euclid's wide lenses (theta_E >= 1.7")?

Run:
  python3 -I exr1.py --data-dir <ECLIPSE dir> --fetch <exr1_fetch cache> --atomdb <atomdb_v3.1.3 dir> \
                     --resp <dir with the TM0 ARF and RMF> --clusters <erass1cl_primary_v3.2.fits>
  EXR1_MUTATE=inject | shift | newton  python3 -I exr1.py ...   (each must exit 1)
"""
import argparse, csv, hashlib, json, math, os, sys, time
import numpy as np
from scipy.special import gammaincc, gammainccinv

HERE = os.path.dirname(os.path.abspath(__file__))
for _d in ("EUC1_eclipse_saturation_ceiling", "EUC4_wide_lenses", "EUC8_wide_lens_residual_profile", "ESZ1_wide_lens_gas_pressure"):
    sys.path.insert(0, os.path.join(HERE, "..", _d))
if os.environ.get("ESZ1_MUTATE"): sys.exit("ESZ1_MUTATE must not be set")
import euc1 as E
import esz1 as Z1
L8 = Z1.L8
MUT = (os.environ.get("EXR1_MUTATE", "") or "").strip()
if MUT == "newton": E.FOOT = {k: 1.0e-30 for k in E.FOOT}
FOOT = dict(E.FOOT)
G, MSUN, KPC = E.G, E.MSUN, E.KPC
MP, MU, MUE, KEVJ = Z1.MP, Z1.MU, Z1.MUE, Z1.KEV
XH = 2.0 / MUE - 1.0                      # hydrogen mass fraction implied by mu_e
KEV = 1.602176634e-9                      # erg
MPG = MP * 1.0e3                          # g
CM = 100.0                                # m -> cm
ARCSEC = math.pi / 648000.0
ECF = 1.074e12                            # eRASS1 0.2-2.3 keV, absorbed Gamma 2, N_H 3e20 (cm^2/erg)
EEF = 0.75
FCLIP = 1.0e-12
NBOOT = 2000
RT = Z1.RT
AP_TH, AP_FAC = 10.0, 2.0 / 3.0
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)

# ---------------------------------------------------------------- absorption: Morrison & McCammon (1983) Table 2
MM83 = [(0.030, 0.100, 17.3, 608.1, -2150.), (0.100, 0.284, 34.6, 267.9, -476.1), (0.284, 0.400, 78.1, 18.8, 4.3),
        (0.400, 0.532, 71.4, 66.8, -51.4), (0.532, 0.707, 95.5, 145.8, -61.1), (0.707, 0.867, 308.9, -380.6, 294.0),
        (0.867, 1.303, 120.6, 169.3, -47.7), (1.303, 1.840, 141.3, 146.8, -31.5), (1.840, 2.471, 202.7, 104.7, -17.0),
        (2.471, 3.210, 342.7, 18.7, 0.0), (3.210, 4.038, 352.2, 18.7, 0.0), (4.038, 7.111, 433.9, -2.4, 0.75),
        (7.111, 8.331, 629.0, 30.9, 0.0), (8.331, 10.00, 701.2, 25.2, 0.0)]
def sigma_mm(E_):
    E_ = np.asarray(E_, float); s = np.zeros_like(E_)
    for lo, hi, c0, c1, c2 in MM83:
        m = (E_ >= lo) & (E_ < hi); s[m] = (c0 + c1 * E_[m] + c2 * E_[m] ** 2) / E_[m] ** 3 * 1e-24
    m = E_ >= 10.0; s[m] = (701.2 + 25.2 * E_[m]) / E_[m] ** 3 * 1e-24
    return s

# ---------------------------------------------------------------- APEC reader
def seg_cumint(e, f, x):
    """exact integral from e[0] to x of the piecewise-linear f on nodes e (zero outside)."""
    e = np.asarray(e, float); f = np.asarray(f, float)
    if len(e) < 2: return np.zeros_like(x)
    seg = 0.5 * (f[1:] + f[:-1]) * np.diff(e); Fn = np.concatenate([[0.0], np.cumsum(seg)])
    xc = np.clip(x, e[0], e[-1]); i = np.clip(np.searchsorted(e, xc, side="right") - 1, 0, len(e) - 2)
    dx = xc - e[i]; sl = (f[i + 1] - f[i]) / np.maximum(e[i + 1] - e[i], 1e-300)
    return Fn[i] + f[i] * dx + 0.5 * sl * dx * dx

class Apec:
    """rest-frame photon emissivity per n_e n_H (photons cm^3 s^-1 per bin) on bin edges eg (keV), H+He and metals apart."""
    def __init__(self, ddir, eg):
        from astropy.io import fits
        Lf = fits.open(os.path.join(ddir, "apec_v3.1.3_line.fits"), memmap=True); Cf = fits.open(os.path.join(ddir, "apec_v3.1.3_coco.fits"), memmap=True)
        self.kT = np.asarray(Lf[1].data["kT"], float); nT = len(self.kT); self.lkT = np.log(self.kT)
        self.eg = eg; nb = len(eg) - 1; self.ec = np.sqrt(eg[1:] * eg[:-1])
        self.hhe = np.zeros((nT, nb)); self.met = np.zeros((nT, nb))
        self.bol = np.zeros((nT, 2))                      # 0.001-20 keV energy emissivity (erg cm^3/s), [H+He, metals]
        KB = 8.617333262e-8                                # keV/K
        for j in range(nT):
            hl, hc = Lf[j + 2], Cf[j + 2]
            for h in (hl, hc):
                if abs(h.header["TEMPERATURE"] * KB / self.kT[j] - 1.0) > 2e-3: raise RuntimeError("APEC HDU order")
            t = hl.data; El = 12.398419843320026 / np.asarray(t["Lambda"], float); eps = np.asarray(t["Epsilon"], float); el = np.asarray(t["Element"])
            idx = np.searchsorted(eg, El, side="right") - 1; ok = (idx >= 0) & (idx < nb); inb = (El >= 0.001) & (El <= 20.0)
            for comp, m in ((0, el <= 2), (1, el >= 3)):
                np.add.at(self.hhe[j] if comp == 0 else self.met[j], idx[ok & m], eps[ok & m])
                self.bol[j, comp] += float(np.sum(eps[m & inb] * El[m & inb])) * KEV
            for row in hc.data:
                if int(row["rmJ"]) != 0: continue
                comp = 0 if int(row["Z"]) <= 2 else 1; tgt = self.hhe[j] if comp == 0 else self.met[j]
                for ne, ee, ff in ((int(row["N_Cont"]), row["E_Cont"], row["Continuum"]), (int(row["N_Pseudo"]), row["E_Pseudo"], row["Pseudo"])):
                    if ne < 2: continue
                    ee = np.asarray(ee[:ne], float); ff = np.asarray(ff[:ne], float)
                    tgt += np.diff(seg_cumint(ee, ff, eg))
                    self.bol[j, comp] += float(np.diff(seg_cumint(ee, ff * ee, np.array([0.001, 20.0])))[0]) * KEV
        Lf.close(); Cf.close()
    def tw(self, kT):
        """interpolation weights (index, weight) on the tabulated temperatures, linear in log kT, clipped to the table."""
        x = np.clip(np.log(np.asarray(kT, float)), self.lkT[0], self.lkT[-1])
        j = np.clip(np.searchsorted(self.lkT, x, side="right") - 1, 0, len(self.lkT) - 2)
        f = (x - self.lkT[j]) / (self.lkT[j + 1] - self.lkT[j])
        return j, f
    def at(self, vec, kT):
        j, f = self.tw(kT); return vec[j] * (1.0 - f) + vec[j + 1] * f
    def lam_bol(self, kT, Z):
        return self.at(self.bol[:, 0] + Z * self.bol[:, 1], kT)

# ---------------------------------------------------------------- response
class Resp:
    def __init__(self, rdir):
        from astropy.io import fits
        a = fits.open(os.path.join(rdir, "em01_180135_020_ARF_00004_c010.fits"))[1].data
        self.elo, self.ehi, self.A = (np.asarray(a[c], float) for c in ("ENERG_LO", "ENERG_HI", "SPECRESP")); self.em = 0.5 * (self.elo + self.ehi)
        r = fits.open(os.path.join(rdir, "em01_180135_020_RMF_00004_c010.fits")); M = r["MATRIX"]; off = int(M.header.get("TLMIN4", 1))
        eb = r["EBOUNDS"].data; self.cE = 0.5 * (np.asarray(eb["E_MIN"], float) + np.asarray(eb["E_MAX"], float))
        R = np.zeros((len(M.data), len(eb)))
        for i, row in enumerate(M.data):
            fc, nc, mat = np.atleast_1d(row["F_CHAN"]), np.atleast_1d(row["N_CHAN"]), np.asarray(row["MATRIX"], float); k = 0
            for f_, n_ in zip(fc, nc):
                R[i, int(f_) - off:int(f_) - off + int(n_)] = mat[k:k + int(n_)]; k += int(n_)
        self.R = np.nan_to_num(R)
        self.files = [os.path.join(rdir, "em01_180135_020_ARF_00004_c010.fits"), os.path.join(rdir, "em01_180135_020_RMF_00004_c010.fits")]
    def rband(self, lo, hi):
        return self.R[:, (self.cE >= lo) & (self.cE < hi)].sum(1)
    def eff(self, NH, lo=0.2, hi=2.3):
        return self.A * np.exp(-sigma_mm(self.em) * NH) * self.rband(lo, hi)
    def ecf_pl(self, NH=3.0e20, lo=0.2, hi=2.3, gamma=2.0):
        """counts per (erg cm^-2 s^-1) of absorbed flux in [lo, hi) for a power law (my ECF; only its shape is used)."""
        ph = (self.elo ** (1 - gamma) - self.ehi ** (1 - gamma)) / (gamma - 1.0)
        cr = float(np.sum(ph * self.eff(NH, lo, hi)))
        x = np.geomspace(lo, hi, 20001); fx = x ** (1 - gamma) * np.exp(-sigma_mm(x) * NH)
        F = float(np.sum(0.5 * (fx[1:] + fx[:-1]) * np.diff(x))) * KEV
        return cr / F

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""): h.update(b)
    return h.hexdigest()

# ---------------------------------------------------------------- per-position spectral response (per unit emission measure)
class Lensresp:
    """for one source at redshift z, luminosity distance DL (cm), N_H: per tabulated kT, the catalogue-equivalent flux,
    the absorbed observed 0.2-2.3 keV energy flux and the rest-frame 0.2-2.3 keV luminosity, per unit int n_e n_H dV (cm^-3)."""
    def __init__(self, AP, RS, ecf_mine, z, DL, NH):
        Eo = AP.ec / (1.0 + z); b = np.searchsorted(RS.ehi, Eo, side="right"); ok = (b < len(RS.ehi)) & (Eo >= RS.elo[0])
        eff = RS.eff(NH); emap = np.where(ok, eff[np.minimum(b, len(eff) - 1)], 0.0)
        geo = (1.0 + z) / (4.0 * math.pi * DL * DL)
        self.fcat = np.stack([AP.hhe @ emap, AP.met @ emap], 1) * geo / ecf_mine
        inb = (Eo >= 0.2) & (Eo < 2.3); wabs = np.where(inb, np.exp(-sigma_mm(Eo) * NH) * Eo * KEV, 0.0)
        self.fabs = np.stack([AP.hhe @ wabs, AP.met @ wabs], 1) * geo
        wr = np.where((AP.ec >= 0.2) & (AP.ec < 2.3), AP.ec * KEV, 0.0)
        self.lrest = np.stack([AP.hhe @ wr, AP.met @ wr], 1)
    def comb(self, vec, Z):
        return vec[:, 0] + Z * vec[:, 1]

# ---------------------------------------------------------------- gas body and emission measure
def body(RE, Re, n, Ms, z, a0, case, bs):
    """ESZ1's G2 per lens: gas mass (kg), the radial grid (m), pressure (Pa) and the stellar field."""
    Mt = math.pi * RE ** 2 * E.EUCLID.sigcr(z, L8.zs_case(z, case))
    L2 = L8.Lens2(RE, Re, n, Ms); eng = {"L2": L2, "gx2": L2.gx("2.0")}
    Mg = Z1.solve_gas("G2", RE, Re, n, Ms, Mt, 10.0 ** bs, a0, eng)
    r = Z1.grid(300.0)[0]
    Menc, rho = Z1.gas_body("G2", Mg, r)
    gs0 = G * Ms[:, None] * E.M3D_frac(r[None, :], Re[:, None], n[:, None]) / r[None, :] ** 2
    Pr = Z1.pressure(r, rho, E.g_law(10.0 ** bs * gs0 + G * Menc / r[None, :] ** 2, a0, "S"))
    kTm = np.where(Mg > 0, MU * MP * 4.0 * math.pi * np.sum(Pr * r[None, :] ** 3 * Z1.lnw(r)[None, :], axis=1) / np.maximum(Mg, 1e-300), np.nan) / KEVJ
    return dict(Mg=Mg, r=r, Pr=Pr, kTm=kTm)

def em_weights(AP, Mg, r, Pr, rin, rout, tfac=1.0, ngrid=1500, lam_const=None):
    """EM-weighted distribution over APEC temperatures (cm^-3) of the G2 gas between rin and rout (m), per lens.
    lam_const: return int n_e n_H dV instead (for check K5)."""
    N = len(Mg); W = np.zeros((N, len(AP.kT))); EMt = np.zeros(N); lr = np.log(r)
    for i in range(N):
        if Mg[i] <= 0 or rout[i] <= rin[i]: continue
        re = np.geomspace(rin[i], rout[i], ngrid); h = math.log(re[1] / re[0]); w = np.full(ngrid, h); w[0] = w[-1] = 0.5 * h
        rho = Mg[i] / (4.0 * math.pi * RT * re ** 2)
        Pe = np.interp(np.log(re), lr, Pr[i]); kT = np.maximum(MU * MP * Pe / rho / KEVJ * tfac, 1e-6)
        ne = rho / (MUE * MP) * 1e-6; nH = XH * rho / MP * 1e-6
        dEM = ne * nH * 4.0 * math.pi * (re * CM) ** 3 * w
        EMt[i] = dEM.sum()
        if lam_const is not None: continue
        j, f = AP.tw(kT); np.add.at(W[i], j, dEM * (1.0 - f)); np.add.at(W[i], j + 1, dEM * f)
    return EMt if lam_const is not None else W

# ---------------------------------------------------------------- statistics
def kbn_ul(C, B, cl=0.9987):
    C = np.asarray(C, float); B = np.asarray(B, float); Q0 = gammaincc(C + 1.0, B)
    return gammainccinv(C + 1.0, (1.0 - cl) * Q0) - B
def boot(v, rng_seed=None):
    v = np.asarray(v, float); N = len(v)
    rng = np.random.default_rng(E.SEED); bs = v[rng.integers(0, N, (NBOOT, N))].mean(1)
    return bs
def word(meas, sig, pmin):
    if not (np.isfinite(meas) and np.isfinite(sig) and np.isfinite(pmin)) or pmin < 3.0 * sig: return "NO POWER"
    return "EXCLUDED" if meas + 2.0 * sig < pmin else "ALLOWED"
def sep_arcsec(ra1, de1, ra2, de2):
    r1, d1, r2, d2 = map(np.radians, (ra1, de1, ra2, de2))
    c = np.sin(d1) * np.sin(d2) + np.cos(d1) * np.cos(d2) * np.cos(r1 - r2)
    return np.degrees(np.arccos(np.clip(c, -1, 1))) * 3600.0

# ================================================================== main
def main():
    ap = argparse.ArgumentParser()
    for k in ("--data-dir", "--fetch", "--atomdb", "--resp", "--clusters"): ap.add_argument(k, required=True)
    a = ap.parse_args(); t0 = time.time(); tag = "exr1" + ("_MUTATE_" + MUT if MUT else "")
    P("EXR1 (WIDE-LENS X-RAY CUSP)%s" % ("   *** MUTATE = %s ***" % MUT if MUT else ""))
    RES = dict(lane="EXR1", criteria_commit="0cc195b7f6", mutate=MUT, footings=FOOT)
    CK = {}
    def ck(k, what, val, ok):
        CK[k] = dict(what=what, value=val, ok=bool(ok)); P("  %s %-3s %s : %s" % ("PASS" if ok else "FAIL", k, what, val))

    # ---------------------------------------------------------------- inputs
    P("\n[data]")
    rows, _ = E.load(a.data_dir); OUT.extend(E.OUT); E.OUT.clear()
    radec = {}
    with open(os.path.join(a.data_dir, "eclipse_dr1_catalogue_key_v20261103.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f): radec[r["unique_identifier"]] = (E.fl(r["ra"]), E.fl(r["dec"]))
    S, _ = E.select(rows, ("A", "B")); S = sorted([r for r in S if np.isfinite(radec[r["id"]]).all()], key=lambda r: r["id"])
    W = [r for r in S if r["tE"] >= 1.7]
    P("  S %d lenses; W (theta_E >= 1.7\") %d" % (len(S), len(W)))
    for p in [a.clusters] + Resp(a.resp).files + [os.path.join(a.atomdb, f) for f in ("apec_v3.1.3_line.fits", "apec_v3.1.3_coco.fits")]:
        P("  sha256 %-40s %s" % (os.path.basename(p), sha256(p)))
    UL = {}
    with open(os.path.join(a.fetch, "ul_table.csv"), newline="") as f:
        for r in csv.DictReader(f): UL[(r["kind"], r["id"], int(r["k"]))] = r
    NHI = {}
    with open(os.path.join(a.fetch, "nh_table.csv"), newline="") as f:
        for r in csv.DictReader(f): NHI[(r["kind"], r["id"])] = float(r["NHI_cm2"])
    SCS = {}
    with open(os.path.join(a.fetch, "scs_table.csv"), newline="") as f:
        for r in csv.DictReader(f): SCS.setdefault((r["kind"], r["id"]), []).append(r)
    P("  upper-limit rows %d, N_HI rows %d, cone rows %d (cones with any source %d)" % (len(UL), len(NHI), sum(len(v) for v in SCS.values()), len(SCS)))
    def meas(key):
        r = UL.get(key)
        if r is None or r["de_sky"] != "True" or r["Exposure"] in ("", None) or float(r["Exposure"]) <= 0: return None
        C, B, T = float(r["Count"]), float(r["Bkg_counts"]), float(r["Exposure"])
        return dict(C=C, B=B, T=T, f=(C - B) / (EEF * T * ECF), ULB=float(r["UL_B"]), ULS=float(r["UL_S"]), flag=int(r["Flag_pos"]))

    # ---------------------------------------------------------------- physics machinery
    eg = np.geomspace(0.04, 40.0, 6001)
    AP = Apec(a.atomdb, eg); RS = Resp(a.resp); ecf_mine = RS.ecf_pl()
    P("  APEC: %d temperatures %.2e to %.2e keV; rest grid %d bins; my ECF (TM0 ARF shape only) %.4e" % (len(AP.kT), AP.kT[0], AP.kT[-1], len(eg) - 1, ecf_mine))

    P("\n[instrument checks]")
    l0 = float(AP.lam_bol(1.0, 0.0)); r12 = float(AP.lam_bol(0.12, 1.0) / AP.lam_bol(0.12, 0.0))
    ck("K1", "APEC reader: Lambda_bol(1 keV, Z 0) = 8.917e-24 (2 %); Lambda_bol(0.12 keV) Z 1 / Z 0 = 30.1 (5 %)", "%.4e (%+.2f %%); %.2f (%+.2f %%)"
       % (l0, 100 * (l0 / 8.917e-24 - 1), r12, 100 * (r12 / 30.1 - 1)), abs(l0 / 8.917e-24 - 1) < 0.02 and abs(r12 / 30.1 - 1) < 0.05)
    e1 = RS.ecf_pl(lo=0.2, hi=2.3); got = [RS.ecf_pl(lo=lo, hi=hi) / e1 for lo, hi in ((0.2, 0.5), (0.5, 1.0), (1.0, 2.0))]
    want = [9.217e11 / 1.074e12, 1.359e12 / 1.074e12, 1.014e12 / 1.074e12]
    ck("K2", "band ECF ratios 0.2-0.5 / 0.5-1 / 1-2 keV over 0.2-2.3 keV, absorbed Gamma 2, N_H 3e20 (8 %)",
       " / ".join("%.3f vs %.3f" % (g, w) for g, w in zip(got, want)), all(abs(g / w - 1) < 0.08 for g, w in zip(got, want)))

    # ---------------------------------------------------------------- tested set, positions
    SHIFT = MUT == "shift"
    Mw = {r["id"]: meas(("Wshift", r["id"], 0) if SHIFT else ("S", r["id"], 0)) for r in W}
    desky_W = [r for r in W if UL.get(("S", r["id"], 0), {}).get("de_sky") == "True"]
    T_ = [r for r in W if Mw[r["id"]] is not None]
    P("\n[sample]  W in the eROSITA-DE sky: %d of %d; tested (de_sky, exposure > 0): %d (required >= 100)" % (len(desky_W), len(W), len(T_)))
    ids = [r["id"] for r in T_]; NT = len(T_)
    _, zT, RET, ReT, nT, lmT = E.build(T_); MsT = 10.0 ** lmT * MSUN
    raT = np.array([radec[i][0] for i in ids]); deT = np.array([radec[i][1] for i in ids])
    DAT = E.EUCLID.DA(zT); DLT = DAT * (1.0 + zT) ** 2 * CM
    nhi = np.array([NHI[("W", i)] for i in ids]); P("  N_HI (HI4PI) over T: median %.2e, range %.2e to %.2e cm^-2" % (np.median(nhi), nhi.min(), nhi.max()))
    fT = np.array([Mw[i]["f"] for i in ids]); TT = np.array([Mw[i]["T"] for i in ids])
    gradeA = np.array([r["grade"] == "A" for r in T_]); P("  median exposure %.0f s, median background %.2f counts, median z_l %.3f" % (np.median(TT), np.median([Mw[i]["B"] for i in ids]), np.median(zT)))

    # K3 upper limits recomputed at every de_sky lens position of S
    rr = [meas(("S", r["id"], 0)) for r in S]; rr = [x for x in rr if x is not None]
    ulc = kbn_ul([x["C"] for x in rr], [x["B"] for x in rr]) / (EEF * np.array([x["T"] for x in rr]) * ECF); ulb = np.array([x["ULB"] for x in rr])
    dev = np.abs(ulc / ulb - 1.0)
    ck("K3", "UL_B recomputed (KBN 99.87 %, EEF 0.75, ECF 1.074e12) within 2 % at >= 99 % of de_sky lens positions",
       "%d positions; median dev %.2e, %.2f %% within 2 %%, max %.2e" % (len(dev), np.median(dev), 100 * np.mean(dev < 0.02), dev.max()), np.mean(dev < 0.02) >= 0.99)

    # K4 known answers: eRASS1 groups
    from astropy.io import fits
    cd = fits.open(a.clusters)[1].data; zc = np.asarray(cd["BEST_Z"], float)
    kt, ktl, kth = (np.asarray(cd[c], float) for c in ("KT", "KT_L", "KT_H"))
    with np.errstate(invalid="ignore"): gi = np.where((kt > 0) & (ktl > 0) & (kth - ktl < 0.3 * kt) & (zc > 0.05))[0]
    C70 = E.Cosmo(70.0, 0.3); ra_, rb_, rc_ = [], [], []
    for i in gi:
        z = zc[i]; DL = C70.DL(z) * CM; NH = NHI[("GR", str(int(i)))]
        lr_ = Lensresp(AP, RS, ecf_mine, z, DL, NH)
        fcat = AP.at(lr_.comb(lr_.fcat, 0.3), kt[i]); fab = AP.at(lr_.comb(lr_.fabs, 0.3), kt[i]); lre = AP.at(lr_.comb(lr_.lrest, 0.3), kt[i])
        ra_.append((float(cd["CR500"][i]) / (float(cd["F500"][i]) * 1e-14)) / (ECF * fcat / fab))
        rb_.append((float(cd["F500"][i]) * 1e-14 * 4 * math.pi * DL ** 2 / (float(cd["L500"][i]) * 1e42)) / (fab * 4 * math.pi * DL ** 2 / lre))
        M = float(cd["MGAS500"][i]) * 1e11 * MSUN * 1e3; V = 4.0 / 3.0 * math.pi * (float(cd["R500"][i]) * KPC * CM) ** 3
        Lu = lre * XH * M * M / (MUE * MPG * MPG * V); rc_.append(float(cd["L500"][i]) * 1e42 / Lu)
    ma, mb, mc = (float(np.median(x)) for x in (ra_, rb_, rc_))
    ck("K4", "eRASS1 groups (kT to 30 %%, z > 0.05; N = %d): CR500/F500 vs predicted (1 +- 0.10); F500 4 pi D_L^2 / L500 vs predicted (1 +- 0.10); L500 over uniform-sphere least (median 1 to 30)" % len(gi),
       "median %.3f [%.3f, %.3f]; %.3f [%.3f, %.3f]; %.2f [%.2f, %.2f]" % (ma, *np.percentile(ra_, [16, 84]), mb, *np.percentile(rb_, [16, 84]), mc, *np.percentile(rc_, [16, 84])),
       abs(ma - 1) <= 0.10 and abs(mb - 1) <= 0.10 and 1.0 <= mc <= 30.0)

    # K5 luminosity integral (Newtonian r^-2 body, constant Lambda): numeric int n_e n_H dV against analytic
    Mg5 = np.array([3.0e12 * MSUN]); r3 = Z1.grid(300.0)[0]; Me5, rho5 = Z1.gas_body("G2", Mg5, r3)
    P5 = Z1.pressure(r3, rho5, E.g_law(G * Me5 / r3[None, :] ** 2, 1e-30, "S")); rin5 = np.array([12.6 * KPC]); rt5 = np.array([RT])
    num = em_weights(AP, Mg5, r3, P5, rin5, rt5, lam_const=True)[0]
    ana = XH * (Mg5[0] * 1e3) ** 2 / (4.0 * math.pi * MUE * MPG ** 2 * (RT * CM) ** 2) * (1.0 / (rin5[0] * CM) - 1.0 / (RT * CM))
    ck("K5", "luminosity integral of an r^-2 body at constant Lambda against analytic (1e-4)", "%.2e" % abs(num / ana - 1), abs(num / ana - 1) < 1e-4)

    # K6 ESZ1 reproduced on its 237 lenses
    if not MUT:
        e_ids = [r["unique_identifier"] for r in csv.DictReader(open(os.path.join(HERE, "..", "ESZ1_wide_lens_gas_pressure", "esz1_per_lens.csv"))) if r["is_W"] == "1"]
        Wd = {r["id"]: r for r in W}; W6 = [Wd[i] for i in e_ids]
        _, z6, RE6, Re6, n6, lm6 = E.build(W6); Ms6 = 10.0 ** lm6 * MSUN
        ref = json.load(open(os.path.join(HERE, "..", "ESZ1_wide_lens_gas_pressure", "esz1_results.json")))["model"]; e6 = []
        for nm, a0 in FOOT.items():
            b6 = body(RE6, Re6, n6, Ms6, z6, a0, "far", 0.10)
            ne6 = np.where(b6["Mg"] > 0, Z1.gas_density_at("G2", b6["Mg"], RE6) / (MUE * MP) * 1e-6, np.nan)
            want6 = ref["%s|G2|far|+0.10" % nm]
            for got6, k in ((float(np.median(b6["Mg"] / MSUN)), "Mg_med"), (float(np.nanmedian(b6["kTm"])), "kT_med"), (float(np.nanmedian(ne6)), "ne_med")):
                e6.append(abs(got6 / want6[k] - 1.0))
        ck("K6", "ESZ1 reproduced on its %d lenses: G2 far b* +0.10 median gas mass, kT, n_e(R_E), both footings (0.1 %%)" % len(W6), "max %.1e" % max(e6), max(e6) < 1e-3)

    # ---------------------------------------------------------------- predictions
    P("\n[model: G2 per tested lens, catalogue-equivalent 0.2-2.3 keV flux in the aperture]")
    Rsp = {fac: [Lensresp(AP, RS, ecf_mine, zT[i], DLT[i], fac * nhi[i]) for i in range(NT)] for fac in (2.0, 1.0)}
    rap = np.minimum(AP_TH * ARCSEC * DAT, RT)
    SETS = {"primary": ("far", 0.10, 0.1, 2.0, "ap", "RE"), "Z = 0 (H and He only)": ("far", 0.10, 0.0, 2.0, "ap", "RE"), "Z = 0.3": ("far", 0.10, 0.3, 2.0, "ap", "RE"),
            "N_H = 1 x N_HI": ("far", 0.10, 0.1, 1.0, "ap", "RE"), "point source": ("far", 0.10, 0.1, 2.0, "pt", "RE"), "r_in = R_E/2": ("far", 0.10, 0.1, 2.0, "ap", "RE2"),
            "r_in = 1 kpc": ("far", 0.10, 0.1, 2.0, "ap", "1kpc"), "Z = 1.0 (reported)": ("far", 0.10, 1.0, 2.0, "ap", "RE"),
            "central source (reported)": ("central", 0.10, 0.1, 2.0, "ap", "RE"), "b* = 0 (reported)": ("far", 0.0, 0.1, 2.0, "ap", "RE")}
    RIN = {"RE": RET, "RE2": 0.5 * RET, "1kpc": np.full(NT, 1.0 * KPC)}
    BOD, EMW, PRED, INFO = {}, {}, {}, {}
    def pred_of(W_, Z, fac, apf):
        return np.array([apf * float(W_[i] @ Rsp[fac][i].comb(Rsp[fac][i].fcat, Z)) for i in range(NT)])
    for nm, a0 in FOOT.items():
        for sname, (case, bs, Z, fac, apm, rin) in SETS.items():
            if (nm, case, bs) not in BOD: BOD[(nm, case, bs)] = body(RET, ReT, nT, MsT, zT, a0, case, bs)
            bd = BOD[(nm, case, bs)]; rout = rap if apm == "ap" else np.full(NT, RT)
            kk = (nm, case, bs, apm, rin)
            if kk not in EMW: EMW[kk] = em_weights(AP, bd["Mg"], bd["r"], bd["Pr"], RIN[rin], rout)
            PRED[(nm, sname)] = pred_of(EMW[kk], Z, fac, AP_FAC if apm == "ap" else 1.0)
        bd = BOD[(nm, "far", 0.10)]
        kRE = np.array([np.interp(math.log(RET[i]), np.log(bd["r"]), bd["Pr"][i]) for i in range(NT)]) * MU * MP / np.maximum(bd["Mg"] / (4 * math.pi * RT * RET ** 2), 1e-300) / KEVJ
        rhoRE = bd["Mg"] / (4 * math.pi * RT * RET ** 2); ne = rhoRE / (MUE * MP) * 1e-6; nH = XH * rhoRE / MP * 1e-6; ntot = rhoRE / (MU * MP) * 1e-6
        tc = {Z: 1.5 * ntot * kRE * KEV / (ne * nH * AP.lam_bol(np.maximum(kRE, 1e-3), Z)) / 3.156e13 for Z in (0.1, 0.3)}
        Wall = em_weights(AP, bd["Mg"], bd["r"], bd["Pr"], np.full(NT, 1.0 * KPC), np.full(NT, RT)); Wre = em_weights(AP, bd["Mg"], bd["r"], bd["Pr"], RET, np.full(NT, RT))
        Lall = np.array([float(Wall[i] @ Rsp[2.0][i].comb(Rsp[2.0][i].lrest, 0.1)) for i in range(NT)]); Lre = np.array([float(Wre[i] @ Rsp[2.0][i].comb(Rsp[2.0][i].lrest, 0.1)) for i in range(NT)])
        need = bd["Mg"] > 0
        INFO[nm] = dict(Mg_med=float(np.median(bd["Mg"] / MSUN)), frac_zero=float(np.mean(~need)), kT_RE_med=float(np.median(kRE[need])), ne_RE_med=float(np.median(ne[need])),
                        L_rest_all_from_1kpc_med=float(np.median(Lall[need])), L_rest_rE_med=float(np.median(Lre[need])), pred_med=float(np.median(PRED[(nm, "primary")][need])),
                        tcool_Myr_Z01=float(np.median(tc[0.1][need])), tcool_Myr_Z03=float(np.median(tc[0.3][need])), kT_mass_weighted_med=float(np.nanmedian(bd["kTm"])))
        P("  %-9s median gas mass %.2e Msun (%.1f %% need none); kT at R_E %.3f keV; n_e at R_E %.3f cm^-3; rest 0.2-2.3 keV luminosity (Z 0.1) from 1 kpc %.2e, from R_E %.2e erg/s; pred_i %.2e erg/s/cm^2; t_cool at R_E %.0f Myr (Z 0.1), %.0f Myr (Z 0.3)"
          % (nm, INFO[nm]["Mg_med"], 100 * INFO[nm]["frac_zero"], INFO[nm]["kT_RE_med"], INFO[nm]["ne_RE_med"], INFO[nm]["L_rest_all_from_1kpc_med"], INFO[nm]["L_rest_rE_med"], INFO[nm]["pred_med"], INFO[nm]["tcool_Myr_Z01"], INFO[nm]["tcool_Myr_Z03"]))
    RES["model"] = INFO

    if MUT == "inject":
        fT = fT + PRED[("canonical", "primary")]; P("\n[MUTATE inject] the primary canonical prediction added to every tested lens's measured value")

    # ---------------------------------------------------------------- stacks
    clip = lambda v: np.minimum(np.asarray(v, float), FCLIP)
    nulls = np.full((NT, 8), np.nan)
    for i, lid in enumerate(ids):
        for k in range(8):
            m = meas(("Wshift", lid, k))
            if m is not None: nulls[i, k] = m["f"]
    def stack(sel):
        v = clip(fT[sel]); bs = boot(v); ns = np.array([np.nanmean(clip(nulls[sel, k])) for k in range(8)])
        sb, sn = float(bs.std()), float(np.sqrt(np.mean(ns ** 2)))
        return dict(N=int(len(v)), mean=float(v.mean()), sigma=max(sb, sn), sig_boot=sb, sig_null=sn, nulls=[float(x) for x in ns])
    allT = np.arange(NT); s0 = stack(allT)
    P("\n[stack of tested W lenses; units 1e-15 erg/s/cm^2, catalogue-equivalent 0.2-2.3 keV in the aperture]")
    P("  N = %d: measured %+.3f, sigma %.3f (bootstrap %.3f, null stacks %.3f); null stacks: %s" % (s0["N"], 1e15 * s0["mean"], 1e15 * s0["sigma"], 1e15 * s0["sig_boot"], 1e15 * s0["sig_null"], " ".join("%+.2f" % (1e15 * x) for x in s0["nulls"])))
    ns = np.array(s0["nulls"])
    ck("K8", "8 null stacks at 0.5 deg: mean within 3 sigma/4 of zero, none beyond 3.5 sigma", "mean %+.3f, largest %.3f, sigma %.3f (1e-15)" % (1e15 * ns.mean(), 1e15 * np.abs(ns).max(), 1e15 * s0["sigma"]),
       abs(ns.mean()) <= 0.75 * s0["sigma"] and np.abs(ns).max() <= 3.5 * s0["sigma"])
    # K7 positive control
    pcz = np.asarray(cd["BEST_Z"], float); pcm = np.asarray(cd["M500"], float) * 1e13
    pc = np.where((pcm >= 2e14) & (pcz >= 0.1) & (pcz <= 0.6))[0]
    kind = "CLshift" if SHIFT else "CL"
    fc = np.array([m["f"] for m in (meas((kind, str(int(i)), 0)) for i in pc) if m is not None])
    bc = boot(clip(fc)); zc7 = float(clip(fc).mean() / bc.std())
    rng = np.random.default_rng(E.SEED); pick = sorted(rng.choice(len(pc), 60, replace=False).tolist())
    rec = sum(1 for j in pick if len(SCS.get((kind, str(int(pc[j]))), [])) > 0)
    ck("K7", "positive control: eRASS1 clusters (M500 >= 2e14, 0.1 <= z <= 0.6): stack >= 5 sigma; >= 90 %% of 60 with a Main source within 60\"",
       "N = %d, %+.2f +- %.2f (1e-15), %.1f sigma; %d of 60 recovered" % (len(fc), 1e15 * clip(fc).mean(), 1e15 * bc.std(), zc7, rec), zc7 >= 5.0 and rec >= 54)
    allok = all(v["ok"] for v in CK.values()) and all(k in CK for k in (["K1", "K2", "K3", "K4", "K5", "K7", "K8"] + ([] if MUT else ["K6"])))
    RES["checks"] = CK; RES["checks_all_pass"] = bool(allok)

    # ---------------------------------------------------------------- Part G
    P("\n[Part G: predicted least stack against the measured stack; units 1e-15 erg/s/cm^2]")
    def grade(sel, sname, show):
        s = stack(sel); out = dict(N=s["N"], meas=s["mean"], sigma=s["sigma"], fam={})
        for nm in FOOT:
            pmin = float(clip(PRED[(nm, sname)][sel]).mean()); w = word(s["mean"], s["sigma"], pmin)
            if not allok or s["N"] < 100: w = "NOT EVALUABLE"
            out["fam"][nm] = dict(pred_min=pmin, word=w, z=(pmin - s["mean"]) / s["sigma"], ratio=pmin / (s["mean"] + 2 * s["sigma"]),
                                  f_M=math.sqrt(max(s["mean"] + 2 * s["sigma"], 0.0) / pmin) if pmin > 0 else float("nan"))
            if show: P("    %-26s %-9s pred_min %8.2f   measured %+7.3f +- %.3f   (pred - meas)/sigma %7.1f   pred/(meas + 2 sigma) %6.2f   f_M %.3f -> %s"
                       % (sname, nm, 1e15 * pmin, 1e15 * s["mean"], 1e15 * s["sigma"], out["fam"][nm]["z"], out["fam"][nm]["ratio"], out["fam"][nm]["f_M"], w))
        return out
    G0 = grade(allT, "primary", True)
    BR = {}
    for sname in SETS:
        if sname == "primary": continue
        BR[sname] = grade(allT, sname, True)
    BR["grade A only"] = grade(np.where(gradeA)[0], "primary", True); BR["z_l <= 0.6 only"] = grade(np.where(zT <= 0.6)[0], "primary", True)
    TAGS = ("Z = 0 (H and He only)", "Z = 0.3", "N_H = 1 x N_HI", "point source", "r_in = R_E/2", "r_in = 1 kpc", "grade A only", "z_l <= 0.6 only")
    WORD = {}
    for nm in FOOT:
        moved = [k for k in TAGS if BR[k]["fam"][nm]["word"] != G0["fam"][nm]["word"]]
        WORD[nm] = G0["fam"][nm]["word"] + (" [BRACKET-DEPENDENT: %s]" % ", ".join(moved) if moved and G0["fam"][nm]["word"] != "NOT EVALUABLE" else "")
    P("  LANE WORD (Part G): %s / %s" % (WORD["canonical"], WORD["alt"]))
    # f_T: temperature factor at which the predicted stack falls to measured + 2 sigma (density fixed)
    FT = {}
    for nm in FOOT:
        bd = BOD[(nm, "far", 0.10)]; target = s0["mean"] + 2 * s0["sigma"]; curve = []
        for phi in np.geomspace(0.01, 1.0, 41):
            Wp = em_weights(AP, bd["Mg"], bd["r"], bd["Pr"], RET, rap, tfac=phi); curve.append((float(phi), float(clip(pred_of(Wp, 0.1, 2.0, AP_FAC)).mean())))
        below = [p for p, v in curve if v <= target]
        FT[nm] = dict(curve=curve, f_T=max(below) if below else None)
        P("  %-9s f_T (largest factor on kT(r), density fixed, at which the least stack falls to measured + 2 sigma): %s; stack at kT x 0.1, 0.3, 1: %s"
          % (nm, "%.3f" % FT[nm]["f_T"] if FT[nm]["f_T"] else "none down to 0.01", ", ".join("%.2f" % (1e15 * v) for p, v in curve if abs(math.log10(p) - math.log10(0.1)) < 0.026 or abs(math.log10(p / 0.3)) < 0.026 or p == 1.0)))
    RES["partG"] = dict(primary=G0, brackets=BR, word=WORD, f_T=FT, stack=s0)

    # ---------------------------------------------------------------- Part C
    P("\n[Part C: wide lenses against matched small-ring controls]")
    tES = E.arr(S, "tE"); zS = E.arr(S, "z"); lS = E.arr(S, "lm")
    mS = [meas(("S", r["id"], 0)) for r in S]
    pool = np.array([j for j in range(len(S)) if tES[j] < 1.0 and mS[j] is not None], int); used = np.zeros(len(S), bool)
    posS = {r["id"]: j for j, r in enumerate(S)}; pairs = []
    for i, lid in enumerate(ids):
        j0 = posS[lid]; d = ((zS[pool] - zS[j0]) / 0.05) ** 2 + ((lS[pool] - lS[j0]) / 0.1) ** 2; d = np.where(used[pool], np.inf, d)
        if not np.isfinite(d).any(): continue
        j = int(pool[int(np.argmin(d))]); used[j] = True; pairs.append((i, j))
    D = np.array([clip(fT[i]) - clip(mS[j]["f"]) for i, j in pairs]); bsd = boot(D)
    lo, hi = float(np.percentile(bsd, 2.5)), float(np.percentile(bsd, 97.5))
    wc = "NOT EVALUABLE" if (len(D) < 100 or not allok) else ("WIDE LENSES ARE BRIGHTER IN X-RAYS" if lo > 0 else "NO EXCESS DETECTED")
    cvals = clip([mS[j]["f"] for _, j in pairs]); bcv = boot(cvals)
    P("  %d pairs; median |dz| %.3f, median |d log M*| %.3f; controls stack %+.3f +- %.3f (1e-15)" % (len(pairs), np.median([abs(zS[posS[ids[i]]] - zS[j]) for i, j in pairs]),
      np.median([abs(lS[posS[ids[i]]] - lS[j]) for i, j in pairs]), 1e15 * cvals.mean(), 1e15 * bcv.std()))
    P("  wide minus control: %+.3f [%+.3f, %+.3f] x 1e-15 -> %s" % (1e15 * D.mean(), 1e15 * lo, 1e15 * hi, wc))
    RES["partC"] = dict(N=len(D), mean=float(D.mean()), lo=lo, hi=hi, word=wc, controls_mean=float(cvals.mean()), controls_sigma=float(bcv.std()))

    # ---------------------------------------------------------------- Part L
    P("\n[Part L: per lens (reported)]")
    det, detfl, chance, chn = 0, [], 0, 0
    from_shift = [EXR1_shift_pos(radec[lid]) for lid in ids]
    for i, lid in enumerate(ids):
        src = SCS.get(("W", lid), [])
        if src:
            sra = np.array([float(s["ra"]) for s in src]); sde = np.array([float(s["dec"]) for s in src]); sf = np.array([float(s["ml_flux_1"]) for s in src])
            sp = sep_arcsec(radec[lid][0], radec[lid][1], sra, sde)
            if (sp <= 30.0).any(): det += 1; detfl.append(float(sf[sp <= 30.0].max()))
            for (pra, pde) in from_shift[i]:
                chn += 1; chance += int((sep_arcsec(pra, pde, sra, sde) <= 30.0).any())
        else:
            chn += 8
    ulb = np.array([Mw[i]["ULB"] for i in ids]); empty = 6.645 / (EEF * TT * ECF)
    LL = {}
    for nm in FOOT:
        pr = PRED[(nm, "primary")]; powered = empty < pr
        LL[nm] = dict(below=int(np.sum(ulb < pr)), powered=int(powered.sum()), below_powered=int(np.sum((ulb < pr) & powered)), N=NT)
        P("  %-9s lenses whose eRASS1 3-sigma bound UL_B is below their least prediction: %d of %d; lenses where an empty aperture could do that: %d (of them below: %d)"
          % (nm, LL[nm]["below"], NT, LL[nm]["powered"], LL[nm]["below_powered"]))
    P("  Main-catalogue source within 30\" of the lens: %d of %d (%.1f %%); at the 8 shifted positions: %.2f %% (chance); catalogued fluxes of matched sources: median %.2e, max %.2e"
      % (det, NT, 100 * det / NT, 100 * chance / max(chn, 1), np.median(detfl) if detfl else float("nan"), max(detfl) if detfl else float("nan")))
    RES["partL"] = dict(per_footing=LL, detected_30arcsec=det, N=NT, chance_rate=chance / max(chn, 1), matched_flux_median=float(np.median(detfl)) if detfl else None)

    # ---------------------------------------------------------------- Part D
    P("\n[Part D (reported)]")
    Lstack = float(np.mean(clip(fT) * 4 * math.pi * DLT ** 2)); P("  the stack as a mean luminosity (catalogue-equivalent flux x 4 pi D_L^2, no K-correction): %.2e erg/s" % Lstack)
    for lab, cond in (("1.3 - 1.7\"", (tES >= 1.3) & (tES < 1.7)), ("1.0 - 1.3\"", (tES >= 1.0) & (tES < 1.3)), ("below 1.0\"", tES < 1.0)):
        v = clip([mS[j]["f"] for j in range(len(S)) if cond[j] and mS[j] is not None]); bv = boot(v)
        P("  class %-12s N = %4d  measured %+.3f +- %.3f (1e-15)" % (lab, len(v), 1e15 * v.mean(), 1e15 * bv.std()))
    RES["partD"] = dict(L_stack=Lstack)
    RES["samples"] = dict(S=len(S), W=len(W), W_de_sky=len(desky_W), tested=NT, pairs=len(pairs), clusters=int(len(fc)), groups_K4=int(len(gi)))

    # ---------------------------------------------------------------- twins
    if MUT:
        if MUT == "inject":
            okm = all(G0["fam"][nm]["word"] == "ALLOWED" for nm in FOOT); msg = "word %s / %s" % tuple(G0["fam"][nm]["word"] for nm in FOOT)
        elif MUT == "shift":
            okm = not CK["K7"]["ok"]; msg = "K7 %s" % ("FAILS" if okm else "still passes")
        elif MUT == "newton":
            ref = json.load(open(os.path.join(HERE, "exr1_results.json")))["partG"]["primary"]["fam"]
            now = [G0["fam"][nm]["pred_min"] for nm in ("canonical", "alt")]; was = [ref[nm]["pred_min"] for nm in ("canonical", "alt")]
            okm = all(x > y for x, y in zip(now, was)); msg = "pred_min %.3e / %.3e against %.3e / %.3e" % (now[0], now[1], was[0], was[1])
        else: okm, msg = False, "unknown twin"
        P("\n[MUTATE %s] %s -> %s" % (MUT, msg, "BITES (exit 1)" if okm else "DOES NOT BITE (exit 2)"))
        RES["mutate_bites"] = bool(okm)
        json.dump(RES, open(os.path.join(HERE, tag + "_results.json"), "w"), indent=1, default=float)
        open(os.path.join(HERE, tag + ".out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1 if okm else 2)

    ctl = {i: S[j]["id"] for i, j in pairs}
    # output-only addition (after a debug run on the cached upper limits showed K8 failing; no grading line changed):
    # the per-lens arrays a dated post hoc amendment needs
    np.savez_compressed(os.path.join(HERE, "exr1_arrays.npz"), ids=np.array(ids), f=fT, nulls=nulls, z=zT, gradeA=gradeA, exposure=TT, ulb=ulb,
                        pair_w=np.array([i for i, _ in pairs]), pair_c_f=np.array([mS[j]["f"] for _, j in pairs]),
                        **{("pred|%s|%s" % k).replace("/", " over "): v for k, v in PRED.items()})
    with open(os.path.join(HERE, "exr1_per_lens.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["unique_identifier", "grade", "z_l", "theta_E_arcsec", "log_Mstar", "ra", "dec", "NHI_cm2", "counts", "bkg_counts", "exposure_s", "UL_B", "f_net",
                    "pred_canonical", "pred_alt", "Mgas_canonical_Msun", "control"])
        for i, lid in enumerate(ids):
            m = Mw[lid]
            w.writerow([lid, T_[i]["grade"], "%.4f" % zT[i], "%.4f" % T_[i]["tE"], "%.4f" % lmT[i], "%.6f" % raT[i], "%.6f" % deT[i], "%.3e" % nhi[i], int(m["C"]), "%.4f" % m["B"],
                        "%.2f" % m["T"], "%.4e" % m["ULB"], "%.4e" % m["f"], "%.4e" % PRED[("canonical", "primary")][i], "%.4e" % PRED[("alt", "primary")][i],
                        "%.4e" % (BOD[("canonical", "far", 0.10)]["Mg"][i] / MSUN), ctl.get(i, "")])
    P("\nchecks all pass: %s" % allok)
    print("run time %.0f s" % (time.time() - t0), file=sys.stderr)
    json.dump(RES, open(os.path.join(HERE, "exr1_results.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "exr1.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if allok else 3)

def shifted(ra, dec, pa_deg, rad_deg=0.5):
    """true-angle offset on the sphere (PA from north through east); identical to exr1_fetch.shifted."""
    d0, a0, th, pa = math.radians(dec), math.radians(ra), math.radians(rad_deg), math.radians(pa_deg)
    d1 = math.asin(math.sin(d0) * math.cos(th) + math.cos(d0) * math.sin(th) * math.cos(pa))
    a1 = a0 + math.atan2(math.sin(pa) * math.sin(th) * math.cos(d0), math.cos(th) - math.sin(d0) * math.sin(d1))
    return (math.degrees(a1) % 360.0, math.degrees(d1))
def EXR1_shift_pos(rd):
    return [shifted(rd[0], rd[1], 45.0 * k) for k in range(8)]

if __name__ == "__main__":
    main()
