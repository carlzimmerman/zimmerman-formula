"""EUC12 graded reading: Euclid P vs SLACS on one stellar-mass scale (A: DESI DR1 CIGALE; B: Legacy Surveys DR10
W1 with one E-MILES recipe) and one dispersion fitter (EUC5R's, both sides).  FROZEN_CRITERIA.md governs.
Run from the repo root after euc12_cigale.py and euc12_fetch_ls.py.
EUC12_MUTATE=shift: +0.20 dex on the Euclid common-scale masses; Delta must fall by 0.20 +- 0.01; exits 1."""
import glob, json, math, os, sys
import numpy as np
import pandas as pd
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "EUC5R_blind_dynamical_boost_regrade"))
from euc5r_model import (ARCSEC, A0_ALT, A0_CANON, ECLIPSE_COSMO, AUGER_COSMO, Cosmo, SersicLens, b_lens, a0_units)
from euc12_common import euclid_chosen, load_slacs_pos, KEY

MUT = os.environ.get("EUC12_MUTATE", "")
TAG = "_MUTATE_shift" if MUT == "shift" else ""
SEED = 20261112
NB = 2000
FOOT = {"canonical": A0_CANON, "alt": A0_ALT}
WMAP7 = Cosmo(70.4, 0.272)
FW = 2.354820045
E5R = "closure_2026_11_12/EUC5R_blind_dynamical_boost_regrade"
LS = "_external_data/euc12_common_mass_scale/ls_dr10"
EM = "_external_data/lam9_emiles_bi_basti"
LINES, RES, KN = [], {}, {}


def P(s=""):
    print(s, flush=True)
    LINES.append(s)


def known(name, ok, val):
    KN[name] = dict(ok=bool(ok), value=val)
    P(f"  {name:34s} {'PASS' if ok else 'FAIL'}  {val}")


def sep(ra1, de1, ra2, de2):
    d = np.radians
    c = np.sin(d(de1)) * np.sin(d(de2)) + np.cos(d(de1)) * np.cos(d(de2)) * np.cos(d(ra1 - ra2))
    return np.degrees(np.arccos(np.clip(c, -1, 1))) * 3600


def bmed(x, rng):
    x = np.asarray(x, float)
    return np.median(x[rng.integers(0, len(x), (NB, len(x)))], axis=1)


def ci(arr):
    return float(np.percentile(arr, 2.5)), float(np.percentile(arr, 97.5))


def word(m, lo, hi):
    if lo >= -0.10 and hi <= 0.10:
        return "SAME STARS"
    if lo > 0 and m >= 0.10:
        return "EUCLID NEEDS MORE"
    if hi < 0 and m <= -0.10:
        return "EUCLID NEEDS LESS"
    return "NO VERDICT"


# ------------------------------------------------------------------ construction B recipe (E-MILES, top-hat bands)
LSUN = 3.828e33
KPC_CM = 3.0856775814913673e21
C_AA = 2.99792458e18
NMGY = 3.631e-29          # erg/s/cm2/Hz
BANDS = {"W1": (30000.0, 37000.0), "z": (8500.0, 10000.0), "V": (5000.0, 6000.0)}


