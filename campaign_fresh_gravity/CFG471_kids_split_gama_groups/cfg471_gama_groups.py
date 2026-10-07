#!/usr/bin/env python3
"""CFG471 -- KiDS EARLY/LATE SPLIT BY SPECTROSCOPIC HOST STATUS (GAMA DR4 G3C GROUPS).  CFG446 found with a photo-z companion count
that companion-poor early types carry the full KiDS 1-halo split (two-regime explanation FAILS); its caveat was the +-250 Mpc
photo-z window.  Here host status is a G3C label: class C = early lens that is the IterCen of a big group (N_fof >= 3, or N_fof >= 2
with MassAfunc/h >= 10^12.5 Msun); class F = early lens GAMA sees (r < 19.8) in no group.  LCDM also predicts group centrals lens
more: SUPPORTED would not discriminate the framework from LCDM; FAILS removes the two-regime explanation again.

Criteria frozen and committed before this script existed: campaign_fresh_gravity/CFG471_kids_split_gama_groups/FROZEN_CRITERIA.md (0ce400d28).
  data     cfg110_perlens.npz, lr_lenses.npz, lr_esd_jackknife.npz (June patches); G3CGalv10 + G3CFoFGroupv10 (GAMA DR4, Data Central).
  match    nearest G3CGal galaxy within 1.5 arcsec, lenses inside the G09/G12/G15 boxes.
  stat     A_S = (D_full^T C^-1 D_S)/(D_full^T C^-1 D_full), D_S = ESD(early S) - ESD(footprint late) on K1; D_full, C^-1 fixed (CFG88);
           jackknife over the June patches touching the footprint.  Headline: (log M*, z)-matched.  SUPPORTED |A_F|/s < 2 and
           A_C/s > 3; FAILS A_F/s > 3 and A_F >= 0.70; else NON-DISCRIMINATING.
  law      B's law predicts a negligible early-minus-late difference in K1 under both footings (CFG61 stacks; projected below).
MUTATE=1: class labels shuffled among matched early lenses (20 shuffles, seeds 471-490); M1 (median |dA|/s >= 1) must FAIL -> rc 1.
Run: python3 campaign_fresh_gravity/CFG471_kids_split_gama_groups/cfg471_gama_groups.py   (MUTATE=1 for the control)
"""
import os, sys, json, hashlib
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.stats import chi2 as CHI2, norm

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(HERE)
sys.path.insert(0, CFG)
import CFG7_common as C

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("cfg471_gama_groups", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
P("  a0 footings: canonical 9.3603e-11, alt 1.1312e-10 m/s^2 (kappa = 1/2 FITTED); B's K1 prediction is the zero difference under both.")
if MUTATE:
    P("\n  *** MUTATE=1: class labels shuffled among matched early lenses -- the C/F contrast must vanish (M1 must FAIL) ***")

LR = os.path.join(C.REPO, "real_research", "data", "lensing_rar")
EXT = os.path.join(CFG, "_external_data", "cfg471")
PL = np.load(os.path.join(LR, "cfg110_perlens.npz"))
LN = np.load(os.path.join(LR, "lr_lenses.npz"))
J = np.load(os.path.join(LR, "lr_esd_jackknife.npz"))
KG = 1.989e30 / (3.0857e16) ** 2
K1 = [8, 9, 10, 11, 12, 13, 14]
NPAT = 50
HART = (NPAT - 7 - 2) / (NPAT - 1)
WGk = PL["WG"][:, K1].astype(float); WWk = PL["WW"][:, K1].astype(float)
typ, zl, lml, ra, dec = LN["typ"], LN["z"], LN["logM"], LN["ra"], LN["dec"]
patch = J["patch"]
NL = len(zl)
EARLY, LATE = typ == 1, typ == 0

# ================================================================== data integrity
R.banner("C5  CONTROL: G3C files are the logged fetch")
SHA = {"G3CGalv10.csv": "051950e193e447ebf8bf7a9458c3ffe4ea368596b8042732ee933fc95f6ad9f8",
       "G3CFoFGroupv10.csv": "eb81594ad6994e3fb44d2ee7c2e4eac4a99e3c7c27750bbf620d9f103a5b96c7"}
got = {f: hashlib.sha256(open(os.path.join(EXT, f), "rb").read()).hexdigest() for f in SHA}
check("C5 CONTROL: sha256 of both G3C files equals FETCH_LOG.md", "; ".join(f"{f}: {'ok' if got[f] == SHA[f] else 'MISMATCH'}" for f in SHA),
      all(got[f] == SHA[f] for f in SHA))
g = pd.read_csv(os.path.join(EXT, "G3CGalv10.csv"))
G = pd.read_csv(os.path.join(EXT, "G3CFoFGroupv10.csv")).set_index("GroupID")
P(f"  G3CGal rows {len(g):,} (grouped {(g.GroupID > 0).sum():,}); G3CFoFGroup rows {len(G):,}; max Rpetro {g.Rpetro.max():.3f}")

# ================================================================== footprint, cross-match, classes
R.banner("FOOTPRINT, CROSS-MATCH AND CLASSES")
box = np.zeros(NL, bool)
for a, b, c, d in ((129, 141, -2, 3), (174, 186, -3, 2), (211.5, 223.5, -2, 3)):
    box |= (ra > a) & (ra < b) & (dec > c) & (dec < d)


def uv(a, d):
    a, d = np.radians(a), np.radians(d)
    return np.c_[np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)]


