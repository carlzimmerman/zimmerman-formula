#!/usr/bin/env python3
"""CFG229 -- inputs for the class-M sample: the class RULE in code (K1-K5), the Dunne+22 helium-convention checks (C2a-c), and the per-galaxy input tables split into a STATIC
file (no velocity values: the pre-flight reads only this) and a KINEMATICS file (the velocities and dispersions).
Compilation; conversions as published except one declared factor (He, x1.36 on Dunne's logMH2); calibration-limited; not a detection.  LambdaCDM has no a0.  kappa = 1/2 FITTED.
Frozen criteria: FROZEN_CRITERIA.md here (5c131c037), committed before any g_bar, g_obs, D or delta of this lane was computed.
Run: python3 campaign_fresh_gravity/CFG229_class_m_gold/cfg229_inputs.py        (MUTATE=1: +0.134 dex injected into Dunne's logMH2 -- the helium controls must fail)"""
import os, sys, math, re, json
sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from scipy.integrate import quad
from astropy.coordinates import SkyCoord
import astropy.units as u

LANE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(LANE))
MUT = os.environ.pop("MUTATE", "").strip() == "1"
DA = os.path.join(REPO, "data_assembly")
AT = os.path.join(DA, "arxiv_tables")
DU = os.path.join(DA, "multitracer_gas", "dunne2022")
SN = os.path.join(DA, "highz_literature_tables", "sins_ao")
OUT, CHK = [], []
HE = 1.36
LOGHE = math.log10(HE)
OM = 0.315


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


def kpc_per_arcsec(z, H0=67.4, Om=OM):                          # as CFG227
    c = 299792.458
    dc = c / H0 * quad(lambda x: 1 / math.sqrt(Om * (1 + x) ** 3 + 1 - Om), 0, z)[0]
    return dc / (1 + z) * 1e3 * math.pi / 648000.0


def nrm(s):
    return re.sub(r"[^A-Z0-9]", "", str(s).upper())


P(__doc__.split("Run:")[0].strip())
P(f"MUTATE = {'1 (+0.134 dex injected into every Dunne logMH2)' if MUT else 'none'}")

# ------------------------------------------------------------------ Dunne+22 (VizieR J/MNRAS/517/962, as parsed by the data chat)
M = pd.read_csv(os.path.join(DU, "dunne2022_master.csv"))
OPT = {k: pd.read_csv(os.path.join(DU, f"dunne2022_opt_{k}.csv")) for k in ("dax", "ad", "xa", "xd")}
NTR = {"dax": 3, "ad": 2, "xa": 2, "xd": 2}
if MUT:
    for k in OPT:
        OPT[k]["logMH2"] = OPT[k]["logMH2"] + LOGHE
cc = SkyCoord(M["RAJ2000"].astype(str).values, M["DEJ2000"].astype(str).values, unit=(u.hourangle, u.deg))
M["ra"], M["dec"] = cc.ra.deg, cc.dec.deg
Mc = SkyCoord(M["ra"].values * u.deg, M["dec"].values * u.deg)
P(f"\nDunne+22 master rows {len(M)}; optimisation tables {{{', '.join(f'{k}: {len(v)}' for k, v in OPT.items())}}}")


def dunne_pos(ra, dec, z, tol=2.0, dz=0.02):
    if not (math.isfinite(ra) and math.isfinite(dec) and math.isfinite(z)):
        return None
    sep = SkyCoord(ra * u.deg, dec * u.deg).separation(Mc).arcsec
    j = int(np.argmin(sep))
    if sep[j] <= tol and abs(float(M["z"].iloc[j]) - z) <= dz:
        return dict(name=str(M["Name"].iloc[j]), sep=float(sep[j]), dz=float(M["z"].iloc[j]) - z, how="position")
    return None


MN = [(nrm(a), nrm(b), nrm(c), float(z)) for a, b, c, z in zip(M["Name"], M["OName"], M["SimbadName"], M["z"])]


def dunne_name(name, z, dz=0.02):
    n = nrm(name)
    if len(n) < 5 or not math.isfinite(z):
        return None
    for j, (a, b, c, zz) in enumerate(MN):
        if abs(zz - z) > dz:
            continue
        if any(len(x) >= 5 and (n in x or x in n) for x in (a, b, c)):
            return dict(name=str(M["Name"].iloc[j]), sep=float("nan"), dz=zz - z, how="name")
    return None