class Emiles:
    def __init__(self):
        fs = sorted(glob.glob(f"{EM}/fits/Ebi1.30Zp0.06T*_iTp0.00_baseFe.fits"))
        self.age = np.array([float(os.path.basename(f).split("T")[1].split("_")[0]) for f in fs])
        h = fits.getheader(fs[0])
        n = h["NAXIS1"]
        self.lam = h["CRVAL1"] + h["CDELT1"] * (np.arange(n) + 1 - h["CRPIX1"])
        self.spec = np.array([fits.getdata(f).astype(float) for f in fs])     # Lsun/A per Msun initial
        tab = [l.split() for l in open(f"{EM}/out_mass_BI_BASTI") if l.startswith("BI")]
        self.msr, self.lv = {}, {}
        for t in tab:
            if abs(float(t[1]) - 1.30) < 1e-6 and abs(float(t[2]) - 0.06) < 1e-6:
                self.msr[round(float(t[3]), 4)] = float(t[5])
                self.lv[round(float(t[3]), 4)] = float(t[12])

    def _band_fnu(self, i, z, DL_kpc, band):
        """photon-weighted mean f_nu (erg/s/cm2/Hz) in a top-hat band for template i at z, per Msun initial."""
        lo, hi = BANDS[band]
        lam_o = self.lam * (1 + z)
        m = (lam_o >= lo) & (lam_o <= hi)
        fl = self.spec[i, m] * LSUN / (4 * math.pi * (DL_kpc * KPC_CM) ** 2 * (1 + z))
        lo_ = lam_o[m]
        return np.trapz(fl * lo_, lo_) / np.trapz(C_AA / lo_, lo_)

    def mass_per_nmgy(self, z, DL_kpc, band, age_gyr):
        """surviving mass (Msun) per nanomaggy of observed flux, interpolated in log age."""
        age_gyr = min(max(age_gyr, self.age[0]), 14.0)
        j = int(np.clip(np.searchsorted(self.age, age_gyr) - 1, 0, len(self.age) - 2))
        t = (math.log(age_gyr) - math.log(self.age[j])) / (math.log(self.age[j + 1]) - math.log(self.age[j]))
        vals = []
        for k in (j, j + 1):
            f = self._band_fnu(k, z, DL_kpc, band) / NMGY      # nmgy per Msun initial
            vals.append(math.log(self.msr[round(self.age[k], 4)] / f))
        return math.exp((1 - t) * vals[0] + t * vals[1])

    def k7(self):
        i = int(np.argmin(abs(self.age - 10.0)))
        DL = 0.01        # 10 pc in kpc
        fnu = self._band_fnu(i, 0.0, DL, "V")
        MV = -2.5 * math.log10(fnu / 3631e-23)
        LV = 10 ** (-0.4 * (MV - 4.80))            # Lsun,V per Msun initial (M_V,sun = 4.80 AB)
        mine = self.msr[round(self.age[i], 4)] / LV
        tabv = self.msr[round(self.age[i], 4)] / self.lv[round(self.age[i], 4)]
        return mine, tabv


def age_at(co, z, zf=3.0):
    """t(z) - t(zf) in Gyr, flat LCDM-form expansion history used only as a clock for the SSP age."""
    from scipy.integrate import quad
    H0 = co.H0 / 977.792                           # 1/Gyr
    f = lambda a: 1.0 / (a * H0 * math.sqrt(co.Om / a ** 3 + 1 - co.Om))
    return quad(f, 1 / (1 + zf), 1 / (1 + z))[0]


def ls_flux(name, ra, dec):
    fn = f"{LS}/{name}.csv"
    if not os.path.exists(fn):
        return None
    try:
        t = pd.read_csv(fn)
    except Exception:
        return None
    if not len(t) or "flux_w1" not in t:
        return None
    t = t[t["type"].astype(str).str.strip() != "PSF"].copy()
    if not len(t):
        return None
    t["sep"] = sep(ra, dec, t.ra.values, t.dec.values)
    t = t[t.sep <= 1.5].sort_values("sep")
    if not len(t):
        return None
    r = t.iloc[0]
    return dict(W1=r.flux_w1 / r.mw_transmission_w1, z=r.flux_z / r.mw_transmission_z, sep=r.sep)