tree = cKDTree(uv(g.RA.values, g.Dec.values))
dd, ii = tree.query(uv(ra, dec))
sep = np.degrees(2 * np.arcsin(dd / 2)) * 3600
for s in (1.0, 1.5, 2.0):
    P(f"  match radius {s:.1f}\": footprint early matched {int(np.sum(box & EARLY & (sep < s))):,}, late {int(np.sum(box & LATE & (sep < s))):,}")
mt = box & (sep < 1.5)
dd2, _ = tree.query(uv(ra, np.clip(dec + 60 / 3600, -90, 90)))
chance = float(np.sum(box & (np.degrees(2 * np.arcsin(dd2 / 2)) * 3600 < 1.5)) / max(mt.sum(), 1))
check("C2 CONTROL: chance-match rate (positions shifted +60\" in Dec) < 2% of the real match rate", f"{chance * 100:.3f}%", chance < 0.02)
dz = g.Z.values[ii[mt]] - zl[mt]
P(f"  spec - photo z (matched): median {np.median(dz):+.4f}, robust scatter {1.4826 * np.median(np.abs(dz - np.median(dz))):.4f}; "
  f"|dz| > 0.1: {np.mean(np.abs(dz) > 0.1) * 100:.1f}%")
gid = g.GroupID.values[ii]; cat = g.CATAID.values[ii]
nf = G.Nfof.reindex(gid).fillna(0).values
ic = G.IterCenCATAID.reindex(gid).fillna(-1).values; bc = G.BCGCATAID.reindex(gid).fillna(-1).values
mh = G.MassAfunc.reindex(gid).fillna(0).values / 0.7
big = (gid > 0) & ((nf >= 3) | ((nf >= 2) & (mh >= 10 ** 12.5)))
ME = mt & EARLY
CL = {"C": ME & big & (ic == cat), "F": ME & (gid == 0), "S": ME & (gid > 0) & (ic != cat), "P": ME & (gid > 0) & ~big & (ic == cat)}
CB = ME & big & (bc == cat)
tot = sum(CL[k].astype(int) for k in CL)
check("C3 CONTROL: classes C, F, S, P disjoint and covering the matched early lenses", f"N: " + ", ".join(f"{k} {int(CL[k].sum()):,}" for k in CL)
      + f"; matched early {int(ME.sum()):,}; BCG variant {int(CB.sum()):,}", bool(np.all(tot[ME] == 1) and np.all(tot[~ME] == 0)))
for k in CL:
    P(f"  class {k}: median log M* {np.median(lml[CL[k]]):.2f}, median z {np.median(zl[CL[k]]):.3f}")
P(f"  G3C non-IterCen members among matched early 'isolated' lenses: {CL['S'].sum() / ME.sum() * 100:.1f}% (finding, not a test)")
FP_LATE = box & LATE
P(f"  footprint: {int(box.sum()):,} lenses, early {int((box & EARLY).sum()):,}, late reference {int(FP_LATE.sum()):,}")

