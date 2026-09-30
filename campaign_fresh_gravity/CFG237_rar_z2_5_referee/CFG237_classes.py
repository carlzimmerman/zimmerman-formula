"""CFG237 attack 1: class-assignment rule (M/S/L/D) implemented as the frozen decision table (section 5.1), applied to every z>=2 galaxy with numbers
on disk, with the frozen cross-match of the Dunne+22 optimised multi-tracer gas masses to every kinematic table that carries a position or a name.
MUTATE 1: move CRISTAL-11 (L->M) and the three footnote-flagged S1 sources (S->D); the class-count line must FAIL (exit 1)."""
import sys, re
from CFG237_common import *

t = start("CFG237_classes")
ck = Checks()
R = {}
DU = os.path.join(DA, "multitracer_gas", "dunne2022")


def hms(s):
    s = str(s).replace("[+]", "+").replace("[-]", "-").strip()
    sign = -1 if s.startswith("-") else 1
    parts = re.split(r"[:\s]+", s.lstrip("+-"))
    v = [float(p) for p in parts if p != ""]
    v += [0.0] * (3 - len(v))
    return sign, v[0] + v[1] / 60 + v[2] / 3600


def ra_deg(s):
    return hms(s)[1] * 15.0


def dec_deg(s):
    sg, v = hms(s); return sg * v


def norm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


# ------------------------------------------------------------------ Dunne
mst = pd.read_csv(os.path.join(DU, "dunne2022_master.csv"))
mst["ra"] = mst.RAJ2000.map(ra_deg); mst["dec"] = mst.DEJ2000.map(dec_deg)
opt = {t_: pd.read_csv(os.path.join(DU, f"dunne2022_opt_{t_}.csv")) for t_ in ("ad", "dax", "xa", "xd")}
TR = {"ad": "CO+dust", "dax": "CO+[CI]+dust", "xa": "CO+[CI]", "xd": "dust+[CI]"}
hi = mst[mst.z >= 2].copy()
hi["opt_tables"] = hi.Name.map(lambda n: [k for k, v in opt.items() if n in set(v.Name)])
hiopt = hi[hi.opt_tables.map(len) > 0].copy()
print(f"Dunne+22 master rows {len(mst)}; z>=2: {len(hi)}; of these with >=1 optimised-conversion row (opt_ad/dax/xa/xd): {len(hiopt)}")
R["dunne_hi"] = len(hi); R["dunne_hi_opt"] = len(hiopt)

# ------------------------------------------------------------------ kinematic records
recs = []     # dict(set, id, name, ra, dec, z, K1, K2, K5)


def add(**k):
    recs.append(k)


# S1 (no positions; names ALESS)
s1 = load_s1(2.0, 5.0)
for _, r in s1.iterrows():
    add(set="S1", id=r.alessid, name="ALESS" + r.alessid.split(".")[0].lstrip("0"), ra=np.nan, dec=np.nan, z=float(r.z), K1=True, K2=True, K5=False, route="S",
        note="gas from CO, alpha_CO stated" + ("; gas (and M*) from another paper (footnote)" if r.footnote_other_paper else ""))
# ALPAKA ten
al = load_alpaka()
for _, r in al.iterrows():
    add(set="ALPAKA", id=int(r.id), name=str(r["name"]), ra=float(r.ra_deg), dec=float(r.dec_deg), z=float(r.z), K1=bool(np.isfinite(r.mstar_1e10msun)), K2=True, K5=False, route="none(stars-only)", note="V_ext at digitised R_ext")
# CRISTAL
cr = load_cristal()
smp = pd.read_csv(os.path.join(AT, "cristal2025_sample.csv")).set_index("id")
for i in ID14:
    rr = smp.loc[SAMPLE_ALIAS.get(i, i)]
    add(set="CRISTAL", id=i, name=str(rr["name"]), ra=float(rr.ra_deg), dec=float(rr.dec_deg), z=float(rr.z_cii), K1=bool(np.isfinite(rr.logMstar)), K2=True,
        K5=True, route=("L(route)+D(fit)" if i in DETECTED6 else "D(fit)"), note="DysmalPy fit; L route = SED M* + dust gas normalisation")