def dunne_rows(dname):
    out = {}
    for k, t in OPT.items():
        r = t[t["Name"] == dname]
        if len(r):
            out[k] = (float(r["logMH2"].iloc[0]), float(r["e_logMH2"].iloc[0]) if "e_logMH2" in r and pd.notna(r["e_logMH2"].iloc[0]) else float("nan"))
    return out


# ------------------------------------------------------------------ tables
alp_s = pd.read_csv(os.path.join(AT, "alpaka1_sample.csv")).set_index("id")
alp_p = pd.read_csv(os.path.join(AT, "alpaka1_properties.csv")).set_index("id")
alp_k = pd.read_csv(os.path.join(AT, "alpaka1_kinematics.csv")).set_index("id")
alp_g = pd.read_csv(os.path.join(AT, "alpaka1_geometry.csv")).set_index("id")
alp_o = pd.read_csv(os.path.join(AT, "alpaka1_alma_obs.csv")).set_index("id")
alp_u = pd.read_csv(os.path.join(AT, "alpaka1_digitised", "alpaka1_outer_summary.csv")).set_index("id")
alp_d = pd.read_csv(os.path.join(AT, "alpaka1_digitised", "alpaka1_vrot_digitised.csv"))
sn1 = pd.read_csv(os.path.join(SN, "sins_ao_table1_sample.csv")).set_index("source")
sn6 = pd.read_csv(os.path.join(SN, "sins_ao_table6_kinematics.csv")).set_index("source")
am_b = pd.read_csv(os.path.join(AT, "amvrosiadis_bestfit.csv"), dtype={"alessid": str}).set_index("alessid")
am_p = pd.read_csv(os.path.join(AT, "amvrosiadis_parent.csv"), dtype={"alessid": str}).set_index("alessid")
cr_s = pd.read_csv(os.path.join(AT, "cristal2025_sample.csv"))
cr_d = pd.read_csv(os.path.join(AT, "cristal2025_dynamics.csv"), dtype={"id": str}).set_index("id")
ro_s = pd.read_csv(os.path.join(AT, "romanoliveira2023_sample.csv"))
rc = pd.read_csv(os.path.join(DA, "rc100_provenance", "rc100_table3_six_fields_paper_values.csv"))
km = pd.read_csv(os.path.join(DA, "kmos3d_phibss", "kmos3d_catalog.csv"), low_memory=False)