# ================================================================== lensing machinery
PATS = np.unique(patch[box])
NP = len(PATS)
pidx = np.full(NPAT, -1); pidx[PATS] = np.arange(NP)
# sub-patches: each June patch split in three by footprint-lens RA terciles within it
sub = np.full(NL, -1)
for p in PATS:
    m = box & (patch == p)
    q = np.quantile(ra[m], [1 / 3, 2 / 3])
    sub[m] = 3 * pidx[p] + np.digitize(ra[m], q)
P(f"  June patches touching the footprint: {NP} {PATS.tolist()}; sub-patches {len(np.unique(sub[box]))}")


def esd_all(mask, w=None):
    ww_ = np.ones(int(mask.sum())) if w is None else w[mask]
    return (WGk[mask] * ww_[:, None]).sum(0) / (WWk[mask] * ww_[:, None]).sum(0) / KG


def esd_jk(mask, w, lab, n):
    ww_ = np.ones(int(mask.sum())) if w is None else w[mask]
    gg = WGk[mask] * ww_[:, None]; vv = WWk[mask] * ww_[:, None]; pa = lab[mask]
    tg, tw = gg.sum(0), vv.sum(0)
    Sg = np.zeros((n, 7)); Sw = np.zeros((n, 7))
    np.add.at(Sg, pa, gg); np.add.at(Sw, pa, vv)
    return tg / tw / KG, (tg[None] - Sg) / (tw[None] - Sw) / KG


# full template (CFG88), 50 June patches
def esd_loo50(mask):
    return esd_jk(mask, None, patch, NPAT)


eLa, lLa = esd_loo50(LATE); eEa, lEa = esd_loo50(EARLY)
Dfull, Lfull = eEa - eLa, lEa - lLa
Rr = Lfull - Lfull.mean(0); Cf = (NPAT - 1) / NPAT * (Rr.T @ Rr); Ci = np.linalg.inv(Cf)
den = float(Dfull @ Ci @ Dfull)

R.banner("C0  CONTROL: CFG88's split from the per-lens sums")
c88 = json.load(open(os.path.join(CFG, "CFG88_kids_split_jackknife_results.json")))["numbers"]
x2full = den * HART
dD = float(np.max(np.abs(Dfull / np.array(c88["D"]) - 1)))
check("C0 CONTROL: D_full equals CFG88's K1 D (1e-6 rel) and the zero-model Hartlap chi2 equals CFG88's 35.0418 (1e-6 rel)",
      f"max rel dev {dD:.1e}; chi2 {x2full:.4f}/7 vs {c88['chi2']['L']:.4f}", dD < 1e-6 and abs(x2full / c88["chi2"]["L"] - 1) < 1e-6)
c61 = json.load(open(os.path.join(CFG, "CFG61_kids_colour_split_results.json")))["numbers"]["RES"]
AB = {f: float((np.array(c61[f]["me"]) - np.array(c61[f]["ml"]))[K1] @ Ci @ Dfull) / den for f in ("canonical", "alt")}
P(f"  B's law, early-minus-late in amplitude units (CFG61 stacks): canonical {AB['canonical']:+.4f}, alt {AB['alt']:+.4f} -- the zero model")

LAB = {"june": (np.where(box, pidx[patch], -1), NP), "sub": (sub, 3 * NP)}
REF = {k: esd_jk(FP_LATE, None, LAB[k][0], LAB[k][1]) for k in LAB}


def amp(mask, w=None, jk="june"):
    lab, n = LAB[jk]
    e, l = esd_jk(mask, w, lab, n)
    D, L = e - REF[jk][0], l - REF[jk][1]
    return float(D @ Ci @ Dfull) / den, (L @ Ci @ Dfull) / den


def jsig(reps):
    n = len(reps)
    return float(np.sqrt((n - 1) / n * np.sum((reps - reps.mean()) ** 2)))


lmc = np.clip(np.digitize(lml, np.arange(8.5, 11.1 + 1e-9, 0.2)) - 1, 0, 12)
zc = np.clip(np.digitize(zl, np.arange(0.1, 0.5 + 1e-9, 0.1)) - 1, 0, 3)
cell = lmc * 4 + zc
NC = 13 * 4