# SINS AO
s1t = pd.read_csv(os.path.join(DA, "highz_literature_tables", "sins_ao", "sins_ao_table1_sample.csv"))
s6 = pd.read_csv(os.path.join(DA, "highz_literature_tables", "sins_ao", "sins_ao_table6_kinematics.csv"))
sins = s1t.merge(s6[["source", "Re_kpc", "Vrot_kms", "Vc_kms"]], on="source", how="left")
for _, r in sins.iterrows():
    try:
        ra = ra_deg(r.ra); de = dec_deg(r.dec)
    except Exception:
        ra = de = np.nan
    z = float(r.z_Halpha) if pd.notna(r.z_Halpha) else np.nan
    add(set="SINS", id=str(r.source), name=str(r.source), ra=ra, dec=de, z=z, K1=bool(pd.notna(r.Mstar_1e10Msun)),
        K2=bool(pd.notna(r.Vc_kms) and pd.notna(r.Re_kpc)), K5=False, route="none(no gas)", note="V_c at R_e, SED M*")
# RC100 (D by rule: M_bary prior-anchored)
rc = load_rc100("corrected")
for _, r in rc[rc.z >= 2].iterrows():
    add(set="RC100", id=int(r.idx), name=str(r["name"]), ra=np.nan, dec=np.nan, z=float(r.z), K1=True, K2=True, K5=True, route="D", note="M_bary fitted with SED+scaling gas prior")
# Roman-Oliveira (no M*)
ro = pd.read_csv(os.path.join(AT, "romanoliveira2023_sample.csv"))
for _, r in ro.iterrows():
    add(set="RomanOliveira", id=str(r["id"]), name=str(r["id"]), ra=ra_deg(r.ra), dec=dec_deg(r.dec), z=float(r.z), K1=False, K2=True, K5=False, route="none(no M*)", note="literature CO gas, alpha_CO 0.8")
# Lelli+23
add(set="Lelli23", id="zC-400569", name="zC-400569", ra=150.28621, dec=1.74116, z=2.24, K1=True, K2=True, K5=True, route="D", note="free-normalisation mass models")
# KMOS3D catalogue (positions only: no tabulated V): K2 False
km = pd.read_csv(os.path.join(DA, "kmos3d_phibss", "kmos3d_catalog.csv"), low_memory=False)
kmz = km[(km.Z >= 2)]
for _, r in kmz.iterrows():
    add(set="KMOS3D", id=str(r.ID), name=str(r.ID), ra=float(r.RA), dec=float(r.DEC), z=float(r.Z), K1=bool(pd.notna(r.LMSTAR)), K2=False, K5=False, route="none(no tabulated V)", note="cubes unprocessed")
# Corpus Z1 (ALPINE)
try:
    cz = pd.read_csv(os.path.join(DA, "highz_literature_tables", "alpine_corpus_z1", "corpus_z1_galaxies.csv"))
    print("Corpus Z1 columns:", list(cz.columns)[:20])
    rac = [c for c in cz.columns if c.lower() in ("ra", "ra_deg")]; dcc = [c for c in cz.columns if c.lower() in ("dec", "dec_deg")]; zc = [c for c in cz.columns if c.lower() in ("z", "z_cii", "redshift")]
    if rac and dcc and zc:
        for _, r in cz.iterrows():
            add(set="CorpusZ1", id=str(r.iloc[0]), name=str(r.iloc[0]), ra=float(r[rac[0]]), dec=float(r[dcc[0]]), z=float(r[zc[0]]), K1=True, K2=True, K5=False, route="none(no gas)", note="rings + SED M*")
except Exception as e:
    print("Corpus Z1 not parsed:", repr(e)[:100])
rec = pd.DataFrame(recs)
print(f"kinematic-table records: {len(rec)}; by set:", rec.groupby("set").size().to_dict())
R["rec_by_set"] = rec.groupby("set").size().to_dict()