# ------------------------------------------------------------------ main
def main():
    rng_master = np.random.default_rng(SEED)
    P(f"EUC12 graded reading {'[MUTATE shift +0.20 dex on Euclid common masses]' if MUT else ''}")
    cig = pd.read_csv(f"{HERE}/euc12_cigale_rows.csv")
    pl = pd.read_csv(f"{E5R}/euc5r_per_lens.csv")
    Pset = pl[pl.in_P].set_index("uid")
    key = pd.read_csv(KEY, low_memory=False).set_index("unique_identifier")
    ch = euclid_chosen().set_index("unique_identifier")
    sl = {s["name"]: s for s in load_slacs_pos()}
    sf = pd.read_csv(f"{E5R}/euc5r_slacs_fits.csv").set_index("name")

    # ---------------- Euclid: b_dyn recomputed (K5) and CIGALE match
    P("\n== Euclid side (sample P) ==")
    E = []
    for uid, r in Pset.iterrows():
        c = key.loc[uid]
        z, zp = float(r.z), float(r.zphot)
        Mcat_raw = 10 ** float(c.eclipse_log_survived_mass_med)
        Ms = Mcat_raw * (ECLIPSE_COSMO.DL(z) / ECLIPSE_COSMO.DL(zp)) ** 2
        DA = ECLIPSE_COSMO.DA(z)
        Re = float(c.eclipse_effective_radius) * ARCSEC * DA
        n = float(c.eclipse_sersic_index)
        Rap = 0.75 * ARCSEC * DA
        L = SersicLens(Ms, Re, n, beta=0.0)
        row = dict(uid=uid, z=z, zphot=zp, thetaE=float(r.thetaE), logMs=math.log10(Ms),
                   logMs_raw=math.log10(Mcat_raw), sigma=float(r.sigma))
        for fn, a0 in FOOT.items():
            for fw in (0.9, 1.1, 1.3):
                row[f"b_{fn}_{fw}"] = L.b_dyn(r.sigma, a0_units(a0), "S", Rap, fw / FW * ARCSEC * DA)[0]
            row[f"bN_{fn}"] = L.b_dyn(r.sigma, 1e-30, "S", Rap, 1.1 / FW * ARCSEC * DA)[0]
            row[f"bK6_{fn}"] = SersicLens(Ms * 10 ** 0.2, Re, n).b_dyn(r.sigma, a0_units(a0), "S", Rap,
                                                                      1.1 / FW * ARCSEC * DA)[0]
        # CIGALE
        cc = ch.loc[uid]
        g = cig[(cig.tag == "euclid") & (cig.TARGETID == int(cc.targetid))]
        if len(g) > 1:
            gg = g[(g.SURVEY == cc.survey) & (g.PROGRAM == cc.program)]
            g = gg if len(gg) else g.iloc[[int(np.argmin(abs(g.Z - cc.z_desi)))]]
        if len(g):
            g = g.iloc[0]
            row.update(cig_Z=float(g.Z), cig_logM_raw=float(g.LOGM), cig_sep=float(sep(c.ra, c.dec, g.RA, g.DEC)),
                       cig_chi2=float(g.CHI2), zdesi=float(cc.z_desi), cig_logMerr=float(g.LOGM_ERR))
            if np.isfinite(g.LOGM) and g.LOGM > 8:
                Mc = 10 ** g.LOGM * (ECLIPSE_COSMO.DL(g.Z) / WMAP7.DL(g.Z)) ** 2
                if MUT == "shift":
                    Mc *= 10 ** 0.2
                row["dA"] = math.log10(Ms / Mc)
                row["dA_raw"] = math.log10(Mcat_raw / Mc)
        # B
        f = ls_flux(uid, c.ra, c.dec)
        if f is not None:
            row["ls_sep"] = f["sep"]
            for band in ("W1", "z"):
                if np.isfinite(f[band]) and f[band] > 0:
                    mb = f[band] * EMI.mass_per_nmgy(z, ECLIPSE_COSMO.DL(z), band, age_at(ECLIPSE_COSMO, z))
                    if MUT == "shift":
                        mb *= 10 ** 0.2
                    row[f"dB_{band}"] = math.log10(Ms / mb)
        E.append(row)
    E = pd.DataFrame(E)

    # ---------------- SLACS: b_dyn on EUC5R's own-fitter sigma, CIGALE match
    P("== SLACS side ==")
    S = []
    for name, s in sl.items():
        row = dict(name=name, zl=s["zl"], logMs=s["logMs"], logMc=s["logMc"])
        if not np.isfinite(s["logMs"]):
            continue
        Re_arc = s["ReV"] if np.isfinite(s["ReV"]) and s["ReV"] > 0 else s["ReI"]
        row["Re_from"] = "V" if np.isfinite(s["ReV"]) and s["ReV"] > 0 else "I"
        DA = AUGER_COSMO.DA(s["zl"])
        Ms = 10 ** s["logMs"]
        if np.isfinite(Re_arc) and Re_arc > 0:
            Re = Re_arc * ARCSEC * DA
            Rap = 1.5 * ARCSEC * DA
            L = SersicLens(Ms, Re, 4.0, beta=0.0)
            sigs = {}
            if name in sf.index:
                q = sf.loc[name]
                if bool(q.deg_q):
                    sigs["deg"] = float(q.deg_sigma)
                if bool(q.nat_q):
                    sigs["nat"] = float(q.nat_sigma)
            row["in_fit"] = name in sf.index
            if np.isfinite(s["sig"]):
                sigs["pub"] = s["sig"]
            for lab, sg in sigs.items():
                for fn, a0 in FOOT.items():
                    for fw in ((1.2, 1.5, 1.8) if lab == "deg" else (1.5,)):
                        bd, ed = L.b_dyn(sg, a0_units(a0), "S", Rap, fw / FW * ARCSEC * DA)
                        row[f"b_{lab}_{fn}_{fw}"] = bd
                        row[f"edge_{lab}_{fn}_{fw}"] = ed
                    if lab == "deg":
                        row[f"bN_{fn}"] = L.b_dyn(sg, 1e-30, "S", Rap, 1.5 / FW * ARCSEC * DA)[0]
        # CIGALE by position + redshift
        for tg, key_ in (("slacs", "dA"), ("slacs_shift", "shift")):
            g = cig[cig.tag == f"{tg}:{name}"].copy()
            if len(g):
                dec0 = s["dec"] + (60 / 3600 if tg == "slacs_shift" else 0)
                g["sep"] = sep(s["ra"], dec0, g.RA.values, g.DEC.values)
                g = g[(g.sep <= 1.5) & (abs(g.Z - s["zl"]) <= 0.005)].sort_values("sep")
            if len(g):
                g = g.iloc[0]
                if tg == "slacs_shift":
                    row["shift_hit"] = 1
                    continue
                row.update(cig_Z=float(g.Z), cig_sep=float(g.sep), cig_logM_raw=float(g.LOGM), cig_chi2=float(g.CHI2))
                if np.isfinite(g.LOGM) and g.LOGM > 8:
                    Mc = 10 ** g.LOGM * (AUGER_COSMO.DL(g.Z) / WMAP7.DL(g.Z)) ** 2
                    row["dA"] = math.log10(Ms / Mc)
                    row["dA_chab"] = s["logMc"] - math.log10(Mc)
        f = ls_flux("SLACS_" + name, s["ra"], s["dec"])
        if f is not None:
            row["ls_sep"] = f["sep"]
            for band in ("W1", "z"):
                if np.isfinite(f[band]) and f[band] > 0:
                    mb = f[band] * EMI.mass_per_nmgy(s["zl"], AUGER_COSMO.DL(s["zl"]), band, age_at(AUGER_COSMO, s["zl"]))
                    row[f"dB_{band}"] = math.log10(Ms / mb)
        S.append(row)
    S = pd.DataFrame(S)
    E.to_csv(f"{HERE}/euc12_euclid{TAG}.csv", index=False, float_format="%.5f")
    S.to_csv(f"{HERE}/euc12_slacs{TAG}.csv", index=False, float_format="%.5f")

    # ---------------- known answers
    P("\n== known answers ==")
    # K1
    k1 = S.dropna(subset=["dA", "dA_chab"])
    known("K1_chabrier_minus_salpeter", abs(np.median(k1.dA_chab - k1.dA) + 0.25) <= 0.02,
          f"median {np.median(k1.dA_chab - k1.dA):+.4f} (N {len(k1)})")
    # K2
    nsh = int(S.get("shift_hit", pd.Series(dtype=float)).fillna(0).sum())
    known("K2_shifted_position_null", nsh <= 1, f"{nsh} matched of {len(S)}")
    # K3
    em = E.dropna(subset=["cig_Z"])
    dz = (em.cig_Z - em.zdesi).abs().max()
    sm = S.dropna(subset=["cig_Z"])
    known("K3_euclid_z_equal", dz <= 1e-4, f"max |dZ| {dz:.2e} (N {len(em)})")
    known("K3_slacs_z", float(np.median(abs(sm.cig_Z - sm.zl))) <= 0.001,
          f"median |Z - zlens| {np.median(abs(sm.cig_Z - sm.zl)):.5f} (N {len(sm)})")
    fpos = float((em.cig_sep <= 1.0).mean())
    known("K3_euclid_position_1arcsec", fpos >= 0.90, f"fraction {fpos:.3f}, max sep {em.cig_sep.max():.2f}\"")
    # K4: J3 through EUC5R machinery (frozen form: n 4, Re(V), 1.5" fibre, 1.5" FWHM, alt, b from lens equation)
    a0u = a0_units(A0_ALT)
    rat = []
    for s in sl.values():
        if not all(np.isfinite([s["zl"], s["zs"], s["sig"], s["RE"], s["ReV"]])) or s["RE"] <= 0 or s["ReV"] <= 0:
            continue
        DA = AUGER_COSMO.DA(s["zl"])
        Re = s["ReV"] * ARCSEC * DA
        L = SersicLens(1e11, Re, 4.0)
        bl = b_lens(1e11, Re, 4.0, s["RE"], AUGER_COSMO.sigcr(s["zl"], s["zs"]), a0u, "S")
        rat.append(L.sigma_ap(10 ** bl, a0u, "S", 1.5 * ARCSEC * DA, 1.5 / FW * ARCSEC * DA) / s["sig"])
    known("K4_J3_reproduced", abs(np.median(rat) - 0.966) <= 0.002, f"{np.median(rat):.4f} (N {len(rat)})")
    # K5
    for fn in FOOT:
        m = float(np.median(E[f"b_{fn}_1.1"]))
        tgt = {"canonical": 0.202, "alt": 0.197}[fn]
        dmax = float((E[f"b_{fn}_1.1"].values - Pset[f"b_{fn}_S_+0.0_1.1"].reindex(E.uid).values).__abs__().max())
        known(f"K5_euclid_P_median_{fn}", abs(m - tgt) <= 0.002 and dmax <= 1e-3, f"{m:+.4f} (max per-lens diff {dmax:.1e})")
    # K7
    mine, tabv = EMI.k7()
    known("K7_emiles_ML_V_10Gyr", abs(mine / tabv - 1) <= 0.15, f"mine {mine:.3f} vs table {tabv:.3f}")
    gates_ok = all(v["ok"] for v in KN.values())

    # ---------------- statistic
    cls = {"thetaE<1.3": E.thetaE < 1.3, "all P": E.thetaE > -1, "thetaE>=1.3": E.thetaE >= 1.3}

    def delta(Eb, Ed, Sb, Sd, seed):
        rng = np.random.default_rng(seed)
        a, b_, c, d = bmed(Eb, rng), bmed(Ed, rng), bmed(Sb, rng), bmed(Sd, rng)
        D = (a + b_) - (c + d)
        m = (np.median(Eb) + np.median(Ed)) - (np.median(Sb) + np.median(Sd))
        return float(m), ci(D), ci(b_ - d), float(np.median(Ed) - np.median(Sd))

    for cons, dcol in (("A", "dA"), ("B_W1", "dB_W1"), ("B_z", "dB_z")):
        P(f"\n== construction {cons} ==")
        Sd = S[dcol].dropna() if dcol in S else pd.Series(dtype=float)
        RES[cons] = {}
        nE_prim = int(E[cls["thetaE<1.3"]][dcol].notna().sum()) if dcol in E else 0
        P(f"N: SLACS with delta {len(Sd)}; Euclid primary-class with delta {nE_prim}; Euclid P with delta "
          f"{int(E[dcol].notna().sum()) if dcol in E else 0} of {len(E)}")
        if len(Sd) < 10 or nE_prim < 10:
            P("   below minimum N")
            RES[cons]["minN"] = False
            continue
        RES[cons]["minN"] = True
        rng = np.random.default_rng(SEED)
        dS = bmed(Sd, rng)
        P(f"delta_S median {Sd.median():+.4f} [{ci(dS)[0]:+.4f}, {ci(dS)[1]:+.4f}] (N {len(Sd)}); "
          f"restricted to the fitted 30: {S[S.get('in_fit', False) == True][dcol].median():+.4f} "
          f"(N {S[S.get('in_fit', False) == True][dcol].notna().sum()})")
        for cn, sel in cls.items():
            Ec = E[sel]
            Ed = Ec[dcol].dropna()
            dE = bmed(Ed, np.random.default_rng(SEED + 1))
            P(f"-- class {cn}: N_b {len(Ec)}, N_delta {len(Ed)}; delta_E {Ed.median():+.4f} [{ci(dE)[0]:+.4f}, {ci(dE)[1]:+.4f}]")
            if cons == "A" and cn == "all P":
                P(f"   delta_E without spec-z rescale (raw catalogue mass): {E['dA_raw'].median():+.4f}")
            for fn in FOOT:
                out = {}
                for lab in ("deg", "nat", "pub"):
                    Sb = S[f"b_{lab}_{fn}_1.5"].dropna() if f"b_{lab}_{fn}_1.5" in S else pd.Series(dtype=float)
                    if lab == "pub":
                        Sb = S[S.in_fit == True][f"b_pub_{fn}_1.5"].dropna()
                    m, (lo, hi), (dlo, dhi), dd = delta(Ec[f"b_{fn}_1.1"], Ed, Sb, Sd, SEED + 7)
                    out[lab] = dict(D=m, lo=lo, hi=hi, word=word(m, lo, hi), NSb=len(Sb),
                                    bE=float(Ec[f"b_{fn}_1.1"].median()), bS=float(Sb.median()),
                                    dE=float(Ed.median()), dS=float(Sd.median()), dEdS=dd, dEdS_lo=dlo, dEdS_hi=dhi)
                    P(f"   {fn:9s} SLACS sigma {lab}: b_E {out[lab]['bE']:+.4f}  b_S {out[lab]['bS']:+.4f} (N {len(Sb)})  "
                      f"dE-dS {dd:+.4f} [{dlo:+.4f}, {dhi:+.4f}]  -> Delta_b_common {m:+.4f} [{lo:+.4f}, {hi:+.4f}]  {out[lab]['word']}")
                w = out["deg"]["word"]
                if out["nat"]["word"] != w:
                    w = "NO VERDICT"
                out["WORD"] = w
                # per-lens form
                pe = (Ec[f"b_{fn}_1.1"] + Ec[dcol]).dropna()
                ps = (S[f"b_deg_{fn}_1.5"] + S[dcol]).dropna() if f"b_deg_{fn}_1.5" in S else pd.Series(dtype=float)
                if len(ps):
                    out["perlens"] = dict(E=float(pe.median()), NE=len(pe), S=float(ps.median()), NS=len(ps),
                                          D=float(pe.median() - ps.median()))
                    P(f"   {fn:9s} per-lens form: median(b+d) E {pe.median():+.4f} (N {len(pe)}), S {ps.median():+.4f} "
                      f"(N {len(ps)}), difference {pe.median() - ps.median():+.4f}")
                # seeing variants and Newton twin (primary sigma)
                Sd_ = Sd
                var = []
                for fe in (0.9, 1.3):
                    var.append((f"E seeing {fe}", delta(Ec[f"b_{fn}_{fe}"], Ed, S[f"b_deg_{fn}_1.5"].dropna(), Sd_, SEED + 7)[0]))
                for fs in (1.2, 1.8):
                    var.append((f"S seeing {fs}", delta(Ec[f"b_{fn}_1.1"], Ed, S[f"b_deg_{fn}_{fs}"].dropna(), Sd_, SEED + 7)[0]))
                var.append(("Newton (both)", delta(Ec[f"bN_{fn}"], Ed, S[f"bN_{fn}"].dropna(), Sd_, SEED + 7)[0]))
                var.append(("K6 Euclid Mcat x10^0.2", delta(Ec[f"bK6_{fn}"], Ed + 0.2, S[f"b_deg_{fn}_1.5"].dropna(), Sd_, SEED + 7)[0]))
                P("   " + fn + " variants: " + "; ".join(f"{a} {b:+.4f}" for a, b in var))
                out["variants"] = dict(var)
                if cn == "thetaE<1.3" and cons == "A":
                    known(f"K6_cancellation_{fn}", abs(out["variants"]["K6 Euclid Mcat x10^0.2"] - out["deg"]["D"]) <= 0.005,
                          f"{out['variants']['K6 Euclid Mcat x10^0.2'] - out['deg']['D']:+.5f}")
                P(f"   WORD {cons} {cn} {fn}: {w}")
                RES[cons].setdefault(cn, {})[fn] = out
    # ---------------- primary construction and the frozen word
    prim = "A" if RES.get("A", {}).get("minN") else ("B_W1" if RES.get("B_W1", {}).get("minN") else None)
    gates_ok = all(v["ok"] for v in KN.values())
    RES["primary"] = prim
    RES["known"] = KN
    P(f"\nknown answers all pass: {gates_ok}")
    for cn in cls:
        for fn in FOOT:
            w = RES[prim][cn][fn]["WORD"] if prim else "NOT EVALUABLE"
            P(f"FROZEN WORD (construction {prim}) class {cn} {fn}: {w}")
    # ---------------- EUC10 Part B reading (not a gate)
    if prim:
        dE = float(E[prim if prim == "A" else "dB_W1"].median()) if False else float(E["dA" if prim == "A" else "dB_W1"].median())
        dS_ = float(S["dA" if prim == "A" else "dB_W1"].median())
        P(f"\nREADING (not a gate): EUC10 Part B lensing numbers moved by delta_E(P) {dE:+.4f}, delta_S {dS_:+.4f}")
        for lab, (c, a) in (("AGEL DR2", (0.238, 0.220)), ("DESI SLF IV", (0.298, 0.282))):
            P(f"   {lab}: Euclid - SLACS on catalogue scales {c - 0.082:+.3f} / {a - 0.070:+.3f}; on common scale "
              f"{c + dE - 0.082 - dS_:+.3f} / {a + dE - 0.070 - dS_:+.3f}  (canonical / alt)")
    # matched subsample vs P
    mE = E.dropna(subset=["dA"])
    P(f"\nmatched (A) Euclid vs P: N {len(mE)}/{len(E)}; median z {mE.z.median():.3f}/{E.z.median():.3f}; "
      f"logMs {mE.logMs.median():.3f}/{E.logMs.median():.3f}; thetaE {mE.thetaE.median():.3f}/{E.thetaE.median():.3f}")
    P(f"spec-z rescale (log Ms rescaled - raw): median {np.median(E.logMs - E.logMs_raw):+.4f}, "
      f"range [{(E.logMs - E.logMs_raw).min():+.3f}, {(E.logMs - E.logMs_raw).max():+.3f}]")
    P(f"CIGALE chi2 (reduced?) median Euclid {mE.cig_chi2.median():.2f}, SLACS {S.cig_chi2.median():.2f}; "
      f"CIGALE LOGM_ERR median Euclid {mE.cig_logMerr.median():.3f}")
    P(f"SLACS: Re from I band for {int((S.Re_from == 'I').sum())}; SLACS b-side edges (deg, canonical): "
      f"{int((S.get('edge_deg_canonical_1.5', pd.Series(dtype=str)).dropna() != 'ok').sum())}")
    json.dump(RES, open(f"{HERE}/euc12_results{TAG}.json", "w"), indent=1, default=float)
    open(f"{HERE}/euc12{TAG}.out", "w").write("\n".join(LINES) + "\n")
    if MUT == "shift":
        base = json.load(open(f"{HERE}/euc12_results.json"))
        mv = {fn: RES[prim]["thetaE<1.3"][fn]["deg"]["D"] - base[prim]["thetaE<1.3"][fn]["deg"]["D"] for fn in FOOT}
        ok = all(abs(v + 0.20) <= 0.01 for v in mv.values())
        P(f"MUTATE shift: Delta moved by {mv} -> expected -0.20 +- 0.01: {ok}")
        open(f"{HERE}/euc12{TAG}.out", "w").write("\n".join(LINES) + "\n")
        sys.exit(1)
    sys.exit(0 if gates_ok else 2)


EMI = Emiles()

if __name__ == "__main__":
    main()