def fnum(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else float("nan")
    except Exception:
        return float("nan")


def sexa(ra, dec):
    try:
        d = re.sub(r"[\[\]\s]", "", str(dec))
        c = SkyCoord(f"{str(ra).strip()} {d}", unit=(u.hourangle, u.deg))
        return float(c.ra.deg), float(c.dec.deg)
    except Exception:
        return float("nan"), float("nan")


# ------------------------------------------------------------------ the candidate pool (every kinematic table the record holds with a name or a position)
POOL = []


def add(**k):
    POOL.append(k)


for gid in alp_s.index:
    mst, emst = fnum(alp_p.loc[gid, "mstar_1e10msun"]), fnum(alp_p.loc[gid, "e_mstar"])
    k1 = bool(math.isfinite(mst) and math.isfinite(emst) and emst < mst)                      # the paper calls M* with error >= value 'not statistically meaningful'
    k2 = bool(gid in alp_k.index and gid in alp_u.index and math.isfinite(fnum(alp_k.loc[gid, "vext_kms"])) and not isinstance(alp_k.loc[gid, "vext_lim"], str))
    add(set="ALPAKA", id=str(gid), name=str(alp_s.loc[gid, "name"]), ra=fnum(alp_s.loc[gid, "ra_deg"]), dec=fnum(alp_s.loc[gid, "dec_deg"]), z=fnum(alp_s.loc[gid, "z"]), K1=k1, K2=k2, K5=True, route="STARDUST SED M*; gas not adopted")
for s in sn1.index:
    ra, dec = sexa(sn1.loc[s, "ra"], sn1.loc[s, "dec"])
    k1 = bool(math.isfinite(fnum(sn1.loc[s, "Mstar_1e10Msun"])))
    k2 = bool(s in sn6.index and math.isfinite(fnum(sn6.loc[s, "Vc_kms"])) and math.isfinite(fnum(sn6.loc[s, "Re_kpc"])))
    add(set="SINS", id=str(s), name=str(s), ra=ra, dec=dec, z=fnum(sn1.loc[s, "z_Halpha"]), K1=k1, K2=k2, K5=True, route="BC03 SED M*; V_c at R_e")
for a in am_b.index:
    pz = fnum(am_p.loc[a, "z"])
    add(set="S1", id=str(a), name="ALESS" + str(a).split(".")[0], ra=float("nan"), dec=float("nan"), z=pz, K1=bool(math.isfinite(fnum(am_p.loc[a, "logMstar"]))), K2=bool(math.isfinite(fnum(am_b.loc[a, "vcirc_2re_kms"]))), K5=True, route="MAGPHYS M*; V_circ(2 r_e) (gas replaced)")
for _, r in cr_s.iterrows():
    cid = str(r["id"])
    add(set="CRISTAL", id=cid, name=str(r["name"]), ra=fnum(r["ra_deg"]), dec=fnum(r["dec_deg"]), z=fnum(r["z_cii"]), K1=bool(math.isfinite(fnum(r["logMstar"]))), K2=bool(cid in cr_d.index), K5=False, route="DysmalPy fit: baryon mass fitted with the dynamics (class D by K5)")
for _, r in rc.iterrows():
    add(set="RC100", id=str(int(r["idx"])), name=str(r["name"]), ra=float("nan"), dec=float("nan"), z=fnum(r["z"]), K1=True, K2=True, K5=False, route="M_bary fitted (SED + scaling-gas prior, three-method f_DM): class D by K5")
for _, r in ro_s.iterrows():
    ra, dec = sexa(r["ra"], r["dec"])
    add(set="RomanOliveira", id=str(r["id"]), name=str(r["id"]), ra=ra, dec=dec, z=fnum(r["z"]), K1=False, K2=True, K5=True, route="no SED stellar mass in the paper")
add(set="Lelli23", id="zC-400569", name="zC-400569", ra=float("nan"), dec=float("nan"), z=2.24, K1=True, K2=True, K5=False, route="free-normalisation mass models: class D by K5")
for _, r in km.iterrows():
    add(set="KMOS3D", id=str(r["ID"]), name=str(r["ID"]), ra=fnum(r["RA"]), dec=fnum(r["DEC"]), z=fnum(r["Z"]), K1=bool(math.isfinite(fnum(r["LMSTAR"]))), K2=False, K5=True, route="catalogue only: no tabulated velocity at a stated radius")
P(f"\nCandidate pool: {len(POOL)} entries; by set {dict(pd.Series([p['set'] for p in POOL]).value_counts())}")


def classify(pool, dec_shift_arcsec=0.0, z_scale=1.0):
    res = []
    for p in pool:
        z = p["z"] * z_scale
        k4 = bool(math.isfinite(z) and z >= 2.0)
        m = None
        if math.isfinite(p["ra"]) and math.isfinite(p["dec"]):
            m = dunne_pos(p["ra"], p["dec"] + dec_shift_arcsec / 3600.0, z)
        elif p["set"] in ("S1", "RC100", "Lelli23"):
            m = dunne_name(p["name"], z)
        k3 = bool(m is not None and len(dunne_rows(m["name"])) > 0)
        res.append(dict(p, K3=k3, K4=k4, match=m, M=bool(p["K1"] and p["K2"] and k3 and k4 and p["K5"])))
    return res


CL = classify(POOL)
hits = [c for c in CL if c["K3"] and c["K4"]]
P("\nCLASS RULE (K1 SED M*; K2 velocity at a stated radius; K3 a Dunne+22 per-galaxy optimised-conversion row by position <= 2 arcsec and |dz| <= 0.02 or, for tables without coordinates, by name; K4 z >= 2; K5 baryons not fitted with the dynamics)")
P("  candidates with a Dunne match at z >= 2 and their decision path:")
for c in hits:
    mm = c["match"]
    P(f"    {c['set']:13s} {c['id']:13s} {c['name'][:22]:22s} z={c['z']:.3f} <-> {mm['name']:9s} ({mm['how']}{'' if mm['how'] == 'name' else f', sep {mm['sep']:.2f} arcsec'}, dz {mm['dz']:+.3f}) tables {list(dunne_rows(mm['name']))}  K1={c['K1']} K2={c['K2']} K5={c['K5']} => {'CLASS M' if c['M'] else 'not class M (' + c['route'] + ')'}")
SEL = [c for c in CL if c["M"]]
WANT = [("ALPAKA", "15"), ("ALPAKA", "18"), ("ALPAKA", "19"), ("ALPAKA", "20"), ("ALPAKA", "22"), ("SINS", "Q2343-BX610"), ("S1", "122.1")]
got = sorted((c["set"], c["id"]) for c in SEL)
check("C0 the rule returns exactly the expected seven (H1)", f"{got}", got == sorted(WANT))
neg = classify(POOL, dec_shift_arcsec=30.0)
npos = sum(1 for c in neg if c["K3"] and c["match"]["how"] == "position")
check("C0n negative control: +30 arcsec on every declination gives ZERO positional Dunne matches", f"{npos}", npos == 0)
zoff = classify(POOL, z_scale=1.05)
nzo = sum(1 for c in zoff if c["match"] is not None and c["match"]["how"] == "position")
check("C0z redshift control: z x 1.05 (|dz| ~ 0.11) removes every positional match", f"{nzo}", nzo == 0)

# ------------------------------------------------------------------ the helium convention (C2a-c)
P("\nDUNNE+22 CONVENTION (the paper: its M_mol columns carry a factor 1.36 for He; Table 10 lists M_H2 and M_mol separately: ad (326) alpha_CO 3.2 for M_H2 against 4.3 for M_mol; daX (101) 2.6 and 3.5)")
Mm = M.drop_duplicates("Name").set_index("Name")
okc = {}
for k in ("ad", "dax", "xa"):
    d = OPT[k]
    lco = d["logLCO"] if "logLCO" in d.columns else d["Name"].map(Mm["logLCO"])
    res = np.log10(d["aCO"]) + lco - d["logMH2"]
    use = res.notna() & (d["JCorr"] == 0)
    nj = int((d["JCorr"] != 0).sum())
    if MUT:
        pass
    okc[k] = (int(use.sum()), float(res[use].abs().max()), int((res[use].abs() <= 0.005).sum()))
    jc = d["JCorr"] != 0
    rj = (res[jc & res.notna()] + d["JCorr"][jc & res.notna()])
    P(f"  {k}: JCorr = 0 rows {int(use.sum())}: max |logMH2 - (log aCO + logLCO)| = {okc[k][1]:.4f}; rows with JCorr != 0: {nj} (descriptive: residual + JCorr has max |.| {float(rj.abs().max()) if len(rj) else float('nan'):.4f}, i.e. the aperture correction is added)")
check("C2a in every CO-based Dunne row with JCorr = 0, logMH2 = log aCO + logLCO to 0.005 dex", f"{sum(v[2] for v in okc.values())} of {sum(v[0] for v in okc.values())} rows", all(v[2] == v[0] for v in okc.values()))
d = OPT["xd"]
res = d["logLCI"] + d["aCI"] - LOGHE - d["logMH2"]
use = res.notna() & (d["JCorr"] == 0)
check("C2b in every opt_xd row with JCorr = 0, logMH2 = logLCI + aCI - log10(1.36) to 0.005 dex (aCI = log alpha_CI with He; logMH2 without)", f"{int((res[use].abs() <= 0.005).sum())} of {int(use.sum())} rows (max {float(res[use].abs().max()):.4f})", bool((res[use].abs() <= 0.005).all()))
med = {k: float(OPT[k]["aCO"].median()) for k in ("ad", "dax")}
check("C2c the median aCO of opt_ad is within 0.4 of Table 10's M_H2-column value 3.2 and more than 0.7 from its M_mol-column value 4.3", f"median {med['ad']:.3f} (daX median {med['dax']:.3f} against Table 10's 2.6 for M_H2 and 3.5 for M_mol)", abs(med["ad"] - 3.2) < 0.4 and abs(med["ad"] - 4.3) > 0.7)
P(f"  => Dunne's logMH2 is M_H2 WITHOUT helium; the gravitating gas is 1.36 x 10^logMH2 (+{LOGHE:.4f} dex).  HI is neglected (the master's HI/H2 column is empty for all seven).")

# ------------------------------------------------------------------ per-galaxy inputs
STAT, KIN = [], []


def pick_table(dname):
    rows = dunne_rows(dname)
    best = sorted(rows.items(), key=lambda kv: (-NTR[kv[0]], kv[1][1] if math.isfinite(kv[1][1]) else 9.0))[0]
    return best[0], best[1], rows


def beam_of(gid):
    return math.sqrt(float(alp_o.loc[gid, "beam_major_arcsec"]) * float(alp_o.loc[gid, "beam_minor_arcsec"]))


P("\nPER-GALAXY INPUTS (static = no velocity values; the pre-flight reads only the static file)")
for c in SEL:
    st, kn = {}, {}
    gname = c["match"]["name"]
    tab, (lmh, elmh), rows = pick_table(gname)
    if c["set"] == "ALPAKA":
        gid = int(c["id"])
        z = float(alp_s.loc[gid, "z"])
        Ms = float(alp_p.loc[gid, "mstar_1e10msun"]) * 1e10
        eMs = float(alp_p.loc[gid, "e_mstar"]) * 1e10
        rext, redash = float(alp_u.loc[gid, "R_ext_kpc"]), fnum(alp_u.loc[gid, "Re_kpc_dashed_line"])
        re_, rule = (redash, "dashed optical R_e") if math.isfinite(redash) else (rext / 1.2, "R_ext/1.2")
        V, ehi, elo = (float(alp_k.loc[gid, k]) for k in ("vext_kms", "vext_errhi", "vext_errlo"))
        sg, sghi, sglo = (float(alp_k.loc[gid, k]) for k in ("sigma_ext_kms", "sigma_ext_errhi", "sigma_ext_errlo"))
        g = alp_g.loc[gid]
        ih, eih = float(g["i_hst"]), 0.5 * (float(g["e1.1"]) + float(g["e2.1"]))
        ia, eia = float(g["i_alma"]), 0.5 * (float(g["e1.3"]) + float(g["e2.3"]))
        which = "ALMA" if (gid in (3, 22) or not math.isfinite(ih)) else "HST"
        iu, eiu, ialt = (ia, eia, ih) if which == "ALMA" else (ih, eih, ia)
        dg = alp_d[(alp_d["id"] == gid) & (alp_d["panel"] == "V")].sort_values("R_kpc")
        ring = dg.iloc[-1]
        rmean = float(dg["R_kpc"].iloc[-2:].mean())
        agn = "AGN" in str(alp_s.loc[gid, "notes"])
        st.update(gid=f"ALPAKA{gid}", set="ALPAKA", name=str(alp_s.loc[gid, "name"]), z=z, R_kpc=rext, Re_kpc=re_, Re_rule=rule, Mstar=Ms, e_logMstar_inner=eMs / (Ms * math.log(10)),
                  sigV_dex=2 * 0.4343 * 0.5 * (ehi + elo) / V, i_used=iu, e_i_used=eiu, i_alt=ialt, i_which=which, agn=agn, beam_arcsec=beam_of(gid), R_over_beam=(rext / kpc_per_arcsec(z)) / beam_of(gid),
                  mstar_route="STARDUST SED (Kokorev+21), Chabrier, AGN torus templates for AGN hosts", v_route="3D tilted ring (BBarolo) V_ext = mean of last two rings, inclination fixed (i_used)")
        kn.update(gid=st["gid"], V_pub=V, V_noP=V, alpha_pub=0.0, eV_hi=ehi, eV_lo=elo, sigma=sg, e_sigma=0.5 * (sghi + sglo), V_ring=float(ring["value_kms"]), R_ring_kpc=float(ring["R_kpc"]),
                  V_ring_band_hi=float(ring["band_hi_kms"]), V_ring_band_lo=float(ring["band_lo_kms"]), R_mean_last2_kpc=rmean)
    elif c["set"] == "SINS":
        s = c["id"]
        z = float(sn1.loc[s, "z_Halpha"])
        Ms = float(sn1.loc[s, "Mstar_1e10Msun"]) * 1e10
        re_ = float(sn6.loc[s, "Re_kpc"])
        V = float(sn6.loc[s, "Vc_kms"]); ehi, elo = float(sn6.loc[s, "Vc_kms_errhi"]), float(sn6.loc[s, "Vc_kms_errlo"])
        st.update(gid="SINS_BX610", set="SINS", name=s, z=z, R_kpc=re_, Re_kpc=re_, Re_rule="Table 6 R_e", Mstar=Ms, e_logMstar_inner=0.2, sigV_dex=2 * 0.4343 * 0.5 * (ehi + elo) / V,
                  i_used=float(np.degrees(np.arcsin(float(sn6.loc[s, "sin_i"])))), e_i_used=float("nan"), i_alt=float("nan"), i_which="fitted (inside the V_c Monte Carlo errors)", agn=(str(sn1.loc[s, "notes"]).strip() not in ("", "nan")),
                  beam_arcsec=float(pd.read_csv(os.path.join(SN, "sins_ao_table2_observations.csv")).set_index("source").loc[s, "res_arcsec"]), R_over_beam=float("nan"),
                  mstar_route="BC03 SED, Chabrier, solar Z, Calzetti, constant or declining SFH; paper adopts 0.2 dex", v_route="Halpha AO: V_rot sin i = C_PSF dv_obs/2; V_c = (V_rot^2 + 3.36 sigma_0^2)^0.5 at R_e (Eqs 1-2)")
        st["R_over_beam"] = re_ / kpc_per_arcsec(z) / st["beam_arcsec"]
        kn.update(gid=st["gid"], V_pub=V, V_noP=float(sn6.loc[s, "Vrot_kms"]), alpha_pub=3.36, eV_hi=ehi, eV_lo=elo, sigma=float(sn6.loc[s, "sigma0_kms"]), e_sigma=0.5 * (float(sn6.loc[s, "sigma0_kms_errhi"]) + float(sn6.loc[s, "sigma0_kms_errlo"])),
                  V_ring=float("nan"), R_ring_kpc=float("nan"), V_ring_band_hi=float("nan"), V_ring_band_lo=float("nan"), R_mean_last2_kpc=float("nan"))
    else:
        a = c["id"]
        z = float(am_p.loc[a, "z"])
        Ms = 10 ** float(am_p.loc[a, "logMstar"])
        eM = 0.5 * (float(am_p.loc[a, "logMstar_errhi"]) + float(am_p.loc[a, "logMstar_errlo"]))
        re_ = float(am_b.loc[a, "re_arcsec"]) * kpc_per_arcsec(z)
        V, ehi, elo = float(am_b.loc[a, "vcirc_2re_kms"]), float(am_b.loc[a, "vcirc_2re_kms_errhi"]), float(am_b.loc[a, "vcirc_2re_kms_errlo"])
        st.update(gid="ALESS_122.1", set="S1", name="ALESS 122.1", z=z, R_kpc=2 * re_, Re_kpc=re_, Re_rule="r_e (CO size) x kpc/arcsec", Mstar=Ms, e_logMstar_inner=eM, sigV_dex=2 * 0.4343 * 0.5 * (ehi + elo) / V,
                  i_used=float(am_b.loc[a, "inc_deg"]), e_i_used=float("nan"), i_alt=float("nan"), i_which="fitted (inside the V_circ posterior)", agn=False, beam_arcsec=float("nan"), R_over_beam=float("nan"),
                  mstar_route="MAGPHYS (da Cunha+15), Chabrier; the source table's gas (Calistro Rivera+18) is replaced by Dunne's", v_route="visibility-space kinematic model, V_circ at 2 r_e")
        kn.update(gid=st["gid"], V_pub=V, V_noP=V, alpha_pub=0.0, eV_hi=ehi, eV_lo=elo, sigma=float(am_b.loc[a, "sigma_kms"]), e_sigma=0.5 * (float(am_b.loc[a, "sigma_kms_errhi"]) + float(am_b.loc[a, "sigma_kms_errlo"])),
                  V_ring=float("nan"), R_ring_kpc=float("nan"), V_ring_band_hi=float("nan"), V_ring_band_lo=float("nan"), R_mean_last2_kpc=float("nan"))
    st.update(dunne_name=gname, dunne_table=tab, n_tracers=NTR[tab], logMH2=lmh, e_logMH2=elmh, logMgas_He=lmh + LOGHE,
              logMH2_ad=rows.get("ad", (float("nan"),))[0], logMH2_dax=rows.get("dax", (float("nan"),))[0], logMH2_xa=rows.get("xa", (float("nan"),))[0], logMH2_xd=rows.get("xd", (float("nan"),))[0],
              match_how=c["match"]["how"], match_sep_arcsec=c["match"]["sep"], match_dz=c["match"]["dz"])
    STAT.append(st); KIN.append(kn)
    P(f"  {st['gid']:12s} z={st['z']:.3f} R={st['R_kpc']:.2f} kpc R_e={st['Re_kpc']:.2f} ({st['Re_rule']}) log M*={math.log10(st['Mstar']):.2f} (+-{st['e_logMstar_inner']:.2f}; {st['mstar_route'][:48]}) "
      f"Dunne {st['dunne_name']} [{tab}, {st['n_tracers']} tracers] logMH2={lmh:.3f}+-{elmh:.3f} -> log M_gas(He) {lmh + LOGHE:.3f}; i_used {st['i_used']:.0f} ({st['i_which']}); AGN {st['agn']}; R/beam {st['R_over_beam']:.2f}")
order = {"ALPAKA15": 0, "ALPAKA18": 1, "ALPAKA19": 2, "ALPAKA20": 3, "ALPAKA22": 4, "SINS_BX610": 5, "ALESS_122.1": 6}
STAT.sort(key=lambda d: order.get(d["gid"], 99)); KIN.sort(key=lambda d: order.get(d["gid"], 99))
bx = [d for d in STAT if d["gid"] == "SINS_BX610"]
if bx:
    P("\nBX610 gas-table sensitivity (logMH2, no He): " + ", ".join(f"{k} {bx[0]['logMH2_' + k]:.3f}" for k in ("dax", "ad", "xa", "xd")))
sdf, kdf = pd.DataFrame(STAT), pd.DataFrame(KIN)
sdf.to_csv(os.path.join(LANE, "cfg229_inputs_static" + ("_MUTATE" if MUT else "") + ".csv"), index=False, float_format="%.10g")
kdf.to_csv(os.path.join(LANE, "cfg229_inputs_kin" + ("_MUTATE" if MUT else "") + ".csv"), index=False, float_format="%.10g")
P(f"\nwrote cfg229_inputs_static{'_MUTATE' if MUT else ''}.csv ({len(sdf)} rows, columns: {', '.join(sdf.columns[:12])} ...) and cfg229_inputs_kin{'_MUTATE' if MUT else ''}.csv ({len(kdf)} rows)")
kin_vals = {}
for _, r in kdf.iterrows():
    kin_vals[r["gid"]] = [float(r[c]) for c in ("V_pub", "V_noP", "sigma", "V_ring", "V_ring_band_hi", "V_ring_band_lo") if pd.notna(r[c])]
leak = [(r["gid"], c) for _, r in sdf.iterrows() for c in sdf.columns if isinstance(r[c], (int, float, np.floating)) and pd.notna(r[c]) and any(abs(float(r[c]) - v) < 1e-6 * max(1.0, abs(v)) for v in kin_vals[r["gid"]])]
check("blindness of the static file: no numeric static entry equals any velocity or dispersion value of its own galaxy (value-level test)", f"{len(leak)} coincidences {leak}", len(leak) == 0)
import hashlib
for fn in ("cfg229_inputs_static", "cfg229_inputs_kin"):
    fp = os.path.join(LANE, fn + ("_MUTATE" if MUT else "") + ".csv")
    P(f"  sha256 {os.path.basename(fp)}: {hashlib.sha256(open(fp, 'rb').read()).hexdigest()[:16]}")
P(f"\n{sum(CHK)}/{len(CHK)} checks pass")
open(os.path.join(LANE, "cfg229_inputs" + ("_MUTATE" if MUT else "") + ".out"), "w").write("\n".join(OUT).replace(REPO, "<repo>") + "\n")
sys.exit(0 if all(CHK) else 1)