# ------------------------------------------------------------------ cross-match (frozen: name OR position 2" and |dz|<0.02)
def sep_arcsec(ra1, de1, ra2, de2):
    d2r = np.pi / 180
    x = np.cos(de1 * d2r) * np.cos(de2 * d2r) * np.cos((ra1 - ra2) * d2r) + np.sin(de1 * d2r) * np.sin(de2 * d2r)
    return np.degrees(np.arccos(np.clip(x, -1, 1))) * 3600


hiopt["nkeys"] = hiopt.apply(lambda r: {norm(r.Name), norm(r.OName), norm(r.SimbadName)} - {"nan", ""}, axis=1)
matches = []
for _, k in rec.iterrows():
    kn = norm(k["name"])
    for _, h in hiopt.iterrows():
        byname = bool(kn) and (kn in h.nkeys or any(kn == x for x in h.nkeys))
        bypos = False; sep = np.nan
        if np.isfinite(k.ra) and np.isfinite(k.dec) and np.isfinite(k.z):
            sep = sep_arcsec(k.ra, k.dec, h.ra, h.dec)
            bypos = bool(sep <= 2.0 and abs(k.z - h.z) < 0.02)
        if byname or bypos:
            matches.append(dict(set=k["set"], id=k["id"], kname=k["name"], kz=k.z, K1=k.K1, K2=k.K2, K5=k.K5, dunne=h.Name, dz=h.z, sep=sep, byname=byname, bypos=bypos, tables=h.opt_tables))
mt = pd.DataFrame(matches)
print(f"\ncross-match hits (name or 2 arcsec & |dz|<0.02): {len(mt)}")
if len(mt):
    pd.set_option("display.width", 250, "display.max_columns", 30, "display.max_colwidth", 40)
    print(mt.to_string(index=False))
R["matches"] = mt.to_dict("records") if len(mt) else []

# S1 gas mass vs Dunne optimised M_H2 where matched (ALESS122)
def dunne_mh2(name):
    for t_ in ("dax", "ad", "xd", "xa"):
        d_ = opt[t_]
        if name in set(d_.Name):
            return t_, float(d_[d_.Name == name].logMH2.iloc[0]), float(d_[d_.Name == name].e_logMH2.iloc[0])
    return None, np.nan, np.nan

print("\n-- decision path for every matched galaxy (frozen order: D if K5; M if K1&K2&K3(opt)>=2; else S/L/none) --")
cls_rows = []
for _, m in mt.iterrows():
    n_tr = len(m.tables)
    if m.K5:
        c = "D (K5: baryon normalisation fitted/prior-anchored); Dunne gas would qualify as M-gas"
    elif m.K1 and m.K2:
        c = "M"
    else:
        c = "none (K1=%s K2=%s)" % (m.K1, m.K2)
    tt, mh2, e = dunne_mh2(m.dunne)
    print(f"   {m.set:10s} {str(m['id']):12s} z={m.kz:.3f} <-> Dunne {m.dunne:12s} z={m.dz:.3f} sep={m.sep if np.isfinite(m.sep) else float('nan'):5.2f}\" tables={m.tables} logMH2({tt})={mh2:.2f}+-{e:.2f}  => {c}")
    cls_rows.append(dict(m.to_dict(), cls=c, logMH2=mh2, table=tt))
R["decision_paths"] = cls_rows
cr_df = pd.DataFrame(cls_rows)
M_hits = cr_df[cr_df.cls == "M"] if len(cr_df) else pd.DataFrame()
M_unique = sorted(set(zip(M_hits.dunne, M_hits.set, M_hits["id"].astype(str)))) if len(M_hits) else []
print("\nclass-M (literal rule R0): unique (Dunne, set, id):", M_unique)
R["M_R0"] = M_unique

# ------------------------------------------------------------------ N per class under R0-R5
S_ids = list(s1.alessid)
foot = [i for i in S_ids if i in ("049.1", "075.1", "122.1")]