def match_weights(subm, ref):
    nref = np.bincount(cell[ref], minlength=NC).astype(float); ns = np.bincount(cell[subm], minlength=NC).astype(float)
    ok = ns > 0
    fac = np.where(ok, nref / np.where(ok, ns, 1), 0) * (subm.sum() / ref.sum())
    w = np.zeros(NL); w[subm] = fac[cell[subm]]
    return w, float(nref[~ok].sum() / nref.sum())


def verdict(Af, sf, Ac, sc):
    if abs(Af) / sf < 2 and Ac / sc > 3:
        return "TWO-REGIME SUPPORTED"
    if Af / sf > 3 and Af >= 0.70:
        return "FAILS"
    return "NON-DISCRIMINATING"


# ================================================================== C1 footprint control
R.banner("C1  CONTROL: CFG446's full-sample amplitude inside the GAMA footprint")
Abox, rbox = amp(box & EARLY); sbox = jsig(rbox)
Ame, rme = amp(ME); sme = jsig(rme)
check("C1 CONTROL: all footprint early vs footprint late, unmatched: |A_box - 1| < 2 sigma", f"A_box {Abox:+.3f} +- {sbox:.3f} "
      f"({(Abox - 1) / sbox:+.2f} s from 1; {Abox / sbox:+.2f} s from 0)", abs(Abox - 1) < 2 * sbox)
P(f"  reported: all matched early (r < 19.8) A {Ame:+.3f} +- {sme:.3f}")
R.num("C1", dict(A_box=Abox, s_box=sbox, A_matched_early=Ame, s_matched_early=sme))


def score(CLs, label="", quiet=False):
    out = {}
    for mode in ("unmatched", "matched"):
        res = {}
        for k in ("C", "F", "S", "P"):
            w, dr = match_weights(CLs[k], ME) if mode == "matched" else (None, 0.0)
            A, reps = amp(CLs[k], w)
            res[k] = (A, jsig(reps), reps, dr)
        dA = res["C"][0] - res["F"][0]; sdA = jsig(res["C"][2] - res["F"][2])
        v = verdict(res["F"][0], res["F"][1], res["C"][0], res["C"][1])
        out[mode] = dict(A={k: res[k][0] for k in res}, s={k: res[k][1] for k in res}, dropped={k: res[k][3] for k in res}, dA=dA, sdA=sdA, verdict=v)
        if not quiet:
            P(f"  [{mode}{label}] " + " | ".join(f"A_{k} {res[k][0]:+.3f} +- {res[k][1]:.3f} ({res[k][0] / res[k][1]:+.2f} s)" for k in ("C", "F", "S", "P")))
            if mode == "matched":
                P(f"  [{mode}{label}] dropped all-matched-early fraction in empty cells: " + ", ".join(f"{k} {res[k][3]:.3f}" for k in res))
            P(f"  [{mode}{label}] dA = A_C - A_F = {dA:+.3f} +- {sdA:.3f} ({dA / sdA:+.2f} s); verdict: {v}")
    return out


R.banner("HEADLINE: EARLY TYPES BY G3C HOST STATUS (C = big-group IterCen, F = in no group; S, P reported)")
RES = score(CL)
pw = 1 / RES["matched"]["s"]["F"]
P(f"  power (measured, matched): 1/s_F = {pw:.2f} (declared ~2.9), s_C = {RES['matched']['s']['C']:.3f} (declared ~0.89); "
  f"P(FAIL | A_F = 1) ~ {norm.cdf(pw - 3):.2f}" + ("  -> UNDERPOWERED to FAIL" if pw < 3 else ""))
if RES["matched"]["verdict"] != RES["unmatched"]["verdict"]:
    P("  FLAG: matched and unmatched verdicts disagree")

R.banner("REPORTED VARIANTS: BCG centrals; 36 sub-patch jackknife; group-hosted (C+S+P) vs field")
CLb = dict(CL); CLb["C"] = CB
RESb = score(CLb, " BCG", quiet=True)
P(f"  BCG centrals (matched): A_C {RESb['matched']['A']['C']:+.3f} +- {RESb['matched']['s']['C']:.3f}; verdict {RESb['matched']['verdict']}")
subres = {}
for k in ("C", "F"):
    w = match_weights(CL[k], ME)[0]
    A, reps = amp(CL[k], w, jk="sub"); subres[k] = (A, jsig(reps))