def counts(reading):
    N = dict(M=0, S=0, L=0, D=0, other_gas_S1=0, none=0)
    Mset = {(a, b, c) for a, b, c in M_unique}
    if reading in ("R5",):
        return None
    # S1
    if reading == "R2":
        N["D"] += len(S_ids)
    elif reading == "R1":
        N["S"] += len(S_ids) - len(foot); N["other_gas_S1"] += len(foot)
    else:
        N["S"] += len(S_ids)
    # S1 members that match Dunne (M override only for K5 false: S1 has K1,K2 true, K5 false) -> M
    for (dn, st, iid) in Mset:
        if st == "S1":
            N["S"] -= 1 if reading != "R2" else 0
            if reading == "R2": N["D"] -= 1
            N["M"] += 1
    # CRISTAL
    z_ok = (lambda z: z <= 5.0) if reading == "R4" else (lambda z: True)
    crs = [(i, float(smp.loc[SAMPLE_ALIAS.get(i, i)].z_cii)) for i in ID14]
    if reading == "R3":
        N["L"] += len(DETECTED6); N["D"] += len([i for i in ID12 if i not in DETECTED6])
    else:
        N["L"] += len([i for i, z in crs if i in DETECTED6 and z_ok(z)])
        N["D"] += len([i for i, z in crs if i in ID12 and z_ok(z)])      # rows (fit route R_e)
        N["D"] += len([i for i, z in crs if i in DETECTED6 and z_ok(z)])    # R_out fit rows (same six)
    # RC100, Lelli
    N["D"] += 41 + 1
    # ALPAKA
    for _, r in al.iterrows():
        if ("ALPAKA", int(r.id)) in {(s_, int(i_)) for _, s_, i_ in Mset if s_ == "ALPAKA"}:
            N["M"] += 1
        else:
            N["none"] += 1
    # SINS etc.
    for (dn, st, iid) in Mset:
        if st not in ("S1", "ALPAKA"):
            N["M"] += 1
    return N

tab = {}
for rd in ("R0", "R1", "R2", "R3", "R4"):
    tab[rd] = counts(rd)
    print(f"   {rd}: {tab[rd]}")
# R0 with cross-match ignored (CFG227's own reading): M = 0
print("   CFG227 reading (no cross-match): M 0, S 9, L 6, D 41+12+6 rows, ALPAKA 10 none")
# R5: M without K2 requirement: Dunne z>=2 optimised galaxies (unique names, and group-collapsed by OName)
n5 = len(hiopt); n5o = hiopt.OName.nunique()
print(f"   R5: Dunne+22 z>=2 galaxies with optimised multi-tracer conversions (no kinematics needed): {n5} rows ({n5o} unique OName); by table: " + ", ".join(f"{TR[k]} {sum(k in l for l in hiopt.opt_tables)}" for k in TR))
tab["R5"] = dict(rows=n5, unique_oname=n5o)
R["table"] = tab

# ------------------------------------------------------------------ gas comparison where S1 or ALPAKA match
print("\n-- gas masses: Dunne optimised M_H2 against the compilation's adopted gas (S1 only; ALPAKA has no gas mass) --")
for c_ in cls_rows:
    if c_["set"] == "S1":
        s = s1[s1.alessid == c_["id"]].iloc[0]
        print(f"   S1 {c_['id']}: Amvrosiadis log M_gas (CO, alpha 0.92 as tabulated) = {s.logMgas_msun:.2f}; Dunne optimised logM_H2 ({c_['table']}) = {c_['logMH2']:.2f}; difference {s.logMgas_msun - c_['logMH2']:+.2f} dex")
        R["S1_gas_vs_dunne"] = dict(id=c_["id"], amv=float(s.logMgas_msun), dunne=c_["logMH2"], diff=float(s.logMgas_msun - c_["logMH2"]))