P(f"  36 sub-patch jackknife (matched): A_C {subres['C'][0]:+.3f} +- {subres['C'][1]:.3f}, A_F {subres['F'][0]:+.3f} +- {subres['F'][1]:.3f}; "
  f"verdict {verdict(subres['F'][0], subres['F'][1], subres['C'][0], subres['C'][1])}")
GH = CL["C"] | CL["S"] | CL["P"]
wg, _ = match_weights(GH, ME); wf, _ = match_weights(CL["F"], ME)
Ag, rg = amp(GH, wg); Af_, rf_ = amp(CL["F"], wf)
P(f"  group-hosted (C+S+P, N {int(GH.sum()):,}) matched A {Ag:+.3f} +- {jsig(rg):.3f}; minus field {Ag - Af_:+.3f} +- {jsig(rg - rf_):.3f}")
R.num("variants", dict(BCG=RESb["matched"], sub=subres, group_hosted=dict(A=Ag, s=jsig(rg), dA=Ag - Af_, sdA=jsig(rg - rf_))))

# ================================================================== C4 null calibration
R.banner("C4  CONTROL: null calibration of dA/s with random disjoint subsets of C and F sizes")
rngn = np.random.default_rng(471)
ie = np.where(ME)[0]; nC, nF = int(CL["C"].sum()), int(CL["F"].sum())
zz = []
for t in range(100):
    o = ie[rngn.permutation(len(ie))]
    a = np.zeros(NL, bool); b = np.zeros(NL, bool); a[o[:nC]] = True; b[o[nC:nC + nF]] = True
    A1, r1 = amp(a, match_weights(a, ME)[0]); A2, r2 = amp(b, match_weights(b, ME)[0])
    zz.append((A1 - A2) / jsig(r1 - r2))
zz = np.array(zz)
check("C4 CONTROL: std of dA/s_dA over 100 random disjoint C/F-sized subsets (matched) in [0.7, 1.4]",
      f"std {zz.std():.3f}, mean {zz.mean():+.3f}, fraction |z| >= 1: {np.mean(np.abs(zz) >= 1):.2f}", 0.7 <= zz.std() <= 1.4)
R.num("C4", dict(std=float(zz.std()), mean=float(zz.mean())))

# ================================================================== M1
R.banner("M1 / VERDICT")
if MUTATE:
    ms = []
    labels = np.array(["C", "F", "S", "P"])
    lab0 = np.empty(NL, "<U1"); lab0[:] = ""
    for k in CL:
        lab0[CL[k]] = k
    for sd in range(471, 491):
        lab = lab0.copy(); lab[ie] = lab0[ie][np.random.default_rng(sd).permutation(len(ie))]
        CLm = {k: lab == k for k in labels}
        r_ = score(CLm, quiet=True)["matched"]
        ms.append(abs(r_["dA"]) / r_["sdA"])
    m1 = float(np.median(ms))
    P(f"  shuffled |dA|/s over 20 shuffles: {np.round(ms, 2).tolist()}")
else:
    m1 = abs(RES["matched"]["dA"]) / RES["matched"]["sdA"]
check("M1 (load-bearing in MUTATE only): the C/F contrast is present, " + ("median over 20 shuffles " if MUTATE else "real ")
      + "|dA_matched|/s >= 1", f"{m1:.2f} s", m1 >= 1, load_bearing=MUTATE)
P(f"  VERDICT (matched, frozen rule): {RES['matched']['verdict']}" + ("  [UNDERPOWERED to FAIL]" if pw < 3 else "")
  + f"   [unmatched: {RES['unmatched']['verdict']}]")
P("  LCDM also predicts group centrals lens more: SUPPORTED would not discriminate the framework from LCDM.")
R.num("RES", RES); R.num("power", dict(inv_s_F=pw, s_C=RES["matched"]["s"]["C"], underpowered_to_fail=bool(pw < 3)))
R.num("C0", dict(D=Dfull.tolist(), chi2=x2full)); R.num("AB_law", AB); R.num("chance_match", chance)
R.num("counts", {k: int(CL[k].sum()) for k in CL})
nf_ = R.write(HERE)
sys.exit(1 if nf_ else 0)