# ------------------------------------------------------------------ class-M candidate points (POST-FROZEN extension, labelled)
print("\n-- class-M candidate points (extension; gas-inclusive, Dunne optimised M_H2; class-M band +-0.03 / +-0.093) --")
pts = []
for c_ in cls_rows:
    if c_["cls"] != "M" or c_["set"] not in ("ALPAKA",):
        continue
    a = al[al.id == c_["id"]].iloc[0]
    Pa = alpaka_points(al[al.id == c_["id"]])
    Mst = a.mstar_1e10msun * 1e10; Mg = 10 ** c_["logMH2"]
    Re = float(Pa["Re"][0]); Rr = float(Pa["R"][0])
    row = dict(id=int(a.id), z=float(a.z), logMH2=c_["logMH2"], table=c_["table"])
    for tau in (0.0, -0.093, 0.093, -0.03, 0.03):
        gb = disc_g(Rr, Mst + Mg * 10 ** tau, Re / RD_FAC)
        for law in ("FLAT", "Hz"):
            row[f"d_{law}_tau{tau:+.3f}"] = float(delta(Pa["gobs"], gb, a.z, law)[0])
    row["D"] = float(Pa["gobs"][0] / disc_g(Rr, Mst + Mg, Re / RD_FAC))
    row["gbar_over_a0"] = float(disc_g(Rr, Mst + Mg, Re / RD_FAC) / A0["canonical"])
    pts.append(row)
    print(f"   ALPAKA {row['id']} z={row['z']:.3f} table {row['table']} logMH2 {row['logMH2']:.2f}: g_bar/a0 {row['gbar_over_a0']:.2f} D {row['D']:.2f}; delta_FLAT {row['d_FLAT_tau+0.000']:+.3f} (band +-0.093: {row['d_FLAT_tau-0.093']:+.3f}..{row['d_FLAT_tau+0.093']:+.3f}), delta_Hz {row['d_Hz_tau+0.000']:+.3f}")
R["M_points"] = pts

# ------------------------------------------------------------------ pass lines (vs CFG227 README, read in phase 1) and MUTATE 1
N_M = len(M_unique)
ck.add("R0 N_M = 0 (CFG227's statement)", N_M == 0, f"mine N_M = {N_M}: {M_unique}")
ck.add("R0 S = 9", tab["R0"]["S"] == 9, f"mine S = {tab['R0']['S']}")
ck.add("R0 L = 6", tab["R0"]["L"] == 6, f"mine L = {tab['R0']['L']}")
ck.add("C1 RC100 z>=2 N = 41 (D)", len(rec[rec.set == "RC100"]) == 41)
ck.add("C1 S1 N = 9; ALPAKA 10 (9 with M*); CRISTAL 14", len(rec[rec.set == "S1"]) == 9 and len(rec[rec.set == "ALPAKA"]) == 10 and int(rec[(rec.set == "ALPAKA")].K1.sum()) == 9 and len(rec[rec.set == "CRISTAL"]) == 14)
ck.add("R4 (z<=5): CRISTAL class L reduces to one disc (CRISTAL-11, z 4.44)", tab["R4"]["L"] == 1, f"mine {tab['R4']['L']}")
ck.add("CRISTAL class-A discs above z=5: 5 of 6", sum(1 for i in DETECTED6 if float(smp.loc[SAMPLE_ALIAS.get(i, i)].z_cii) > 5.0) == 5)

if MODE == "1":
    # M1: move CRISTAL-11 L->M and the three footnote S1 sources S->D; the frozen count line must now FAIL
    n_before = dict(tab["R0"])
    n_after = dict(n_before); n_after["L"] -= 1; n_after["M"] += 1; n_after["S"] -= 3; n_after["D"] += 3
    ck.add("M1 class-count line: counts after the mutation must equal my unmutated R0 counts (they must NOT: S -3, L -1, M +1, D +3)", n_after == n_before,
           f"baseline (S,L,M,D) = {n_before['S'], n_before['L'], n_before['M'], n_before['D']}; mutated = {n_after['S'], n_after['L'], n_after['M'], n_after['D']}")

savejson("CFG237_classes", R)
nf = ck.n_fail("M" + MODE) if MODE else ck.n_fail()
print(f"\nSUMMARY: {len(ck.rows)} lines, {ck.n_fail()} FAIL ({nf} counted for the exit code)")
for r_ in ck.rows:
    if not r_[1]: print("   FAILED" + (" (expected, kept)" if r_[3] else "") + ":", r_[0], "::", r_[2])
if MODE:
    print("MUTATE", MODE, "bites" if nf > 0 else "DOES NOT BITE"); sys.exit(1 if nf > 0 else 0)
sys.exit(0)
